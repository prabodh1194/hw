#!/usr/bin/env python3
"""Render a shaded, globally depth-sorted multi-view 3D engineering sheet with non-overlapping 2D callouts."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from model.parts import (
    create_actuator, create_grill_clamp_bracket, create_crib_rail_clamp,
    create_controller_enclosure, create_crib_frame_section, create_window_grill_section,
)
from model.environment import create_floor, create_wall

CALLOUTS_PANEL_1 = [
    ((-0.20, -0.02, 1.14), (0.15, 0.84), "Black Window Grill\n(Fixed Anchor @ X=-20cm)", "#0284c7"),
    ((-0.17, 0.42, 1.15), (0.44, 0.92), "Yellow Window Curtain\n(Back-Left Corner)", "#ca8a04"),
    ((0.34, 0.56, 0.92), (0.78, 0.88), "Arched Headboard\n+ Pastel Bumpers", "#db2777"),
    ((-0.25, -0.48, 0.77), (0.15, 0.62), "ESP32 + Driver Pod\n(On Recessed Window Sill)", "#16a34a"),
    ((-0.09, -0.38, 0.78), (0.16, 0.42), "12V Linear Actuator\n(Bridges 20cm Sill-Crib Gap)", "#ea580c"),
    ((-0.08, -0.78, 0.66), (0.15, 0.21), "Foreground White\nSide Table / Desk", "#475569"),
    ((0.34, -0.56, 0.90), (0.46, 0.48), "HunyHuny Arched Footboard\n+ Drop Panel", "#7c3aed"),
    ((1.03, -0.10, 0.48), (0.83, 0.58), "Adjacent Parent Bed\n(Right Side of Crib)", "#2563eb"),
    ((0.34, -0.56, 0.03), (0.54, 0.12), "Curved Bottom Rocker Rail\n(Side-to-Side Rocking Arc)", "#d97706"),
]

CALLOUTS_PANEL_2 = [
    ((-0.20, -0.38, 0.78), (0.19, 0.88), "1. Grill Split-Clamp Bracket\n(TPU-Padded on Black Grill Bar)", "#0284c7"),
    ((-0.165, -0.38, 0.78), (0.64, 0.92), "2. Rear Clevis Pivot Pin\n(Allows Vertical Rocking Angle)", "#475569"),
    ((-0.25, -0.48, 0.77), (0.18, 0.58), "6. ESP32 Controller + E-Stop\n(Rests on Flat Window Sill)", "#16a34a"),
    ((-0.11, -0.38, 0.76), (0.24, 0.20), "3. 12V Silent Linear Actuator\n(Alu Body + Underslung Gearmotor)", "#ea580c"),
    ((-0.024, -0.38, 0.78), (0.80, 0.78), "4. Stainless Extension Rod\n(±30mm Gentle Rocking Stroke)", "#ca8a04"),
    ((0.020, -0.38, 0.78), (0.80, 0.50), "5. Felt-Lined Crib Rail Clamp\n(No-Drill Wrap on Pinewood Rail)", "#7c3aed"),
]

CALLOUTS_PANEL_3 = [
    ((-0.20, -0.02, 1.14), (0.17, 0.86), "Black Window Grill\n(Anchored into Sill)", "#0284c7"),
    ((-0.08, -0.38, 0.78), (0.55, 0.85), "Horizontal Actuator Bridge\n(±3 cm Push/Pull @ Z=78 cm)", "#ea580c"),
    ((-0.27, -0.40, 0.72), (0.17, 0.44), "Recessed Window Sill\n(Height Z = 72 cm)", "#0284c7"),
    ((0.34, -0.56, 0.02), (0.48, 0.13), "Curved Pinewood Rocker Base\n(Converts Push into ±4° Roll)", "#d97706"),
    ((1.00, 0.0, 0.48), (0.82, 0.62), "Adjacent Parent Bed\n(Right of Crib @ X > +74 cm)", "#2563eb"),
]

CALLOUTS_PANEL_4 = [
    ((-0.17, 0.42, 1.0), (0.18, 0.86), "Yellow Window Curtain\n(Back-Left Corner)", "#ca8a04"),
    ((-0.24, -0.05, 0.75), (0.18, 0.62), "Window Sill + Grill\n(X = -38 to -18 cm)", "#0284c7"),
    ((-0.09, -0.38, 0.78), (0.19, 0.38), "Actuator Bridge\n(20 cm Sill-to-Crib Gap)", "#ea580c"),
    ((-0.08, -0.78, 0.68), (0.24, 0.14), "Foreground White Desk\n(Bottom-Left of Photo)", "#475569"),
    ((0.34, 0.10, 0.50), (0.53, 0.86), "HunyHuny Baby Cot\n(68 cm × 116 cm + Bumpers)", "#7c3aed"),
    ((1.03, 0.0, 0.50), (0.83, 0.54), "Adjacent Parent Bed\n(Right Side of Crib)", "#2563eb"),
]


def _shade_faces(mesh):
    ldir = np.array([-0.45, -0.65, 0.62]) / np.linalg.norm([-0.45, -0.65, 0.62])
    tris = mesh.vertices[mesh.faces]
    intensity = 0.56 + 0.44 * np.clip(mesh.face_normals @ ldir, -0.25, 1.0)
    base_rgb = mesh.visual.vertex_colors[mesh.faces[:, 0], :3] / 255.0
    shaded = np.clip(base_rgb * intensity[:, None], 0.0, 1.0)
    return tris, np.hstack([shaded, np.full((len(mesh.faces), 1), 0.98)])


def _filter_bounds(tris, rgba, b):
    if b is None:
        return tris, rgba
    c = tris.mean(axis=1)
    m = (c[:, 0] >= b[0][0]) & (c[:, 0] <= b[0][1]) & (c[:, 1] >= b[1][0]) & (c[:, 1] <= b[1][1]) & (c[:, 2] >= b[2][0]) & (c[:, 2] <= b[2][1])
    return tris[m], rgba[m]


def _draw_scene_unified(ax, parts, bounds=None):
    pairs = [_filter_bounds(*_shade_faces(m), bounds) for m in parts.values()]
    tris = np.concatenate([p[0] for p in pairs if len(p[0]) > 0], axis=0)
    rgba = np.concatenate([p[1] for p in pairs if len(p[0]) > 0], axis=0)
    poly = Poly3DCollection(tris, facecolors=rgba, edgecolors=(0.1, 0.13, 0.18, 0.18), linewidths=0.22, zsort="average")
    ax.add_collection3d(poly)


def _draw_one_callout(ax, xyz, axes_xy, text, accent):
    x2, y2, _ = proj3d.proj_transform(xyz[0], xyz[1], xyz[2], ax.get_proj())
    ax.scatter([xyz[0]], [xyz[1]], [xyz[2]], color=accent, edgecolors="#ffffff", linewidths=0.8, s=28, zorder=200)
    bbox = {"boxstyle": "round,pad=0.32", "facecolor": "#f8fafc", "edgecolor": accent, "linewidth": 1.5, "alpha": 0.96}
    arrow = {"arrowstyle": "-|>", "color": accent, "lw": 1.4, "shrinkA": 0, "shrinkB": 3, "connectionstyle": "arc3,rad=0.06"}
    ax.annotate(text, xy=(x2, y2), xytext=axes_xy, textcoords="axes fraction", fontsize=8.2, fontweight="bold",
                color="#0f172a", ha="center", va="center", zorder=210, bbox=bbox, arrowprops=arrow)


def _add_callouts_2d(ax, callouts):
    for item in callouts:
        _draw_one_callout(ax, *item)


def _setup_panel(fig, idx, parts, elev, azim, xlim, ylim, zlim, title, bounds=None):
    ax = fig.add_subplot(2, 2, idx, projection="3d", facecolor="#1e293b")
    _draw_scene_unified(ax, parts, bounds=bounds)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_zlim(*zlim)
    ax.set_box_aspect([xlim[1] - xlim[0], ylim[1] - ylim[0], zlim[1] - zlim[0]])
    ax.set_title(title, color="#f8fafc", fontsize=11.5, fontweight="bold", pad=8)
    ax.set_xlabel("X (m) — Window → Crib → Bed", color="#cbd5e1", fontsize=8, labelpad=2)
    ax.set_ylabel("Y (m) — Front → Back", color="#cbd5e1", fontsize=8, labelpad=2)
    ax.set_zlabel("Z (m) — Height", color="#cbd5e1", fontsize=8, labelpad=2)
    ax.tick_params(colors="#94a3b8", labelsize=7)
    for p in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        p.set_facecolor((0.08, 0.12, 0.19, 0.90))
    return ax


def render_preview(out_path: Path):
    parts = {"floor": create_floor(), "wall": create_wall(), "window_grill": create_window_grill_section(),
             "crib_frame": create_crib_frame_section(), "u_bolt_bracket": create_grill_clamp_bracket(),
             "actuator": create_actuator(), "l_bracket": create_crib_rail_clamp(), "pivot_pin": create_controller_enclosure()}
    fig = plt.figure(figsize=(18, 12.5), dpi=160, facecolor="#0f172a")
    fig.suptitle("Crib Rocker 3D Mock Model — Room Layout (IMG_2438) & Horizontal Window-Grill Actuator Assembly",
                 fontsize=15, fontweight="bold", color="#f8fafc", y=0.975)
    axes = [
        _setup_panel(fig, 1, parts, 28, -58, (-0.42, 1.25), (-0.88, 0.78), (0.0, 1.38), "1. Photo Perspective (Matches IMG_2438.jpg Bed/Crib/Window Layout)"),
        _setup_panel(fig, 2, parts, 24, -52, (-0.34, 0.16), (-0.62, -0.12), (0.62, 1.00), "2. Mechanism Detail — Window Grill to Crib Left Rail (Z = 78 cm)", ((-0.36, 0.22), (-0.65, -0.05), (0.58, 1.05))),
        _setup_panel(fig, 3, parts, 10, -86, (-0.38, 1.20), (-0.82, 0.65), (0.0, 1.32), "3. Front Kinematic View — Horizontal Push ↔ Curved Rocker Motion", ((-0.42, 1.35), (-0.88, 0.65), (-0.02, 1.38))),
        _setup_panel(fig, 4, parts, 84, -90, (-0.40, 1.25), (-0.88, 0.78), (0.0, 1.35), "4. Top-Down Room Plan — Window Wall (Left), Crib (Center), Bed (Right)"),
    ]
    plt.tight_layout(rect=[0, 0.01, 1, 0.955]); fig.canvas.draw()
    for ax, c_list in zip(axes, (CALLOUTS_PANEL_1, CALLOUTS_PANEL_2, CALLOUTS_PANEL_3, CALLOUTS_PANEL_4)):
        _add_callouts_2d(ax, c_list)
    fig.savefig(out_path, dpi=160, facecolor=fig.get_facecolor()); plt.close(fig)


if __name__ == "__main__":
    render_preview(Path(__file__).parent / "preview.png")
