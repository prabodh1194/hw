# HW — Hardware Hobby Dev

Monorepo for hardware projects. Built for learning, prototyping, and tinkering.

## Projects

| Project | Description | Status |
|---------|-------------|--------|
| [crib-rocker](projects/crib-rocker/) | Motorized crib rocker using 12V linear actuator | Planning |

## Structure

```
hw/
├── projects/          # Individual hardware projects
│   └── <project>/
│       ├── spec.md    # ASD-STE100 specification
│       ├── 3d/        # 3D models (STL, STEP, OpenSCAD)
│       ├── firmware/  # Microcontroller code
│       ├── electronics/ # Schematics, wiring diagrams
│       └── docs/      # Build logs, photos, notes
├── shared/            # Shared resources
│   ├── parts/         # Common parts library
│   ├── libraries/     # Reusable code/firmware
│   └── tools/         # Build and test tools
├── templates/         # Project templates
└── scripts/           # Build/compile scripts
```

## How to Add a Project

1. Copy `templates/project-template/` to `projects/<name>/`
2. Write a spec in ASD-STE100 format
3. Add 3D models, firmware, and electronics
4. Update the project table above

## Tools

- **3D Modeling:** OpenSCAD, CadQuery
- **Firmware:** Arduino IDE, PlatformIO
- **Electronics:** KiCad, Fritzing
- **Docs:** Markdown, ASD-STE100

## License

MIT — use freely, modify freely.
