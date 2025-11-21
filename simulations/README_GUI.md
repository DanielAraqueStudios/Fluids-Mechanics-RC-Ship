# 🚢 RC Cargo Barge - Analysis Dashboard

**Professional Dark Mode UI/UX for Comprehensive Hydrodynamic Analysis**

Universidad Militar Nueva Granada | Fluid Mechanics Project

---

## 📋 Features

### ✨ **Professional Interface**
- 🌙 **Dark Mode Design**: Easy on the eyes, professional appearance
- 📊 **Tabbed Navigation**: Organized workflow across 5 sections
- 🎨 **Real-time Visualization**: Interactive matplotlib plots
- 📈 **Progress Tracking**: Live status updates during calculations

### 🔬 **Analysis Modules**

#### 1️⃣ **Parameters Tab**
- Input hull geometry (length, beam, height, draft)
- Configure mass distribution (hull, electronics, cargo)
- Set analysis parameters (velocity, form factor)
- Quick action buttons for each analysis type

#### 2️⃣ **Stability Analysis**
- Displacement volume calculation (pyramid + rectangular geometry)
- Center of buoyancy (KB)
- Metacentric radius (BM)
- Metacentric height (GM)
- Flotation check (buoyancy vs. weight forces)
- Visual stability charts

#### 3️⃣ **Resistance Analysis (ITTC-1957)**
- Reynolds number calculation
- Froude number analysis
- Friction coefficient (ITTC-1957 method)
- Total resistance curves
- Power requirements
- Multi-velocity sweep (0.1-1.5 m/s)

#### 4️⃣ **3D Visualization**
- Interactive 3D hull mesh
- Pyramidal bow + rectangular stern geometry
- Exportable high-resolution images
- Rotatable view

#### 5️⃣ **Summary Report**
- Comprehensive analysis results
- Design compliance checklist
- Export to TXT or JSON
- Timestamped reports

---

## 🚀 Installation

### Prerequisites
```bash
# Python 3.9 or higher required
python --version
```

### Install Dependencies
```bash
# Navigate to simulations directory
cd simulations

# Install GUI requirements
pip install -r requirements_gui.txt
```

### Required Packages
- **PyQt6** (≥6.6.0): Modern GUI framework
- **matplotlib** (≥3.8.0): Plotting and visualization
- **numpy** (≥1.24.0): Numerical computations

---

## 💻 Usage

### Launch the Dashboard
```bash
python hull_analysis_gui.py
```

### Quick Start Guide

1. **Set Parameters** (⚙️ Parameters Tab)
   - Review default values (pre-configured for project specs)
   - Modify geometry: L=0.45m, B=0.172m, H=0.156m
   - Adjust mass distribution
   - Set design velocity

2. **Run Analysis**
   - **🔄 Stability**: Calculate GM, flotation status
   - **🌊 Resistance**: ITTC-1957 method for full velocity range
   - **⚡ Complete**: Run all analyses sequentially

3. **View Results**
   - Switch between tabs to see detailed results
   - Interactive plots update automatically
   - Real-time status updates in bottom bar

4. **Export Data**
   - **📄 TXT Report**: Human-readable summary
   - **📊 JSON Data**: Machine-readable for further processing
   - **🖼️ PNG Images**: High-res plots (300 DPI)

---

## 🎯 Default Parameters

### Hull Geometry (Hybrid Design)
```
Total Length:        0.45 m  (5cm bow + 40cm stern)
Beam:                0.172 m
Height:              0.156 m
Bow Length:          0.05 m  (pyramidal section)
Draft:               0.055 m
```

### Mass Distribution
```
Hull (MDF + paint):  1.20 kg
Electronics:         1.00 kg
Cargo:               2.50 kg
TOTAL:               4.70 kg
```

### Analysis Settings
```
Design Velocity:     0.5 m/s
Form Factor (k):     0.2
Wetted Area:         0.165 m² (calculated)
```

---

## 📊 Output Examples

### Stability Results
```
GM = 2.16 cm           ⚠ MARGINAL
KB = 2.69 cm
BM = 4.32 cm
KG = 4.85 cm

Buoyancy Force: 38.67 N ↑
Weight Force:   46.11 N ↓
Status:         ✗ SINKS (requires T=6.56cm)
```

### Resistance @ 0.5 m/s
```
Reynolds:       2.24×10⁵
Froude:         0.238 (displacement mode)
Cf (ITTC):      0.00534
Resistance:     0.165 N
Power:          0.083 W
Shaft Power:    0.218 W (η=0.38)
```

---

## 🎨 UI/UX Features

### Color Scheme
- **Primary**: `#0d7377` (Teal) - Action buttons, highlights
- **Secondary**: `#14a085` (Mint) - Accents, success states
- **Warning**: `#e63946` (Red) - Critical values, errors
- **Background**: `#1e1e1e` (Dark gray) - Main canvas
- **Surface**: `#2b2b2b` (Charcoal) - Cards, inputs

### Typography
- **Headers**: Segoe UI Bold 16pt
- **Body**: Segoe UI Regular 10pt
- **Code**: Consolas Monospace 9pt

### Icons
- ⚙️ Parameters
- ⚖️ Stability
- 🌊 Resistance
- 📐 3D Visualization
- 📊 Summary Report

---

## 🔧 Troubleshooting

### Import Errors
```bash
# If analysis modules not found
cd simulations
python -c "import stability_analysis"
```

### PyQt6 Display Issues
```bash
# Windows: Ensure graphics drivers updated
# Linux: Install Qt dependencies
sudo apt-get install python3-pyqt6 libqt6gui6
```

### Matplotlib Backend
```python
# GUI uses 'Qt5Agg' backend automatically
# If issues persist, check:
import matplotlib
print(matplotlib.get_backend())
```

---

## 📁 File Structure

```
simulations/
├── hull_analysis_gui.py       # Main GUI application
├── requirements_gui.txt        # GUI dependencies
├── stability_analysis.py       # Stability calculations
├── resistance_calc.py          # ITTC-1957 resistance
├── visualize_hull_3d.py        # 3D mesh generation
├── run_all_analysis.py         # CLI batch runner
└── analysis_results/           # Output directory
    ├── *.png                   # Generated plots
    ├── *.txt                   # Text reports
    └── *.json                  # Data exports
```

---

## 🎓 Project Context

**Course**: Mecánica de Fluidos  
**Institution**: Universidad Militar Nueva Granada  
**Program**: Ingeniería Mecatrónica  
**Method**: ITTC-1957 Standard for Model-Scale Vessels

### Design Constraints
- Length: 0.35-0.60 m ✓
- Draft: < 6 cm ⚠
- Cargo: ≥ 1.5 kg ✓
- Power: < 75 W ✓
- Heel: < 10° @ max load ⚠

### Key Innovations
- **Hybrid Hull**: Pyramidal bow + rectangular stern
- **Real-time Analysis**: Instant feedback on design changes
- **ESP32 Control**: Wireless telemetry integration ready
- **Professional Tools**: Industry-standard ITTC method

---

## 🤝 Contributing

### Team Members
- Sebastián Andrés Rodríguez Carrillo
- David Andrés Rodríguez Rozo
- Daniel Garcia Araque
- Julián Andrés Rosas

### Development
```bash
# Clone repository
git clone [repository-url]

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements_gui.txt

# Run tests
python -m pytest tests/
```

---

## 📝 License

Educational Project - Universidad Militar Nueva Granada

---

## 🔗 References

1. **ITTC (2017)**: *Recommended Procedures and Guidelines: 1978 ITTC Performance Prediction Method*
2. **Molland et al. (2011)**: *Ship Resistance and Propulsion*, Cambridge University Press
3. **Rawson & Tupper (2001)**: *Basic Ship Theory*, Butterworth-Heinemann
4. **Espressif (2023)**: *ESP-NOW User Guide*, ESP32 Documentation

---

## 📧 Contact

For questions or issues:
- Open an issue on GitHub
- Contact team members via university email

---

**Version**: 1.0.0  
**Last Updated**: November 20, 2025  
**Status**: ✅ Production Ready

🚢 **Happy Analyzing!** 🌊
