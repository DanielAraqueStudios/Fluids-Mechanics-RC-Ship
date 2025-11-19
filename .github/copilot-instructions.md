# Copilot Instructions: RC Cargo Barge - Fluid Mechanics Project

## Project Overview
This is a mechatronics engineering project for a Fluid Mechanics course at Universidad Militar Nueva Granada. The goal is to design, build, and test a scale RC cargo barge that optimizes hydrodynamic performance and energy efficiency.

## Design Constraints
- **Length (L)**: 0.35 - 0.60 m
- **Propulsion**: Electric only (max 75W), sealed batteries
- **Minimum payload**: 1.5 kg (target ≥ 2.5 kg)
- **Maximum draft**: 6 cm
- **Stability**: Heel angle ≤ 10° at maximum load
- **Test course**: 20 m canal with round-trip efficiency test

## Core Calculations (ITTC Method)

### Reynolds Number and Friction Coefficient
```python
Re = (V * L) / nu  # nu = kinematic viscosity of water (m²/s)
Cf = 0.075 / (log10(Re) - 2)**2  # ITTC-1957
```

### Resistance Components
```python
Rf = 0.5 * rho * V**2 * S * Cf  # Friction resistance
Rv = (1 + k) * Rf  # Viscous resistance (k = 0.1-0.3 form factor)
RT = Rv + Rw + Ra  # Total resistance (waves + air)
Fr = V / sqrt(g * L)  # Froude number for wave resistance
```

### Power Requirements
```python
PE = RT * V  # Effective power (W)
P_shaft = PE / eta_T  # Shaft power (eta_T = 0.4-0.6 total efficiency)
```

## Performance Metric
**Transport Index (IT)**: Used for ranking performance
```
IT = (m_cargo × D) / (t × E)
```
- `m_cargo`: cargo mass (kg)
- `D`: distance (m)
- `t`: time (s)
- `E`: energy consumed (Wh)

**Maximize IT by**: reducing resistance, optimizing propeller efficiency, minimizing weight.

## Project Structure Conventions

### CAD Files
- Store hull designs in `/cad/` with versioning (e.g., `hull_v1.step`, `hull_v2.stl`)
- Include waterline analysis and center of buoyancy calculations
- Export 2D plans for construction in `/plans/`

### Simulation Code
- `/simulations/` for hydrodynamic calculations
- Use SI units consistently: meters, kg, seconds, Newtons, Watts
- Validate Reynolds number range (typically 10⁴-10⁶ for this scale)
- Compare Froude numbers: Fr < 0.4 (displacement mode) vs Fr > 0.4 (planing mode)

### Electronics (ESP32 + ESP-NOW Control System)
**Based on**: [2J5R6/ESP32-Boat-Control-ESPNOW-](https://github.com/2J5R6/ESP32-Boat-Control-ESPNOW-)

#### Hardware Setup
- **ESP32-S3** x2: Control (transmitter) + Barco (receiver on barge)
- **L298N** motor driver with dual DC motors (differential steering)
- **Serial commands**: 115200 bps for testing and telemetry
- **Range**: Up to 20m wireless with ESP-NOW protocol

#### Pin Configuration (EspBarco.ino)
```cpp
// Motor A (Left) - GPIO 18,17,2
// Motor B (Right) - GPIO 16,4,15
// PWM: 1kHz, 8-bit resolution (0-255)
```

#### Key Files
- `/EspControl/EspControl.ino`: Transmitter code (command console)
- `/EspBarco/EspBarco.ino`: Receiver code (motor control logic)
- **MAC Configuration**: Must update both files with real MAC addresses (see setup section)

#### Movement Logic
| Command | Left Motor (A) | Right Motor (B) | Result |
|---------|----------------|-----------------|--------|
| ADELANTE | IN1=1, IN2=0 | IN3=1, IN4=0 | Forward |
| ATRAS | IN1=0, IN2=1 | IN3=0, IN4=1 | Reverse |
| IZQUIERDA | IN1=0, IN2=1 | IN3=1, IN4=0 | Turn left |
| DERECHA | IN1=1, IN2=0 | IN3=0, IN4=1 | Turn right |

#### Power Monitoring Integration
- Measure voltage/current at battery terminals for energy calculation
- Log commands + PWM levels + power data synchronized with telemetry
- Target efficiency: `eta_motor * eta_propeller = 0.4-0.6`

### Test Data
- `/tests/` with CSV format: timestamp, velocity, current, voltage, position, command
- Calculate energy: `E = integral(V * I * dt)` in Wh
- Record video synchronized with telemetry and ESP-NOW command logs

## Development Workflow

### Iteration Cycle
1. **Calculate** → Estimate resistance and power for design variants
2. **CAD** → Model hull with accurate wetted surface area
3. **Simulate** → Verify stability (metacentric height, righting moment)
4. **Build** → Waterproof testing is mandatory before electronics installation
5. **Test** → Measure IT and compare with predictions

### ESP32 Setup (Critical First Steps)
```bash
# 1. Get MAC addresses (upload code to each ESP32, check Serial Monitor @ 115200)
# EspControl: Copy MAC shown at startup
# EspBarco: Copy MAC shown at startup

# 2. Update MAC addresses in code
# In EspControl.ino line ~15: uint8_t macBarco[] = {0x98, 0xA3, ...};
# In EspBarco.ino line ~25: uint8_t macControl[] = {0x24, 0x58, ...};

# 3. Re-upload both sketches with correct MACs

# 4. Test communication via Serial Monitor
# Commands: w (forward), s (back), a (left), d (right), p (stop)
# Expected: "[TX] Comando enviado OK" → "[RX] ESTADO DEL BARCO"
```

### Key Commands
```bash
# Python calculations (if using)
python simulations/resistance_calc.py --length 0.45 --velocity 0.5

# Arduino CLI (if batch uploading ESP32 code)
arduino-cli compile --fqbn esp32:esp32:esp32s3 EspControl/
arduino-cli upload -p COM3 --fqbn esp32:esp32:esp32s3 EspControl/

# 3D printing (if applicable)
# Slice STL files at 20-30% infill for buoyancy optimization
```

## Common Patterns

### Hull Optimization
- **Displacement hulls**: Minimize wetted surface area, smooth transitions
- **Form factor k**: Start with 0.2, refine based on hull shape complexity
- **Prismatic coefficient**: Balance cargo volume vs. wave-making resistance
- **Motor placement**: Position motors/propellers to avoid interference with hull flow
- **ESP32 mounting**: Ensure antenna clearance from metal/water for 20m range

### Stability Analysis
- Calculate GM (metacentric height) > 0.05 m for adequate stability
- Use `rho * V_displaced = m_total` for draft prediction
- Test center of gravity position with loaded/unloaded configurations
- **Electronics weight distribution**: Place ESP32 + battery low and centered

### Energy Efficiency
- **Propeller selection**: Match to motor RPM and required thrust
- **Battery sizing**: 12V for motors (via L298N), separate 5V/3.3V for ESP32 (weight trade-off)
- **PWM optimization**: Test velocity settings (0-255) - start at 150-200 for efficiency
- Monitor efficiency: `eta_propeller * eta_motor * eta_controller`
- **L298N modes**: 
  - PWM mode (ENA/ENB to GPIO): Variable speed, better efficiency
  - Failsafe mode (ENA/ENB to 5V direct): Fixed speed, guaranteed operation

### ESP-NOW Communication Patterns
```cpp
// Send command with velocity and timeout
struct_message cmd;
strcpy(cmd.comando, "ADELANTE");
cmd.velocidad = 180;      // PWM 0-255
cmd.tiempo_ms = 2000;     // Duration (0=continuous)
cmd.timestamp = millis(); // For debugging

// Always wait for confirmation callback
// "[RX] ESTADO DEL BARCO" indicates successful receipt
```

## Deliverables Checklist
- [ ] Technical report (8-12 pages) with ITTC calculations
- [ ] CAD models and construction plans (hull + motor mounts)
- [ ] Bill of materials with costs (ESP32-S3 x2, L298N, motors, battery)
- [ ] Test videos with synchronized data (telemetry overlay)
- [ ] Arduino code (EspControl.ino + EspBarco.ino with final MACs)
- [ ] Electrical schematics (ESP32 → L298N → Motors + power distribution)
- [ ] Power monitoring setup documentation (voltage/current sensors if used)
- [ ] A2 poster for presentation

## Troubleshooting ESP32 Issues

### No ESP-NOW Communication
```bash
✅ Verify MACs match in both .ino files
✅ Check Serial Monitor shows "ESP-NOW OK" and "Callback registrado OK"
✅ Distance < 20m, avoid metal obstacles
✅ Test with: mac (show configured MAC), espnow (send test message)
```

### Motors Not Responding
```bash
✅ L298N powered by 12V battery (verify with multimeter)
✅ Common GND between ESP32 and L298N
✅ Test failsafe mode: ENA/ENB → 5V direct (bypasses PWM)
✅ Check IN1-IN4 connections (GPIO 18,17,16,4)
✅ Increase velocity: vel 255 via Serial Monitor
```

### Erratic Movement
```bash
✅ Verify motor polarity (swap OUT1↔OUT2 or OUT3↔OUT4 if reversed)
✅ Check power supply stability under load
✅ Lower PWM frequency if motors vibrate
✅ Balance motor speeds in code if turning biased
```

## Technical Report Structure
Focus sections 4-6 on methodology, construction, and test results. Include:
- Reynolds/Froude number calculations at test velocities
- Wetted surface area measurement method
- Power consumption vs. velocity curves
- Comparison: predicted vs. measured resistance

## Grading Focus (100 pts total)
- **Technical report** (40 pts): Correct ITTC methodology, accurate calculations
- **Practical test** (40 pts): IT index (15 pts), stability (10 pts), compliance (10 pts)
- **Presentation** (20 pts): Technical clarity and data-backed arguments

## References
- ITTC-1957 friction line for model-scale vessels
- Prohaska method for form factor determination
- Standard naval architecture texts for stability calculations
- ESP32 control system: [2J5R6/ESP32-Boat-Control-ESPNOW-](https://github.com/2J5R6/ESP32-Boat-Control-ESPNOW-)
- ESP-NOW protocol documentation: [Espressif ESP-NOW](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/network/esp_now.html)
