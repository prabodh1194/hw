"""Room environment capturing the exact bed/window/crib layout from IMG_2438.jpg."""

import numpy as np
import trimesh


def _color(mesh: trimesh.Trimesh, rgba: list[int]) -> trimesh.Trimesh:
    mesh.visual.vertex_colors = np.tile(np.array(rgba, dtype=np.uint8), (len(mesh.vertices), 1))
    return mesh


def _box(extents, center, rgba):
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(center)
    return _color(m, rgba)


def _cyl(radius, height, center, rgba, axis="z", sections=32):
    m = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    rot_axis = [0, 1, 0] if axis == "x" else ([1, 0, 0] if axis == "y" else None)
    if rot_axis:
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, rot_axis))
    m.apply_translation(center)
    return _color(m, rgba)


def create_floor():
    """Bedroom floor spanning under window wall, crib, foreground desk, and adjacent adult bed."""
    floor = _box([1.85, 1.75, 0.018], [0.42, -0.05, -0.009], [214, 210, 202, 255])
    skirting = _box([0.02, 1.75, 0.075], [-0.17, -0.05, 0.0375], [196, 192, 184, 255])
    return trimesh.util.concatenate([floor, skirting])


def _create_curtain():
    """Yellow/gold pleated curtain hanging between window & crib headboard (Y = +0.20 to +0.66)."""
    folds = []
    for i, y_fold in enumerate(np.linspace(0.20, 0.66, 9)):
        x_off = -0.17 + (0.015 if i % 2 == 0 else -0.010)
        shade = [198, 166, 62, 255] if i % 2 == 0 else [178, 146, 48, 255]
        folds.append(_cyl(0.028, 0.92, [x_off, float(y_fold), 1.02], shade, axis="z", sections=24))
    return folds


def create_wall():
    """Left window wall with recessed sill, back wall, yellow curtain, foreground table & adjacent adult bed."""
    cream, sill = [236, 232, 222, 255], [248, 246, 240, 255]
    meshes = [
        _box([0.20, 1.75, 0.72], [-0.28, -0.05, 0.36], cream),
        _box([0.22, 1.75, 0.025], [-0.28, -0.05, 0.72], sill),
        _box([0.20, 0.34, 0.76], [-0.28, -0.75, 1.10], cream),
        _box([1.85, 0.10, 1.48], [0.42, 0.77, 0.74], cream),
        _box([0.36, 0.42, 0.68], [-0.08, -0.78, 0.34], [232, 234, 230, 255]),
        _box([0.58, 1.50, 0.32], [1.03, 0.02, 0.16], [120, 92, 68, 255]),
        _box([0.56, 1.46, 0.16], [1.03, 0.02, 0.40], [235, 232, 228, 255]),
        _box([0.54, 1.10, 0.04], [1.03, -0.12, 0.49], [210, 218, 226, 255]),
        *_create_curtain(),
    ]
    return trimesh.util.concatenate(meshes)
