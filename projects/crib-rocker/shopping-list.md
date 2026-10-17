# Crib Rocker Shopping List (Amazon.in / Robu.in)

Sized specifically for the **20 cm gap** between the recessed window grill (`X = -20 cm, Z = 78 cm`) and the HunyHuny pinewood crib rail (`X = +2 cm, Z = 78 cm`).

## 1. Actuation & Motion

| # | Part | Exact Specification | Qty | Est. Price (INR) | Where to Buy (Amazon.in / Robu.in Search) |
|---|------|---------------------|-----|------------------|-------------------------------------------|
| 1 | **12V Mini Linear Actuator (50 mm / 2" Stroke)** | 12V DC, **50 mm (2 inch) stroke**, 15 mm/s speed, 60N–100N force, built-in limit switches, clevis ends (`~155 mm` retracted → `205 mm` extended, fits the `200 mm` grill-to-crib gap directly) | 1 | ₹1,650 | Amazon.in / Robu.in: `"12V 50mm stroke micro linear actuator with bracket"` |
| 2 | **Clevis Pivot Pins + R-Clips (6 mm)** | 6 mm × 30 mm stainless steel clevis pins with retaining clips (usually included with actuator bracket kit) | 2 | ₹150 | Included with actuator bracket set or `"M6 clevis pin with R clip"` |

## 2. Electronics & Control (Fits Inside Windowsill Pod)

| # | Part | Exact Specification | Qty | Est. Price (INR) | Where to Buy (Amazon.in / Robu.in Search) |
|---|------|---------------------|-----|------------------|-------------------------------------------|
| 3 | **ESP32 DevKit V1 (30-pin USB-C / Micro-USB)** | ESP-WROOM-32 development board (runs 20 kHz silent half-sine PWM firmware) | 1 | ₹380 | Amazon.in / Robu.in: `"ESP32 DevKit V1 30 pin"` |
| 4 | **BTS7960 (IBT-2) 43A H-Bridge Motor Driver** *(preferred over L298N for silent 20 kHz PWM & cool running)* | Dual BTS7960B half-bridge module, 5.5V–27V, supports 20 kHz ultrasonic PWM without audible whine | 1 | ₹260 | Amazon.in / Robu.in: `"BTS7960 43A motor driver module"` |
| 5 | **LM2596 DC-DC Buck Converter (12V → 5V)** | Input 4–35V, Output 1.23–30V (set to 5.0V for ESP32 VIN), 2A | 1 | ₹95 | Amazon.in / Robu.in: `"LM2596 buck converter module"` |
| 6 | **12V 3A DC Power Adapter (5.5 × 2.1 mm)** | 100–240V AC input, 12V 3A regulated DC output + screw terminal barrel jack adapter | 1 | ₹420 | Amazon.in: `"12V 3A DC power supply adapter 5.5x2.1mm"` |
| 7 | **16 mm Latching Emergency-Stop Push Button** | Red mushroom/flush push button with green LED ring (mounts on top lid of windowsill pod) | 1 | ₹140 | Amazon.in: `"16mm latching push button switch LED"` |
| 8 | **ABS Project Enclosure Box (115 × 90 × 55 mm)** | Matte white/light grey ABS enclosure for windowsill controller pod | 1 | ₹190 | Amazon.in: `"115x90x55mm white ABS junction box enclosure"` |

## 3. Non-Marring Mounting Hardware (No Drilling into Crib or Grill)

| # | Part | Exact Specification | Qty | Est. Price (INR) | Where to Buy (Amazon.in / Local Hardware) |
|---|------|---------------------|-----|------------------|-------------------------------------------|
| 9 | **Square U-Bolt Clamp Set (M6 × 25 mm × 50 mm)** | Stainless steel square U-bolts with backing plates & nyloc nuts (clamps onto the 12 mm black window grill bar) | 2 | ₹240 | Amazon.in: `"M6 square U bolt clamp 25mm"` |
| 10 | **Padded Pipe/Rail Saddle Clamp or L-Brackets** | 30 mm padded U-channel clamp + 3 mm adhesive felt/rubber strip (wraps the 26 mm pinewood crib top rail without scratching wood) | 1 set | ₹220 | Amazon.in: `"3mm self adhesive felt furniture pad strip"` + `"M6 L bracket heavy duty"` |
| 11 | **M4 & M6 Stainless Fastener Assortment + Dupont Wires** | M4/M6 bolts, nyloc nuts, washers + 20 cm female-to-female jumper wires + 18 AWG 2-core cable (1.5 m) | 1 | ₹280 | Amazon.in: `"M4 M6 stainless nut bolt assortment"` + `"Dupont jumper wires"` |

---

**Estimated Total:** **~₹4,025 INR** (all off-the-shelf components, zero custom machining required; optional 3D-printed brackets in `projects/crib-rocker/3d/*.stl`).
