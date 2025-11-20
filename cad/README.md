# 🛠️ CAD Models - Hull Design

## Directory Structure

```
cad/
├── hull_v1.step       # Initial hull design (STEP format for editing)
├── hull_v1.stl        # STL for 3D printing/visualization
├── hull_v2.step       # Optimized design (reduced wetted area)
├── hull_v2.stl
├── motor_mount.step   # Motor mounting bracket
├── propeller.step     # Custom propeller design (optional)
└── assembly.step      # Full assembly with electronics placement
```

## Design Guidelines

### Hull Geometry
- **Length (L)**: 0.35 - 0.60 m (actual: 0.45 m)
- **Beam (B)**: ~40-50% of length for stability
- **Draft (T)**: Max 6 cm at full load (2.5 kg)
- **Prismatic coefficient (Cp)**: 0.75-0.85 for displacement hulls

### Critical Features
1. **Smooth transitions**: Minimize flow separation
2. **Flat bottom**: Maximize cargo volume, reduce draft
3. **Rounded bilges**: Reduce wetted area
4. **Transom stern**: Simplify propeller installation
5. **Watertight compartments**: Electronics protection

### Waterline Analysis
Use CAD software to measure:
- Wetted surface area (S) at design waterline
- Center of buoyancy (KB) position
- Waterplane area (Aw) for stability calculations
- Longitudinal center of flotation (LCF)

### Motor Mounting
- Position propellers 10-15 cm below waterline
- Angle propeller shaft 5-10° downward for efficiency
- Ensure clearance from hull (min 2 cm)
- Seal shaft penetrations with O-rings

## Export Settings

### For 3D Printing (STL)
- Resolution: 0.1 mm
- Units: millimeters
- Binary format (smaller file size)
- Check for manifold geometry

### For Manufacturing (STEP)
- Version: AP214 or AP203
- Include metadata: material, mass properties
- Preserve parametric features

## Material Selection

| Material | Density (kg/m³) | Pros | Cons |
|----------|-----------------|------|------|
| PLA | 1240 | Easy to print, low cost | Brittle, low temp resistance |
| PETG | 1270 | Strong, waterproof | Requires higher temp |
| ABS | 1040 | Durable, impact resistant | Warping, fumes |
| Foam/Fiberglass | 300-600 | Lightweight, strong | Complex fabrication |

**Recommendation**: PETG with 30% infill, 3 perimeters, waterproofed with epoxy resin.

## Design Iterations Log

### v1.0 - Initial Design
- Simple rectangular barge shape
- Area mojada: 0.20 m²
- Issues: High resistance, poor directional stability

### v2.0 - Optimized (Current)
- Added bow taper (15° entry angle)
- Rounded bilges (radius 0.02 m)
- Area mojada: 0.18 m² (-10%)
- Improved directional stability with keel effect

### v3.0 - Future (Optional)
- Consider semi-planing hull for Fr > 0.4
- Hydrofoil-assisted design for advanced testing

## References
- Principles of Naval Architecture (SNAME)
- OpenFOAM CFD validation studies
- Model yacht design databases
