# SPECIFICATION: Crib Rocker Actuator System

**Document Number:** CR-001
**Revision:** A
**Date:** 2025-01-27

---

## 1. Scope

This specification describes an actuator system for a baby crib. The system moves the crib in a slow back-and-forth motion. The crib has curved rockers. The system attaches to a fixed window grill.

---

## 2. System Description

The system has five main parts:

1. Linear actuator
2. Motor controller
3. Microcontroller
4. Power supply
5. Mounting hardware

The actuator pushes and pulls the crib frame. The curved rockers change this movement into a rocking motion. The microcontroller controls the actuator speed and direction.

---

## 3. Components

### 3.1 Linear Actuator

| Parameter | Value |
|-----------|-------|
| Type | 12V DC linear actuator |
| Stroke | 150 mm |
| Force | 450 N |
| Speed | 10 mm/s |
| Limit switches | Built-in |

### 3.2 Motor Controller

| Parameter | Value |
|-----------|-------|
| Type | H-bridge driver |
| Maximum current | 2 A |
| Input | PWM speed signal, direction signal |

### 3.3 Microcontroller

| Parameter | Value |
|-----------|-------|
| Type | ESP32 DevKit |
| Power | 5V DC |
| Output | PWM signal, direction signal |

### 3.4 Power Supply

| Parameter | Value |
|-----------|-------|
| Input | 100-240V AC |
| Output | 12V DC, 3 A |

### 3.5 Buck Converter

| Parameter | Value |
|-----------|-------|
| Input | 12V DC |
| Output | 5V DC, 1 A |

### 3.6 Mounting Hardware

| Item | Quantity |
|------|----------|
| U-bolts | 2 |
| L-brackets | 2 |
| Screws M4 x 20mm | 8 |
| Washers M4 | 16 |

---

## 4. Installation

### 4.1 Prepare the Crib

- Place the crib next to the window grill.
- Fix the curved rockers to the floor.
- Check that the crib rocks freely.

### 4.2 Install the Actuator

- Attach the U-bolts to the window grill.
- Install the actuator on the U-bolts.
- Tighten the U-bolts.

### 4.3 Connect the Actuator to the Crib

- Attach the L-bracket to the crib frame.
- Connect the actuator rod to the L-bracket.
- Install a pivot pin at the connection.

### 4.4 Install the Electronics

- Connect the actuator to the motor controller.
- Connect the motor controller to the power supply.
- Connect the microcontroller to the motor controller.
- Connect the buck converter to the power supply.
- Connect the buck converter to the microcontroller.

---

## 5. Operation

### 5.1 Start the System

- Connect the power supply to the mains.
- The actuator starts to move.
- The crib starts to rock.

### 5.2 Adjust the Speed

- Open the microcontroller code.
- Change the PWM value.
- Upload the code to the microcontroller.

### 5.3 Stop the System

- Disconnect the power supply from the mains.

---

## 6. Safety

### 6.1 Emergency Stop

- Install a power switch on the mains cable.
- The switch must be within reach of the operator.

### 6.2 Pinch Protection

- Install guards on the actuator joints.
- Keep fingers away from moving parts.

### 6.3 Electrical Safety

- Keep all connections away from water.
- Use insulated connectors.

### 6.4 Mechanical Safety

- Check all bolts before operation.
- Do not exceed the actuator force limit.

---

## 7. Maintenance

### 7.1 Monthly Check

- Check all bolts for tightness.
- Check the actuator for wear.
- Check the wiring for damage.

### 7.2 Lubrication

- Apply silicone spray to the actuator rod.
- Do not use oil-based lubricants.

---

## 8. Wiring Diagram

```
12V Power Supply ──→ L298N (VCC, GND)
                      │
                      ├──→ OUT1 ──→ Actuator +
                      └──→ OUT2 ──→ Actuator −

ESP32 GPIO 16 ──→ IN1 (PWM speed)
ESP32 GPIO 17 ──→ IN2 (direction)
ESP32 GND ──→ L298N GND

Buck Converter 12V→5V ──→ ESP32 5V
```

---

## 9. Reference Diagram

```
Side View:

    Window Grill (fixed)
         │
    ┌────┴────┐
    │ Actuator│  ← U-bolt to grill
    │         │
    │  ┌───┐  │
    │  │   │  │  ← rod extends/retracts
    └──┤   ├──┘
       └─┬─┘
         │
    ┌────┴────┐
    │  Crib   │  ← L-bracket to crib frame
    │  Frame  │
    └────┬────┘
         │
    ╭────┴────╮
    │ Curved  │  ← fixed to floor
    │ Rocker  │
    ╰─────────╯
```

---

**END OF SPECIFICATION**
