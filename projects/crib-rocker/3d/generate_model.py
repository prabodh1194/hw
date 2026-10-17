#!/usr/bin/env python3
"""Generate 3D model and multi-angle preview render of the HunyHuny crib rocker setup."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from model.parts import (
    create_actuator,
    create_grill_clamp_bracket,
    create_crib_rail_clamp,
    create_controller_enclosure,
    create_crib_frame_section,
    create_window_grill_section,
)
from model.environment import create_floor, create_wall
from model.export import export_parts, export_assembly
from render_preview import render_preview


def create_all_parts():
    """Create all parts positioned in real-world coordinates (meters)."""
    return {
        "actuator": create_actuator(),
        "u_bolt_bracket": create_grill_clamp_bracket(),
        "l_bracket": create_crib_rail_clamp(),
        "pivot_pin": create_controller_enclosure(),
        "crib_frame": create_crib_frame_section(),
        "window_grill": create_window_grill_section(),
        "floor": create_floor(),
        "wall": create_wall(),
    }


def main():
    parts = create_all_parts()
    export_parts(parts)
    export_assembly(parts)
    render_preview(Path(__file__).parent / "preview.png")


if __name__ == "__main__":
    main()
