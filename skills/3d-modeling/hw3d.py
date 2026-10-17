"""Reusable 3D CAD primitives, multi-node GLB exporter, and globally depth-sorted 4-view sheet renderer."""

from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def color_mesh(mesh: trimesh.Trimesh, rgba: list[int]) -> trimesh.Trimesh:
    """Assign uniform RGBA vertex color to a trimesh object."""
    mesh.visual.vertex_colors = np.tile(np.array(rgba, dtype=np.uint8), (len(mesh.vertices), 1))
    return mesh


def box(extents, center, rgba) -> trimesh.Trimesh:
    """Create a colored box centered at world coordinates (x, y, z)."""
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(center)
    return color_mesh(m, rgba)


def cyl(radius, height, center, rgba, axis="z", sections=40) -> trimesh.Trimesh:
    """Create a colored cylinder aligned along 'x', 'y', or 'z' centered at (x, y, z)."""
    m = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    rot_axis = [0, 1, 0] if axis == "x" else ([1, 0, 0] if axis == "y" else None)
    if rot_axis:
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, rot_axis))
    m.apply_translation(center)
    return color_mesh(m, rgba)


def parabolic_arc(xs, y_pos, z_base, coeff, width_y, height_z, rgba, x_center=0.34) -> list[trimesh.Trimesh]:
    """Create a shallow curved beam along X at fixed Y (use instead of full torus for rockers/arches)."""
    segs = []
    for i in range(len(xs) - 1):
        x0, x1 = float(xs[i]), float(xs[i + 1])
        xm = 0.5 * (x0 + x1)
        zm = z_base + coeff * (xm - x_center) ** 2
        dz = coeff * ((x1 - x_center) ** 2 - (x0 - x_center) ** 2)
        dx = x1 - x0
        seg = trimesh.creation.box(extents=[float(np.hypot(dx, dz)) + 0.005, width_y, height_z])
        seg.apply_transform(trimesh.transformations.rotation_matrix(-float(np.arctan2(dz, dx)), [0, 1, 0]))
        seg.apply_translation([xm, y_pos, zm])
        segs.append(color_mesh(seg, rgba))
    return segs


def export_bundle(parts: dict[str, trimesh.Trimesh], out_dir: Path, name: str = "assembly"):
    """Export individual part STLs, combined STL, and multi-node GLB preserving part names & colors."""
    out_dir.mkdir(parents=True, exist_ok=True)
    scene = trimesh.Scene()
    for part_name, mesh in parts.items():
        mesh.export(out_dir / f"{part_name}.stl")
        scene.add_geometry(mesh, node_name=part_name, geom_name=part_name)
    scene.export(out_dir / f"{name}.glb")
    trimesh.util.concatenate(list(parts.values())).export(out_dir / f"{name}.stl")


def shade_faces(mesh: trimesh.Trimesh):
    """Compute Lambertian shaded face RGBA from mesh vertex colors and directional light."""
    ldir = np.array([-0.45, -0.65, 0.62]) / np.linalg.norm([-0.45, -0.65, 0.62])
    tris = mesh.vertices[mesh.faces]
    intensity = 0.56 + 0.44 * np.clip(mesh.face_normals @ ldir, -0.25, 1.0)
    base_rgb = mesh.visual.vertex_colors[mesh.faces[:, 0], :3] / 255.0
    shaded = np.clip(base_rgb * intensity[:, None], 0.0, 1.0)
    return tris, np.hstack([shaded, np.full((len(mesh.faces), 1), 0.98)])


def filter_bounds(tris, rgba, b):
    """Crop triangle arrays to a 3D bounding box ((xmin, xmax), (ymin, ymax), (zmin, zmax))."""
    if b is None:
        return tris, rgba
    c = tris.mean(axis=1)
    m = (c[:, 0] >= b[0][0]) & (c[:, 0] <= b[0][1]) & (c[:, 1] >= b[1][0]) & (c[:, 1] <= b[1][1]) & (c[:, 2] >= b[2][0]) & (c[:, 2] <= b[2][1])
    return tris[m], rgba[m]


def draw_scene_unified(ax, parts: dict[str, trimesh.Trimesh], bounds=None):
    """Draw all meshes in one unified Poly3DCollection so matplotlib depth-sorts globally across parts."""
    pairs = [filter_bounds(*shade_faces(m), bounds) for m in parts.values()]
    tris = np.concatenate([p[0] for p in pairs if len(p[0]) > 0], axis=0)
    rgba = np.concatenate([p[1] for p in pairs if len(p[0]) > 0], axis=0)
    poly = Poly3DCollection(tris, facecolors=rgba, edgecolors=(0.1, 0.13, 0.18, 0.18), linewidths=0.22, zsort="average")
    ax.add_collection3d(poly)


def draw_one_callout(ax, xyz, axes_xy, text, accent):
    """Project one 3D target point to 2D and render a margin callout badge."""
    x2, y2, _ = proj3d.proj_transform(xyz[0], xyz[1], xyz[2], ax.get_proj())
    ax.scatter([xyz[0]], [xyz[1]], [xyz[2]], color=accent, edgecolors="#ffffff", linewidths=0.8, s=28, zorder=200)
    bbox = {"boxstyle": "round,pad=0.32", "facecolor": "#f8fafc", "edgecolor": accent, "linewidth": 1.5, "alpha": 0.96}
    arrow = {"arrowstyle": "-|>", "color": accent, "lw": 1.4, "shrinkA": 0, "shrinkB=3": 3, "connectionstyle": "arc3,rad=0.06"}
    arrow.pop("shrinkB=3", None)
    arrow["shrinkB"] = 3
    ax.annotate(text, xy=(x2, y2), xytext=axes_xy, textcoords="axes fraction", fontsize=8.2, fontweight="bold",
                color="#0f172a", ha="center", va="center", zorder=210, bbox=bbox, arrowprops=arrow)


def add_callouts_2d(ax, callouts):
    """Render a list of (target_xyz, axes_fraction_xy, label_text, hex_color) callouts on a 3D axes."""
    for item in callouts:
        draw_one_callout(ax, *item)
