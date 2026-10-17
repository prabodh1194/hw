# Step-by-Step Assembly Guide — HunyHuny Crib Rocker (`CR-001`)

Matches the 6 numbered mechanism components in `projects/crib-rocker/3d/preview.png` and `projects/crib-rocker/3d/assembly-steps.png`.

---

## Exploded Bill of Materials (Mechanism Bridge @ `Y = -38 cm, Z = 78 cm`)

| Callout # | STL File | Component | Mount Location |
|-----------|----------|-----------|----------------|
| **1** | `u_bolt_bracket.stl` | **Grill Split-Clamp Bracket** (with 3 mm TPU/rubber pad + 4× M4 bolts) | Clamps around the vertical/horizontal black window grill bar at `X = -20 cm, Z = 78 cm` |
| **2** | *(6 mm × 35 mm steel pin)* | **Rear Clevis Pivot Pin + R-Clip** | Links Grill Split-Clamp clevis ears (`X = -16.5 cm`) to actuator rear eye |
| **3** | `actuator.stl` | **12V Silent Linear Actuator (50 mm stroke)** | Spans horizontally from `X = -16.5 cm` (window grill) to `X = +0.5 cm` (crib rail) |
| **4** | *(Actuator telescoping rod)* | **Stainless Extension Rod + Front Clevis Pin** | Extends/retracts `±25 mm` horizontally; pinned to Crib Rail Clamp at `X = +0.5 cm` |
| **5** | `l_bracket.stl` | **Felt-Lined Crib Rail Clamp** (no-drill wrap) | Wraps around the HunyHuny crib's left pinewood top rail (`X = +2.0 cm, Z = 78 cm`) |
| **6** | `pivot_pin.stl` | **Windowsill ESP32 + BTS7960 Controller Pod** | Rests on the flat recessed window sill (`X = -25 cm, Y = -48 cm, Z = 72 cm`) |

---

## 4-Stage Assembly Sequence

### Stage 1 — Exploded Sub-Assembly Prep (On the Desk)
1. Line the inside faces of the **Grill Split-Clamp Bracket (#1)** with 2 mm rubber/TPU tape so it grips the painted black grill bar without slipping or scratching.
2. Line the inside U-channel of the **Crib Rail Clamp (#5)** with 3 mm self-adhesive felt pad so the pinewood rail is completely protected.
3. Mount the **ESP32 DevKit**, **BTS7960 H-bridge**, and **LM2596 buck converter (set to 5.00V first!)** inside the **Windowsill Controller Pod (#6)** and wire the 16 mm red E-stop button on the lid.

### Stage 2 — Anchor the Grill Split-Clamp (#1) to the Window Grill
1. Position the HunyHuny crib parallel to the window wall so the left top rail sits **20 cm (`X = +2 cm`)** from the black window grill (`X = -20 cm`) and unlock the crib's bottom curved rockers so it rocks freely side-to-side.
2. Clamp the **Grill Split-Clamp Bracket (#1)** onto the lower-left intersection of the black window grill (`Y = -38 cm, Z = 78 cm`, matching the height of the crib's top side rail).
3. Tighten the 4× M4 hex bolts evenly in an X-pattern until the bracket is rigid.

### Stage 3 — Pin the Linear Actuator (#3) & Crib Rail Clamp (#5)
1. Slide the rear mounting eye of the **12V Linear Actuator (#3)** between the clevis ears of the **Grill Split-Clamp (#1)** and insert the **Rear Clevis Pin (#2)** with its R-clip.
2. Slip the **Felt-Lined Crib Rail Clamp (#5)** over the crib's left top rail directly opposite the actuator (`Y = -38 cm, Z = 78 cm`).
3. With the crib resting at its natural center equilibrium and the actuator rod at mid-stroke (`~25 mm` extended), align the actuator front clevis with the **Crib Rail Clamp (#5)** ears and insert the front clevis pin.
4. Rock the crib gently by hand `±3 cm` left and right to verify the clevis pins pivot smoothly with zero binding.

### Stage 4 — Place Controller Pod (#6) on Window Sill & Wire Up
1. Place the **ESP32 Controller Pod (#6)** on the flat recessed window sill at `X = -25 cm, Y = -48 cm, Z = 72 cm`.
2. Connect the 2-core actuator motor cable to `M+` / `M-` on the BTS7960 driver inside the pod:
   - `12V 3A PSU (+ / -)` → `BTS7960 B+ / B-` and `LM2596 IN+ / IN-`
   - `LM2596 OUT+ (5.0V)` → `ESP32 5V (VIN)` and `BTS7960 VCC / R_EN / L_EN`
   - `ESP32 GPIO 16` → `BTS7960 RPWM` (Extend)
   - `ESP32 GPIO 17` → `BTS7960 LPWM` (Retract)
   - `ESP32 GPIO 4` → `E-Stop Button` → `GND`
3. Plug in the 12V adapter; the ESP32 ramps the actuator with a 20 kHz ultrasonic half-sine velocity profile (`projects/crib-rocker/firmware/crib_rocker.ino`) for silent, jerk-free rocking.
