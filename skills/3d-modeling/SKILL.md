---
name: 3d-modeling
description: "Create 3D models for hardware projects using Python and trimesh. Use when designing parts, mechanisms, or assemblies for fabrication or 3D printing."
---

# 3D Modeling for Hardware Projects

## When to Use

- Designing custom brackets, mounts, or enclosures
- Creating assemblies to check fit and clearances
- Generating STL files for 3D printing
- Exporting GLB for web viewing or documentation

## Tools

- **trimesh** — Python library for 3D geometry
- **numpy** — numerical operations
- **STL** — standard 3D printing format
- **GLB** — web-friendly 3D format

## Setup

```bash
cd /Users/pbd/personal/hw
source .venv/bin/activate
```

## Workflow

1. **Design principles** — Apple-inspired: rounded edges, clean lines, minimal visible fasteners
2. **Create parts** — each part as a separate function
3. **Export individual parts** — STL for 3D printing
4. **Export assembly** — STL + GLB for visualization

## Example

```python
import trimesh
import numpy as np

def create_bracket():
    """Create a mounting bracket."""
    plate = trimesh.creation.box(extents=[0.06, 0.015, 0.08])
    plate.apply_translation([0, 0, 0.04])
    return plate

bracket = create_bracket()
bracket.export("bracket.stl")
```

## File Structure

```
projects/<project>/3d/
├── generate_model.py    # Main generation script
├── *.stl               # Individual parts
├── *-assembly.stl      # Assembled scene
└── *-assembly.glb      # Web-viewable format
```

## Design Guidelines

- Use rounded edges (radius 0.002–0.005) for premium look
- Keep proportions realistic (mm scale)
- Use smooth curves (torus, cylinder) over sharp boxes
- Export at 48+ sections for smooth surfaces
- Name parts descriptively: `u_bolt_bracket.stl`, `l_bracket.stl`

## Rotation in Trimesh

```python
# Correct way to rotate in trimesh
rot = trimesh.transformations.rotation_matrix(angle, [x, y, z])
mesh.apply_transform(rot)
```

## Resources

- [trimesh docs](https://trimsh.org/)
- [STL format](https://en.wikipedia.org/wiki/STL_(file_format))
