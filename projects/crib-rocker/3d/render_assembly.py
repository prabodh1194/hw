#!/usr/bin/env python3
"""Render a 4-stage Exploded & Sequential Assembly Sheet (assembly-steps.png) for the Crib Rocker."""

import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills" / "3d-modeling"))
sys.path.insert(0, str(Path(__file__).parent))

from hw3d import add_callouts_2d, draw_scene_unified
from model.environment import create_floor, create_wall
from model.parts import (
    create_actuator, create_controller_enclosure, create_crib_frame_section,
    create_crib_rail_clamp, create_grill_clamp_bracket, create_window_grill_section,
)

BOUNDS_MECH = ((-0.40, 0.24), (-0.66, -0.06), (0.58, 1.06))

STAGE_CALLOUTS = [
    [((-0.26, -0.38, 0.78), (0.18, 0.88), "1. Grill Split-Clamp\n(Exploded -6 cm in X)", "#0284c7"),
     ((-0.11, -0.38, 0.78), (0.54, 0.90), "3. 12V Linear Actuator\n(Center Bridge Sub-Assembly)", "#ea580c"),
     ((0.08, -0.38, 0.78), (0.82, 0.80), "5. Felt-Lined Crib Clamp\n(Exploded +6 cm in X)", "#7c3aed"),
     ((-0.25, -0.54, 0.85), (0.20, 0.20), "6. ESP32 + BTS7960 Pod\n(Exploded +8 cm Above Sill)", "#16a34a")],
    [((-0.20, -0.38, 0.78), (0.22, 0.86), "Step 1A: Clamp Split-Bracket\nto 12mm Black Grill Bar", "#0284c7"),
     ((-0.165, -0.38, 0.78), (0.74, 0.86), "Step 1B: Torque 4× M4 Bolts\n& Verify Clevis Ears @ Z=78cm", "#38bdf8"),
     ((0.02, -0.38, 0.78), (0.76, 0.24), "Crib Left Top Rail\nAligned 20 cm from Grill", "#d97706")],
    [((-0.165, -0.38, 0.78), (0.22, 0.88), "Step 2A: Insert 6mm Rear\nClevis Pin + R-Clip", "#0284c7"),
     ((-0.09, -0.38, 0.78), (0.24, 0.20), "Step 2B: Set Actuator Rod\nto Mid-Stroke (25 mm)", "#ea580c"),
     ((0.02, -0.38, 0.78), (0.77, 0.82), "Step 2C: Slip Felt Clamp Over\nCrib Rail & Pin Front Clevis", "#7c3aed")],
    [((-0.25, -0.48, 0.77), (0.20, 0.86), "Step 3A: Place ESP32 Pod\non Recessed Window Sill", "#16a34a"),
     ((-0.14, -0.38, 0.76), (0.24, 0.20), "Step 3B: Plug 2-Wire Motor\nLead into BTS7960 M+/M-", "#ea580c"),
     ((0.02, -0.38, 0.78), (0.78, 0.84), "Step 3C: Ready — 20 kHz Sine\nPWM Rocks Crib ±3 cm", "#22c55e")],
]


def _shifted(mesh, dx=0.0, dy=0.0, dz=0.0):
    m = mesh.copy()
    m.apply_translation([dx, dy, dz])
    return m


def _stage_parts(stage: int):
    base = {"floor": create_floor(), "wall": create_wall(),
            "window_grill": create_window_grill_section(), "crib_frame": create_crib_frame_section()}
    if stage == 1:
        return {**base, "g": _shifted(create_grill_clamp_bracket(), dx=-0.06),
                "a": create_actuator(), "c": _shifted(create_crib_rail_clamp(), dx=0.06),
                "p": _shifted(create_controller_enclosure(), dy=-0.06, dz=0.08)}
    if stage == 2:
        return {**base, "g": create_grill_clamp_bracket()}
    if stage == 3:
        return {**base, "g": create_grill_clamp_bracket(), "a": create_actuator(), "c": create_crib_rail_clamp()}
    return {**base, "g": create_grill_clamp_bracket(), "a": create_actuator(),
            "c": create_crib_rail_clamp(), "p": create_controller_enclosure()}


def _setup_ax(fig, idx, title):
    ax = fig.add_subplot(2, 2, idx, projection="3d", facecolor="#1e293b")
    draw_scene_unified(ax, _stage_parts(idx), bounds=BOUNDS_MECH)
    ax.view_init(elev=25, azim=-54)
    ax.set_xlim(-0.36, 0.18); ax.set_ylim(-0.64, -0.10); ax.set_zlim(0.62, 1.02)
    ax.set_box_aspect([0.54, 0.54, 0.40])
    ax.set_title(title, color="#f8fafc", fontsize=11.5, fontweight="bold", pad=8)
    ax.set_xlabel("X (m) — Window → Crib", color="#cbd5e1", fontsize=8, labelpad=2)
    ax.set_ylabel("Y (m) — Front → Back", color="#cbd5e1", fontsize=8, labelpad=2)
    ax.set_zlabel("Z (m) — Height", color="#cbd5e1", fontsize=8, labelpad=2)
    ax.tick_params(colors="#94a3b8", labelsize=7)
    for p in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        p.set_facecolor((0.08, 0.12, 0.19, 0.90))
    return ax


def render_assembly(out_path: Path):
    fig = plt.figure(figsize=(18, 12.5), dpi=160, facecolor="#0f172a")
    fig.suptitle("Crib Rocker 3D Assembly Guide — Exploded BOM & 4-Stage Installation Sequence",
                 fontsize=15, fontweight="bold", color="#f8fafc", y=0.975)
    titles = [
        "Stage 1 — Exploded View of All 4 Custom/Off-the-Shelf Modules",
        "Stage 2 — Clamp TPU-Lined Split Bracket (#1) to Black Window Grill Bar",
        "Stage 3 — Pin 12V Linear Actuator (#3) & Felt-Lined Crib Rail Clamp (#5)",
        "Stage 4 — Place ESP32 + BTS7960 Controller Pod (#6) on Window Sill & Wire",
    ]
    axes = [_setup_ax(fig, i + 1, titles[i]) for i in range(4)]
    plt.tight_layout(rect=[0, 0.01, 1, 0.955]); fig.canvas.draw()
    for ax, c_list in zip(axes, STAGE_CALLOUTS):
        add_callouts_2d(ax, c_list)
    fig.savefig(out_path, dpi=160, facecolor=fig.get_facecolor()); plt.close(fig)


if __name__ == "__main__":
    render_assembly(Path(__file__).parent / "assembly-steps.png")
