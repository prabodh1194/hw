"""Export individual STL parts and multi-node GLB assembly."""

from pathlib import Path
import trimesh

OUT_DIR = Path(__file__).parent.parent


def export_parts(parts: dict[str, trimesh.Trimesh]):
    """Export individual parts as STL files."""
    for name, mesh in parts.items():
        path = OUT_DIR / f"{name}.stl"
        mesh.export(path)
        print(f"Exported: {path}")


def export_assembly(parts: dict[str, trimesh.Trimesh]):
    """Export assembled scene as multi-node GLB (preserving colors & part hierarchy) and combined STL."""
    scene = trimesh.Scene()
    for name, mesh in parts.items():
        scene.add_geometry(mesh, node_name=name, geom_name=name)

    glb_path = OUT_DIR / "crib-rocker-assembly.glb"
    scene.export(glb_path)
    print(f"Exported: {glb_path}")

    combined = trimesh.util.concatenate(list(parts.values()))
    stl_path = OUT_DIR / "crib-rocker-assembly.stl"
    combined.export(stl_path)
    print(f"Exported: {stl_path}")
