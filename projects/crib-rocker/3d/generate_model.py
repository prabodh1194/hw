#!/usr/bin/env python3
"""Generate 3D model of crib rocker mechanism — Apple-inspired design."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from model.parts import (
    create_actuator,
    create_u_bolt_bracket,
    create_l_bracket,
    create_pivot_pin,
    create_crib_frame_section,
    create_window_grill_section,
)
from model.export import export_parts, export_assembly


def create_all_parts():
    """Create all parts and return as dict."""
    return {
        "actuator": create_actuator(),
        "u_bolt_bracket": create_u_bolt_bracket(),
        "l_bracket": create_l_bracket(),
        "pivot_pin": create_pivot_pin(),
        "crib_frame": create_crib_frame_section(),
        "window_grill": create_window_grill_section(),
    }


def position_parts(parts):
    """Position all parts in the assembly."""
    parts["u_bolt_bracket"].apply_translation([0, 0.04, 0.25])
    parts["actuator"].apply_translation([0, 0.04, 0.25])
    parts["pivot_pin"].apply_translation([0, 0.04, 0.32])
    parts["l_bracket"].apply_translation([0, 0.04, 0.32])
    parts["crib_frame"].apply_translation([0.12, 0, 0])
    parts["window_grill"].apply_translation([-0.08, 0, 0])
    return parts


def main():
    """Generate and export all 3D models."""
    parts = create_all_parts()
    parts = position_parts(parts)
    export_parts(parts)
    export_assembly(parts)


if __name__ == "__main__":
    main()
