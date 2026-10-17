"""Realistic 3D part geometry for the HunyHuny crib + window grill rocker setup (matching IMG_2438.jpg)."""

import numpy as np
import trimesh

from model.environment import _box, _color, _cyl

MECH_Y = -0.38
MECH_Z = 0.78
PINE = [218, 182, 132, 255]
PINE_DARK = [194, 156, 106, 255]


def create_grill_clamp_bracket():
    """Space-gray anodized aluminum split-clamp bracket mounted onto the window grill bar."""
    alu, steel, tpu = [64, 70, 82, 255], [215, 220, 228, 255], [32, 35, 40, 255]
    parts = [
        _box([0.012, 0.068, 0.068], [-0.212, MECH_Y, MECH_Z], alu),
        _box([0.012, 0.068, 0.068], [-0.188, MECH_Y, MECH_Z], alu),
        _box([0.014, 0.062, 0.062], [-0.200, MECH_Y, MECH_Z], tpu),
        _box([0.030, 0.008, 0.032], [-0.172, MECH_Y - 0.012, MECH_Z], alu),
        _box([0.030, 0.008, 0.032], [-0.172, MECH_Y + 0.012, MECH_Z], alu),
        _cyl(0.005, 0.038, [-0.165, MECH_Y, MECH_Z], steel, axis="y", sections=28),
    ]
    bolts = [_cyl(0.0035, 0.036, [-0.20, MECH_Y + dy, MECH_Z + dz], steel, axis="x") for dy in (-0.022, 0.022) for dz in (-0.022, 0.022)]
    return trimesh.util.concatenate(parts + bolts)


def create_actuator():
    """Horizontal 12V linear actuator bridging window grill (X=-0.165) to crib left rail (X=+0.005)."""
    alu, cap, rod = [216, 220, 228, 255], [54, 60, 70, 255], [242, 245, 250, 255]
    return trimesh.util.concatenate([
        _cyl(0.018, 0.105, [-0.110, MECH_Y, MECH_Z], alu, axis="x", sections=48),
        _cyl(0.015, 0.068, [-0.128, MECH_Y, MECH_Z - 0.028], cap, axis="x", sections=40),
        _box([0.026, 0.032, 0.052], [-0.155, MECH_Y, MECH_Z - 0.014], cap),
        _cyl(0.009, 0.014, [-0.165, MECH_Y, MECH_Z], cap, axis="y", sections=32),
        _cyl(0.019, 0.010, [-0.056, MECH_Y, MECH_Z], cap, axis="x", sections=48),
        _cyl(0.008, 0.065, [-0.024, MECH_Y, MECH_Z], rod, axis="x", sections=36),
        _cyl(0.009, 0.014, [0.005, MECH_Y, MECH_Z], alu, axis="y", sections=32),
    ])


def create_crib_rail_clamp():
    """Felt-lined wood-safe clamp bracket on the crib's left top rail at X=+0.02m."""
    alu, felt, steel = [64, 70, 82, 255], [96, 104, 114, 255], [215, 220, 228, 255]
    return trimesh.util.concatenate([
        _box([0.040, 0.068, 0.056], [0.020, MECH_Y, MECH_Z], alu),
        _box([0.032, 0.070, 0.048], [0.020, MECH_Y, MECH_Z], felt),
        _box([0.024, 0.007, 0.028], [0.005, MECH_Y - 0.011, MECH_Z], alu),
        _box([0.024, 0.007, 0.028], [0.005, MECH_Y + 0.011, MECH_Z], alu),
        _cyl(0.005, 0.034, [0.005, MECH_Y, MECH_Z], steel, axis="y", sections=28),
    ])


def create_controller_enclosure():
    """Apple-style matte white ESP32 + driver enclosure sitting on the window sill."""
    return trimesh.util.concatenate([
        _box([0.085, 0.115, 0.042], [-0.25, -0.48, 0.753], [244, 246, 250, 255]),
        _box([0.079, 0.109, 0.006], [-0.25, -0.48, 0.776], [224, 228, 236, 255]),
        _cyl(0.014, 0.012, [-0.25, -0.50, 0.783], [225, 48, 48, 255], axis="z", sections=32),
        _cyl(0.005, 0.004, [-0.25, -0.45, 0.780], [46, 204, 113, 255], axis="z", sections=24),
    ])


def _parabolic_arc(xs, y_pos, z_base, coeff, width_y, height_z, rgba):
    """Build a curved wooden beam along X at fixed Y using a parabolic profile."""
    segs = []
    for i in range(len(xs) - 1):
        x0, x1 = float(xs[i]), float(xs[i + 1])
        xm = 0.5 * (x0 + x1)
        zm = z_base + coeff * (xm - 0.34) ** 2
        dz = coeff * ((x1 - 0.34) ** 2 - (x0 - 0.34) ** 2)
        dx = x1 - x0
        seg = trimesh.creation.box(extents=[float(np.hypot(dx, dz)) + 0.005, width_y, height_z])
        seg.apply_transform(trimesh.transformations.rotation_matrix(-float(np.arctan2(dz, dx)), [0, 1, 0]))
        seg.apply_translation([xm, y_pos, zm])
        segs.append(_color(seg, rgba))
    return segs


def _crib_end_panels():
    """Front footboard (Y=-0.56) and back headboard (Y=+0.56) with rockers, posts, slats, and arch."""
    meshes = [_box([0.64, 0.022, 0.52], [0.34, -0.59, 0.44], PINE)]
    for y_end in (-0.56, 0.56):
        meshes.extend(_parabolic_arc(np.linspace(-0.03, 0.71, 25), y_end, 0.015, 0.52, 0.028, 0.034, PINE_DARK))
        meshes.extend(_parabolic_arc(np.linspace(0.00, 0.68, 17), y_end, 0.94, -0.85, 0.028, 0.060, PINE_DARK))
        meshes.append(_box([0.62, 0.020, 0.28], [0.34, y_end, 0.34], PINE))
        meshes.extend([_box([0.036, 0.036, 0.84], [xp, y_end, 0.48], PINE) for xp in (0.02, 0.66)])
        meshes.extend([_box([0.030, 0.014, 0.34], [float(xs), y_end, 0.66], PINE) for xs in np.linspace(0.10, 0.58, 6)])
    return meshes


def _crib_sides_and_bedding():
    """Left/right side rails, vertical slats, mattress, and pastel patchwork bumpers."""
    pink, blue = [236, 206, 214, 255], [204, 216, 232, 255]
    meshes = [_box([0.60, 1.08, 0.08], [0.34, 0.0, 0.28], [232, 230, 225, 255]), _box([0.18, 0.75, 0.04], [0.16, -0.10, 0.33], [242, 168, 188, 255])]
    for x_s in (0.02, 0.66):
        meshes.extend([_box([0.026, 1.10, 0.036], [x_s, 0.0, 0.24], PINE_DARK), _box([0.028, 1.10, 0.042], [x_s, 0.0, 0.78], PINE_DARK)])
        meshes.extend([_box([0.014, 0.026, 0.52], [x_s, float(ys), 0.51], PINE) for ys in np.linspace(-0.48, 0.48, 13)])
    for i, yp in enumerate(np.linspace(-0.44, 0.44, 8)):
        c = pink if i % 2 == 0 else blue
        meshes.extend([_box([0.035, 0.12, 0.26], [0.052, float(yp), 0.48], c), _box([0.035, 0.12, 0.26], [0.628, float(yp), 0.48], c)])
    meshes.extend([_box([0.11, 0.035, 0.26], [float(xp), 0.525, 0.48], blue if i % 2 == 0 else pink) for i, xp in enumerate(np.linspace(0.10, 0.58, 5))])
    return meshes


def create_crib_frame_section():
    """HunyHuny pinewood cot next to window: arched ends, drop footboard panel, patchwork bumpers, mattress & rockers."""
    return trimesh.util.concatenate(_crib_end_panels() + _crib_sides_and_bedding())


def create_window_grill_section():
    """Black metal grid window grill anchored into the window sill at X = -0.20m."""
    blk = [38, 42, 48, 255]
    v_bars = [_cyl(0.007, 0.70, [-0.20, yb, 1.07], blk, axis="z", sections=24) for yb in (-0.38, -0.02, 0.34)]
    h_bars = [_box([0.012, 0.96, 0.012], [-0.20, -0.10, zb], blk) for zb in (0.78, 0.96, 1.14, 1.32)]
    window = [_box([0.035, 0.98, 0.72], [-0.32, -0.10, 1.08], [228, 224, 212, 255]), _box([0.008, 0.90, 0.64], [-0.30, -0.10, 1.08], [188, 204, 214, 255])]
    return trimesh.util.concatenate(v_bars + h_bars + window)
