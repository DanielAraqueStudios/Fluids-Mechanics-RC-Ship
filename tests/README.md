# 🧪 Test Data and Analysis

## Test Protocol

### Pre-Test Checklist
- [ ] Hull waterproof test completed (24h submersion)
- [ ] All connections secured with heat shrink tubing
- [ ] Battery fully charged (12V > 11.5V at rest)
- [ ] ESP32 communication tested (MAC addresses configured)
- [ ] Motors respond to all commands (w, s, a, d, p)
- [ ] Cargo secured and centered
- [ ] Emergency stop procedure reviewed

### Test 1: Stability and Load Capacity

**Objective**: Verify heel angle ≤ 10° up to 2.5 kg cargo

**Procedure**:
1. Float hull in calm water without cargo
2. Measure initial draft with ruler
3. Add cargo in 0.5 kg increments
4. Measure draft and heel angle at each load
5. Record maximum stable load

**Data to collect**:
- Cargo mass (kg)
- Draft port/starboard (cm)
- Heel angle (degrees, use smartphone inclinometer)
- Photos of waterline at each load

**Template**: `stability_test.csv`

### Test 2: Efficiency and Transport Index (IT)

**Objective**: Measure IT = (m_cargo × D) / (t × E)

**Procedure**:
1. Load barge with 1.5 kg cargo (minimum requirement)
2. Position at start line (0 m mark)
3. Start data logging (voltage, current, time)
4. Command ADELANTE @ PWM 200
5. Record time to reach 20 m
6. Turn around manually or via commands
7. Return to start position
8. Stop logging
9. Calculate energy: E = ∫V(t)·I(t)dt in Wh

**Data to collect** (10 Hz sampling recommended):
- Timestamp (s)
- Velocity (m/s, from position derivative or GPS)
- Current (A, from INA219 or multimeter)
- Voltage (V, from INA219 or multimeter)
- Position (m, manual markers or GPS)
- Command sent
- PWM value

**Template**: `test_template.csv`

### Test 3: Power Consumption vs Velocity

**Objective**: Validate ITTC resistance calculations

**Procedure**:
1. Load barge with fixed cargo (1.5 kg)
2. For PWM = [100, 150, 200, 255]:
   - Accelerate to steady velocity
   - Measure velocity over 10 m (stopwatch + markers)
   - Record voltage and current for 10 seconds
   - Calculate average power
3. Plot P vs V, compare with `simulations/resistance_calc.py`

**Template**: `power_velocity_test.csv`

## Data Analysis Scripts

### Calculate Transport Index
```python
import pandas as pd

data = pd.read_csv('test_run_2024-11-20.csv')

# Calculate energy (trapezoidal integration)
dt = data['timestamp'].diff()
power = data['voltage_V'] * data['current_A']
energy_J = (power * dt).sum()
energy_Wh = energy_J / 3600

# Calculate IT
m_cargo = 1.5  # kg
distance = data['position_m'].max()  # meters
time = data['timestamp'].max()  # seconds

IT = (m_cargo * distance) / (time * energy_Wh)
print(f"Transport Index: {IT:.2f} kg·m/(s·Wh)")
```

### Compare Measured vs Predicted Resistance
```python
import sys
sys.path.append('../simulations')
from resistance_calc import ITTCResistanceCalculator, HullParameters, FluidProperties

# Measured data
V_measured = 0.47  # m/s average
P_measured = 11.8 * 0.65  # W average

# Calculate from theory
hull = HullParameters(length=0.45, wetted_area=0.18)
calc = ITTCResistanceCalculator(hull, FluidProperties())
result = calc.calculate_resistance(V_measured)

print(f"Measured Power: {P_measured:.3f} W")
print(f"Predicted Power (η=50%): {result.effective_power / 0.5:.3f} W")
print(f"Error: {abs(P_measured - result.effective_power/0.5) / P_measured * 100:.1f}%")
```

## Test Results Repository

Store completed test files with naming convention:
```
test_YYYY-MM-DD_HHmm_condition.csv
```

Example:
- `test_2024-11-20_1430_cargo1.5kg.csv`
- `test_2024-11-21_0900_cargo2.5kg.csv`
- `test_2024-11-21_1500_no_cargo_baseline.csv`

## Video Synchronization

Record video with:
- Timestamp overlay (use smartphone app)
- Clear view of barge position
- Speed markers visible in frame

Sync video with CSV data using timestamp alignment for post-analysis.

## Safety Notes

⚠️ **Do not test in**:
- Water with currents > 0.1 m/s
- Wind > 10 km/h
- Water depth < 0.5 m
- Areas with boat traffic

🛟 **Emergency procedures**:
- Have retrieval pole ready (3m minimum)
- Life jacket for operator near deep water
- Waterproof phone/radio for communication
- First aid kit on site

## Expected Results

Based on design calculations:

| Test | Target | Minimum Pass |
|------|--------|--------------|
| Stability @ 2.5kg | Heel < 6° | Heel < 10° |
| IT @ 1.5kg | IT > 350 | IT > 200 |
| Velocity @ 200 PWM | 0.47 m/s | 0.40 m/s |
| Power @ 0.5 m/s | < 10 W | < 15 W |
| Range (single battery) | > 500 m | > 200 m |

## Reporting

Include in final report:
1. All raw CSV files (zipped)
2. Summary statistics table
3. Comparison plots (measured vs predicted)
4. Photos of test setup
5. Video links (uploaded to cloud)
6. Lessons learned and improvements
