# 🚀 QUICK START GUIDE - RC Barge Analysis Dashboard

**Get up and running in 3 minutes!**

---

## ⚡ Super Fast Start (Windows)

### Option 1: Double-Click Launcher (Easiest)
```
1. Navigate to: simulations/
2. Double-click: launch_gui.bat
3. Wait for automatic setup
4. Dashboard opens automatically! 🎉
```

### Option 2: Manual Launch
```powershell
cd simulations
python hull_analysis_gui.py
```

---

## 📦 One-Time Setup (First Use Only)

### Install Python (if not installed)
1. Download from: https://python.org/downloads/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify: Open PowerShell, type `python --version`

### Install Dependencies
```powershell
# Navigate to project
cd "path\to\Fluids-Mechanics-RC-Ship\simulations"

# Install GUI packages
python -m pip install PyQt6 matplotlib numpy
```

**That's it!** You're ready to analyze! 🚢

---

## 🎯 Your First Analysis (5-Minute Tutorial)

### Step 1: Launch Dashboard
```powershell
python hull_analysis_gui.py
```

You'll see a professional dark-themed window with 5 tabs.

### Step 2: Review Parameters (⚙️ Tab)
Default values are already set:
- ✅ Length: 0.45 m
- ✅ Beam: 0.172 m
- ✅ Draft: 0.055 m
- ✅ Cargo: 2.5 kg

**No changes needed for first run!**

### Step 3: Run Complete Analysis
1. Click the **big red button**: `⚡ Run Complete Analysis`
2. Watch the progress bar (takes ~10 seconds)
3. Results appear automatically!

### Step 4: Explore Results

#### ⚖️ Stability Tab
- See if boat floats or sinks
- Check metacentric height (GM)
- View stability charts

#### 🌊 Resistance Tab
- ITTC-1957 calculations
- Resistance curves
- Power requirements

#### 📐 3D Visualization Tab
- Interactive 3D hull model
- Rotate with mouse
- Export as image

#### 📊 Summary Report Tab
- Complete analysis overview
- Export as TXT or JSON

---

## 💡 Common Tasks

### Change Cargo Weight
```
1. Go to ⚙️ Parameters tab
2. Find "Cargo Mass (kg)"
3. Change value (e.g., 3.0)
4. Click "⚡ Run Complete Analysis"
```

### Test Different Velocities
```
1. Go to ⚙️ Parameters tab
2. Find "Design Velocity (m/s)"
3. Change value (e.g., 0.7)
4. Click "🌊 Run Resistance Analysis"
```

### Export 3D Image
```
1. Go to 📐 3D Visualization tab
2. Click "🎨 Generate 3D Visualization"
3. Wait for rendering
4. Click "💾 Export Image"
5. Choose save location
```

### Save Complete Report
```
1. Go to 📊 Summary Report tab
2. Run complete analysis first
3. Click "📄 Export Report (TXT)"
4. File saved with timestamp!
```

---

## 🎨 Understanding the Interface

### Color Codes
- 🟢 **Teal buttons**: Safe actions (run analysis)
- 🔴 **Red button**: Complete analysis (all modules)
- ⚠️ **Yellow text**: Warning values
- ✅ **Green text**: Good values
- ❌ **Red text**: Failed criteria

### Status Bar (Bottom)
- **Left**: Current operation
- **Right**: Progress bar (0-100%)

### Tabs (Top)
1. **⚙️ Parameters**: Input your design
2. **⚖️ Stability**: Is it stable? Will it float?
3. **🌊 Resistance**: How much drag?
4. **📐 3D Viz**: See your hull
5. **📊 Summary**: Full report

---

## 🔍 Interpreting Results

### Stability Analysis

#### Good Signs ✅
```
GM > 5 cm           → Stable
Buoyancy > Weight   → Floats
Draft < 6 cm        → Meets spec
```

#### Warning Signs ⚠️
```
GM = 2-5 cm         → Marginal stability
GM < 2 cm           → Sensitive to load shifts
Draft > 6 cm        → Exceeds limit
```

#### Bad Signs ❌
```
GM < 0              → UNSTABLE
Buoyancy < Weight   → SINKS
```

### Resistance Analysis

#### Key Metrics
```
Re > 10⁵            → Turbulent flow (good for ITTC)
Fr < 0.4            → Displacement mode
Power << 75W        → Plenty of margin
```

### Design Compliance

Check the Summary Report for:
```
✅ Draft < 6 cm
✅ Cargo ≥ 1.5 kg
✅ Power < 75 W
⚠️ GM > 5 cm
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: PyQt6"
```powershell
python -m pip install PyQt6
```

### "No module named 'stability_analysis'"
```powershell
# Make sure you're in simulations/ folder
cd simulations
python hull_analysis_gui.py
```

### Window doesn't open
```powershell
# Check Python version (need 3.9+)
python --version

# Try verbose mode
python hull_analysis_gui.py --verbose
```

### Plots don't show
```powershell
# Install matplotlib
python -m pip install matplotlib
```

### Slow performance
- Close other programs
- Reduce velocity range (fewer points)
- Run individual analyses instead of complete

---

## 🎓 Pro Tips

### Keyboard Shortcuts
- `Ctrl+Tab`: Switch tabs
- `Alt+F4`: Close window
- Mouse wheel: Zoom plots

### Workflow Optimization
1. **Design iteration**: Use Parameters → Stability only
2. **Performance check**: Use Parameters → Resistance only
3. **Final validation**: Use Complete Analysis
4. **Documentation**: Export everything from Summary tab

### Best Practices
- Always check flotation status first
- GM should be > 5 cm for safety
- Keep draft under 6 cm
- Test multiple cargo weights
- Export results before closing

### Data Analysis
1. Export JSON for Excel/Python processing
2. Export TXT for reports/documentation
3. Export PNG for presentations/papers

---

## 📚 Next Steps

### Learn More
- Read `README_GUI.md` for full documentation
- Check `informe_barcaza.tex` for theory
- Review Python scripts for calculations

### Modify Design
- Change hull dimensions in Parameters
- Test different mass distributions
- Optimize for stability or speed

### Advanced Features
- Edit `stability_analysis.py` for custom calculations
- Modify `resistance_calc.py` for different methods
- Extend GUI with new analysis modules

---

## 🤝 Need Help?

### Common Questions

**Q: Can I change hull shape?**
A: Yes! Edit L, B, H in Parameters tab. Bow length changes pyramid size.

**Q: What if I exceed draft limit?**
A: Reduce total mass or increase beam for better flotation.

**Q: How to improve stability?**
A: Lower center of gravity (KG), increase beam, add ballast.

**Q: Why is my boat sinking?**
A: Total mass > displacement. Reduce weight or increase draft.

**Q: Can I export to Excel?**
A: Yes! Export JSON, then import in Excel/Python/MATLAB.

---

## ✨ Features Coming Soon
- [ ] Real-time 3D rotation
- [ ] Parametric optimization
- [ ] Multi-design comparison
- [ ] ESP32 telemetry integration
- [ ] Auto-report generation for LaTeX

---

## 📞 Contact

**Issues?** Open a GitHub issue or contact team members.

**Feedback?** We'd love to hear how you're using the dashboard!

---

**Made with ❤️ by UMNG Mechatronics Team**

🚢 **Now go analyze some hulls!** 🌊
