#!/usr/bin/env python3
"""Render annotated product-photo style reference sheets: real 12V metal linear actuator + both mount brackets."""

import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills" / "3d-modeling"))
sys.path.insert(0, str(Path(__file__).parent))

from hw3d import add_callouts_2d, draw_scene_unified, box
from model.parts import MECH_Y, MECH_Z, create_actuator, create_crib_rail_clamp, create_grill_clamp_bracket

INK = "#f8fafc"
PANEL = "#1e293b"


def _setup_ax(fig, idx, title, elev, azim, xlim, ylim, zlim, ncols=2):
    ax = fig.add_subplot(1, ncols, idx, projection="3d", facecolor=PANEL)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_zlim(*zlim)
    ax.set_box_aspect([xlim[1] - xlim[0], ylim[1] - ylim[0], zlim[1] - zlim[0]])
    ax.set_title(title, color=INK, fontsize=12, fontweight="bold", pad=10)
    ax.tick_params(colors="#94a3b8", labelsize=7)
    for p in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        p.set_facecolor((0.08, 0.12, 0.19, 0.90))
    ax.set_xlabel("X (m)", color="#cbd5e1", fontsize=8, labelpad=2)
    ax.set_ylabel("Y (m)", color="#cbd5e1", fontsize=8, labelpad=2)
    ax.set_zlabel("Z (m)", color="#cbd5e1", fontsize=8, labelpad=2)
    return ax


def render_actuator_reference(out_path: Path):
    parts = {"actuator": create_actuator()}
    fig = plt.figure(figsize=(15, 10), dpi=160, facecolor="#0f172a")
    fig.suptitle("Reference: What the 12V Metal Linear Actuator Actually Looks Like (Generic 300N–750N Industrial Actuator)",
                 fontsize=15, fontweight="bold", color=INK, y=0.985)
    ax = _setup_ax(fig, 1, "Part #3 — 12V DC Heavy-Duty Metal Linear Actuator (300N–750N, 50mm Stroke) with Integrated Clevis Mounts",
                   22, -52, (-0.24, 0.08), (-0.58, -0.16), (0.66, 0.94), ncols=1)
    draw_scene_unified(ax, parts)
    plt.tight_layout(rect=[0, 0.01, 1, 0.95]); fig.canvas.draw()
    add_callouts_2d(ax, [
        ((-0.165, MECH_Y, MECH_Z), (0.12, 0.80), "① Rear Mounting Eye\n(Pins to Grill Bracket #1)", "#0284c7"),
        ((-0.11, MECH_Y, MECH_Z - 0.028), (0.20, 0.20), "② Underslung 12V DC\nGeared Motor Pod", "#f97316"),
        ((-0.10, MECH_Y, MECH_Z + 0.005), (0.52, 0.92), "③ Anodized Aluminum Outer Tube\n(Splash Resistant IP54)", "#e2e8f0"),
        ((-0.024, MECH_Y, MECH_Z), (0.76, 0.72), "④ Polished Stainless Steel\nExtension Rod (±25mm Stroke)", "#facc15"),
        ((0.005, MECH_Y, MECH_Z), (0.82, 0.30), "⑤ Front Mounting Eye\n(Pins to Crib Clamp #5)", "#7c3aed"),
    ])
    fig.savefig(out_path, dpi=160, facecolor=fig.get_facecolor()); plt.close(fig)


GRILL_CALLOUTS = [
    ((-0.20, MECH_Y, MECH_Z + 0.02), (0.18, 0.86), "① TPU/Rubber Liner\n(Non-Slip, Non-Scratch)", "#16a34a"),
    ((-0.20, MECH_Y, MECH_Z - 0.02), (0.20, 0.16), "② Split Body Wraps\nAround the Grill Bar", "#0284c7"),
    ((-0.172, MECH_Y, MECH_Z + 0.015), (0.80, 0.82), "③ Clevis Ears + Pin Hole\n(Links to Actuator Eye #2)", "#e2e8f0"),
    ((-0.20, MECH_Y + 0.022, MECH_Z - 0.022), (0.82, 0.28), "④ 4× M4 Hex Bolts\n(Tighten in X-Pattern)", "#facc15"),
]

RAIL_CALLOUTS = [
    ((0.02, MECH_Y, MECH_Z + 0.028), (0.22, 0.84), "① 3mm Self-Adhesive Felt Lining\n(Protects Pinewood Rail)", "#16a34a"),
    ((0.02, MECH_Y + 0.034, MECH_Z), (0.82, 0.80), "② Anodized Aluminum Outer Wrap\n(No-Drill Saddle)", "#0284c7"),
    ((0.005, MECH_Y - 0.011, MECH_Z), (0.20, 0.22), "③ Clevis Ears + Pin Hole\n(Links to Actuator Rod #4)", "#e2e8f0"),
    ((0.02, MECH_Y, MECH_Z), (0.52, 0.36), "HunyHuny Crib\nLeft Top Rail", "#d97706"),
]


def _render_grill_panel(fig):
    grill_bar = box([0.012, 0.068, 0.068], [-0.212, MECH_Y, MECH_Z], [120, 130, 145, 255])
    ax = _setup_ax(fig, 1, "Part #1 — Window Grill Split-Clamp Bracket (Bolts onto 12mm Black Grill Bar)",
                   24, -58, (-0.32, -0.10), (-0.52, -0.24), (0.70, 0.90))
    draw_scene_unified(ax, {"g": create_grill_clamp_bracket(), "bar": grill_bar})
    return ax


def _render_rail_panel(fig):
    pine_rail = box([0.026, 1.10, 0.042], [0.02, 0.0, MECH_Z], [218, 182, 132, 255])
    ax = _setup_ax(fig, 2, "Part #5 — Felt-Lined Crib Rail Clamp (Wraps 26mm × 42mm Pinewood Crib Top Rail)",
                   20, -64, (-0.06, 0.12), (-0.48, -0.26), (0.70, 0.90))
    draw_scene_unified(ax, {"c": create_crib_rail_clamp(), "pine": pine_rail})
    return ax


def render_brackets_reference(out_path: Path):
    fig = plt.figure(figsize=(18, 10), dpi=160, facecolor="#0f172a")
    fig.suptitle("Reference: What the Mount Brackets Look Like & How They Clamp (NO Drilling Required)",
                 fontsize=15, fontweight="bold", color=INK, y=0.985)
    _render_grill_panel(fig)
    _render_rail_panel(fig)
    plt.tight_layout(rect=[0, 0.01, 1, 0.95]); fig.canvas.draw()
    _annotate_panels(fig)
    fig.savefig(out_path, dpi=160, facecolor=fig.get_facecolor()); plt.close(fig)


def _annotate_panels(fig):
    axes = fig.get_axes()
    add_callouts_2d(axes[0], GRILL_CALLOUTS)
    add_callouts_2d(axes[1], RAIL_CALLOUTS)


if __name__ == "__main__":
    render_actuator_reference(Path(__file__).parent / "actuator-reference.png")
    render_brackets_reference(Path(__file__).parent / "brackets-reference.png")
