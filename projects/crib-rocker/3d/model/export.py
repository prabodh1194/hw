"""Export functions for crib rocker model."""

import trimesh
from pathlib import Path

OUT_DIR = Path(__file__).parent.parent


def export_parts(parts):
    """Export individual parts as STL."""
    for name, mesh in parts.items():
        path = OUT_DIR / f"{name}.stl"
        mesh.export(path)
        print(f"Exported: {path}")


def export_assembly(parts):
    """Export assembled scene as STL and GLB."""
    scene = trimesh.util.concatenate(list(parts.values()))
    stl_path = OUT_DIR / "crib-rocker-assembly.stl"
    scene.export(stl_path)
    print(f"Exported: {stl_path}")
    glb_path = OUT_DIR / "crib-rocker-assembly.glb"
    scene.export(glb_path)
    print(f"Exported: {glb_path}")
