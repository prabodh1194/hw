---
name: 3d-modeling
description: "Build photo-calibrated 3D hardware mock models, globally depth-sorted 4-view labeled engineering sheets (preview.png), exploded assembly guides (assembly-steps.png), printable STL/GLB bundles, and interactive Three.js WebGL viewers (preview.html). Use whenever designing hardware mechanisms, brackets, enclosures, or room/fixture layouts."
---

# 3D Hardware Modeling & Interactive Assembly Skill

Turn a real-world photo + hardware concept into:
1. **Printable STL part files** + a **multi-node color GLB assembly**
2. **A 4-panel shaded, globally depth-sorted engineering sheet (`preview.png`)** with non-overlapping 2D margin callouts
3. **A 4-step exploded & sequential assembly sheet (`assembly-steps.png`)**
4. **An interactive Z-up Three.js + CSS2DRenderer web viewer (`preview.html`)** with camera presets, floating 3D labels, explode slider, and live kinematic animation

## Reusable Toolkit

Import helpers from `/Users/pbd/personal/hw/skills/3d-modeling/hw3d.py`:
- `box(extents, center, rgba)` — colored box placed at world coordinates `(x, y, z)`
- `cyl(radius, height, center, rgba, axis="z", sections=40)` — colored cylinder oriented along `x`, `y`, or `z`
- `parabolic_arc(xs, y_pos, z_base, coeff, width_y, height_z, rgba, x_center)` — shallow segmented arc for rockers, arches, or curved brackets (never use a full `torus` when you need a partial arc)
- `export_bundle(parts_dict, out_dir, name)` — exports `<part>.stl`, combined `<name>.stl`, and multi-node `<name>.glb` (preserving node names for animation/explode and per-vertex colors)
- `draw_scene_unified(ax, parts_dict, bounds=None)` — combines all visible triangles across all parts into a **single** `Poly3DCollection` so matplotlib depth-sorts globally (prevents background walls from occluding foreground parts)
- `add_callouts_2d(ax, callouts)` — projects 3D anchor points `(x, y, z)` via `proj3d.proj_transform` into 2D data coordinates and places callout boxes in `axes fraction` margin coordinates `(px, py)` so labels never collide

## Core Rules

1. **Calibrate to the User's Photo First**:
   - Read the reference photo before writing geometry.
   - Establish a single right-handed **Z-up** world coordinate system in meters (`X` left-to-right, `Y` front-to-back, `Z` height above floor).
   - Include surrounding context objects from the photo (window sill, grill bars, curtains, adjacent furniture) so mounting clearances are self-evident.
2. **Never Use Full Toruses for Shallow Arcs**:
   - Use `parabolic_arc(...)` to build shallow segmented arcs with realistic cross-sections.
3. **Preserve Multi-Node Hierarchy & Vertex Colors in GLB**:
   - Export GLB with `trimesh.Scene()` adding each part via `scene.add_geometry(mesh, node_name=name)`.
   - In Three.js, set `new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.48, metalness: 0.15 })` and `THREE.Object3D.DEFAULT_UP.set(0, 0, 1)`.
4. **Always Render Labeled Multi-View Sheets (`preview.png` & `assembly-steps.png`)**:
   - Call `fig.canvas.draw()` before `add_callouts_2d(ax, callouts)` so `ax.get_proj()` is finalized, then inspect the output PNG with `read` to verify zero label overlap.
