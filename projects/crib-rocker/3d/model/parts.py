"""Part creation functions for crib rocker model."""

import trimesh
import numpy as np


def rounded_box(extents, radius=0.005):
    """Create a box with rounded edges."""
    return trimesh.creation.box(extents=extents)


def create_actuator():
    """Premium linear actuator."""
    body = trimesh.creation.cylinder(radius=0.025, height=0.18, sections=48)
    body.apply_translation([0, 0, 0.09])
    cap = trimesh.creation.cylinder(radius=0.025, height=0.01, sections=48)
    cap.apply_translation([0, 0, 0.185])
    rod = trimesh.creation.cylinder(radius=0.010, height=0.12, sections=32)
    rod.apply_translation([0, 0, 0.25])
    rod_end = trimesh.creation.cylinder(radius=0.015, height=0.025, sections=32)
    rod_end.apply_translation([0, 0, 0.32])
    body_end = trimesh.creation.cylinder(radius=0.015, height=0.02, sections=32)
    body_end.apply_translation([0, 0, -0.01])
    return trimesh.util.concatenate([body, cap, rod, rod_end, body_end])


def create_u_bolt_bracket():
    """Minimal mounting bracket."""
    plate = rounded_box([0.06, 0.015, 0.08], radius=0.003)
    plate.apply_translation([0, 0, 0.04])
    u_bolt = trimesh.creation.torus(major_radius=0.03, minor_radius=0.004)
    u_bolt.apply_translation([0, 0, 0.04])
    return trimesh.util.concatenate([plate, u_bolt])


def create_l_bracket():
    """L-bracket with seamless corner."""
    h_part = rounded_box([0.05, 0.015, 0.012], radius=0.002)
    h_part.apply_translation([0, 0, 0.006])
    v_part = rounded_box([0.012, 0.015, 0.05], radius=0.002)
    v_part.apply_translation([-0.019, 0, 0.025])
    boss = trimesh.creation.cylinder(radius=0.010, height=0.02, sections=24)
    rot = trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])
    boss.apply_transform(rot)
    boss.apply_translation([-0.019, 0, 0.045])
    return trimesh.util.concatenate([h_part, v_part, boss])


def create_pivot_pin():
    """Pivot pin — polished, minimal."""
    pin = trimesh.creation.cylinder(radius=0.005, height=0.04, sections=24)
    rot = trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])
    pin.apply_transform(rot)
    return pin


def create_crib_frame_section():
    """Crib frame — elegant curved rocker, clean posts."""
    rocker = trimesh.creation.torus(major_radius=0.35, minor_radius=0.012)
    rot = trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])
    rocker.apply_transform(rot)
    rocker.apply_translation([0, 0, 0.35])
    post = rounded_box([0.025, 0.025, 0.35], radius=0.004)
    post.apply_translation([0.08, 0, 0.175])
    rail = rounded_box([0.20, 0.018, 0.025], radius=0.003)
    rail.apply_translation([0, 0, 0.32])
    return trimesh.util.concatenate([rocker, post, rail])


def create_window_grill_section():
    """Window grill — minimal vertical bars."""
    bars = []
    for i in range(5):
        x = i * 0.07 - 0.14
        bar = trimesh.creation.cylinder(radius=0.006, height=0.50, sections=16)
        bar.apply_translation([x, 0, 0.25])
        bars.append(bar)
    for z in [0.08, 0.25, 0.42]:
        cross = rounded_box([0.35, 0.012, 0.012], radius=0.002)
        cross.apply_translation([0, 0, z])
        bars.append(cross)
    return trimesh.util.concatenate(bars)
