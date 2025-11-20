# 📐 Construction Plans - 2D Drawings

## Contents

This directory contains 2D technical drawings for manual construction if 3D printing is not available.

```
plans/
├── hull_profile.pdf        # Side view with dimensions
├── hull_sections.pdf       # Cross-sections every 10 cm
├── hull_plan_view.pdf      # Top view (deck layout)
├── electrical_diagram.pdf  # Wiring schematic
├── assembly_instructions.pdf
└── cutting_templates/      # Full-scale printable templates
    ├── frame_1.pdf
    ├── frame_2.pdf
    └── frame_3.pdf
```

## Drawing Standards

- **Scale**: 1:1 for cutting templates, 1:5 for assembly views
- **Dimensions**: All in millimeters
- **Tolerances**: ±2 mm for structural, ±0.5 mm for motor mounts
- **Material thickness**: Clearly labeled (e.g., "5mm plywood")

## Construction Methods

### Method 1: Plank-on-Frame
1. Cut frame templates from plans
2. Transfer to 5mm plywood
3. Assemble frames on building jig
4. Attach 2mm plywood planking
5. Seal with fiberglass cloth + epoxy

### Method 2: 3D Printing (Recommended)
1. Export STL from CAD
2. Slice at 0.2mm layer height, 30% infill
3. Print in sections if hull > print bed
4. Join sections with epoxy
5. Sand and waterproof

### Method 3: Foam Core
1. Cut foam blocks to rough shape
2. Carve with hot wire cutter following templates
3. Cover with fiberglass cloth (2 layers)
4. Apply epoxy resin
5. Sand smooth

## Electrical Schematic Components

### Power Distribution
```
Battery 12V ─┬─> L298N VIN
             ├─> ESP32 (via 5V regulator)
             └─> Power monitoring (INA219)

L298N ─┬─> Motor A (Left)
       └─> Motor B (Right)

ESP32 GPIO:
  18, 17 -> Motor A direction (IN1, IN2)
  16, 4  -> Motor B direction (IN3, IN4)
  2, 15  -> PWM enable (ENA, ENB)
```

### Connections Table
| Component | Pin | Wire to | Notes |
|-----------|-----|---------|-------|
| ESP32 GND | GND | L298N GND, Battery - | Common ground critical |
| ESP32 5V | 5V | Buck converter output | Do not connect to 12V! |
| L298N IN1 | - | ESP32 GPIO 18 | Motor A Dir 1 |
| L298N IN2 | - | ESP32 GPIO 17 | Motor A Dir 2 |
| L298N IN3 | - | ESP32 GPIO 16 | Motor B Dir 1 |
| L298N IN4 | - | ESP32 GPIO 4 | Motor B Dir 2 |
| L298N ENA | - | ESP32 GPIO 2 | PWM Motor A |
| L298N ENB | - | ESP32 GPIO 15 | PWM Motor B |
| L298N OUT1/2 | - | Motor A terminals | Left motor |
| L298N OUT3/4 | - | Motor B terminals | Right motor |
| L298N +12V | - | Battery + | Motor power |
| L298N GND | - | Battery - | Power ground |

## Assembly Sequence

1. **Hull Construction** (Day 1-2)
   - Build or print hull
   - Waterproof test (submerge 24h)
   - Drill motor mount holes

2. **Motor Installation** (Day 3)
   - Attach motors to mounts
   - Install propellers
   - Seal shaft penetrations

3. **Electronics Mounting** (Day 4)
   - Install waterproof box for ESP32
   - Mount L298N in ventilated area
   - Route wires through conduits

4. **Wiring** (Day 5)
   - Follow electrical schematic
   - Use heat shrink tubing on all connections
   - Test continuity with multimeter

5. **Testing** (Day 6)
   - Upload ESP32 code
   - Test motors individually
   - Calibrate PWM ranges
   - Buoyancy test with ballast

6. **Final Integration** (Day 7)
   - Add cargo platform
   - Balance center of gravity
   - Seal all access panels
   - Full system test

## Safety Checklist

- [ ] All battery connections have inline fuse (3A)
- [ ] Electronics in waterproof enclosure (IP65+)
- [ ] Motor wires secured away from propellers
- [ ] Propellers have guards to prevent injury
- [ ] Emergency stop accessible (parar command)
- [ ] Battery voltage monitoring to prevent over-discharge
- [ ] Hull has flotation foam in case of leak
- [ ] Lost communication triggers auto-stop (ESP32 watchdog)

## Bill of Materials (BOM)

See `informe/informe_barcaza.tex` Table V for complete list with costs.

## Contact for Questions

- Course instructor: [Professor name]
- Lab support: [Lab email]
- Project repository: https://github.com/DanielAraqueStudios/Fluids-Mechanics-RC-Ship
