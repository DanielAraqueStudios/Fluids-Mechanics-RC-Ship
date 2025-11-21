# 🎨 UI/UX Design Specification - RC Barge Analysis Dashboard

**Professional Dark Mode Interface for Hydrodynamic Analysis**

---

## 🎯 Design Philosophy

### Core Principles
1. **Clarity**: Information hierarchy, readable typography
2. **Efficiency**: Quick access to all functions
3. **Professional**: Engineering-grade aesthetics
4. **Dark Mode**: Reduced eye strain for extended use
5. **Responsive**: Adapts to different window sizes

---

## 🖼️ Screen Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  🚢 RC Cargo Barge - Hydrodynamic Analysis Dashboard            │
│  UMNG | Fluid Mechanics Project | ITTC-1957                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ [⚙️ Parameters] [⚖️ Stability] [🌊 Resistance] [📐 3D] [📊] │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                            │ │
│  │              TAB CONTENT AREA                              │ │
│  │                                                            │ │
│  │  [Inputs, Results, Plots, Visualizations]                 │ │
│  │                                                            │ │
│  │                                                            │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ ⚡ Running analysis...          [████████░░] 80%                │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Color Palette

### Primary Colors
```
Teal Primary:    #0d7377  ███  Main actions, highlights
Mint Secondary:  #14a085  ███  Accents, success states
Alert Red:       #e63946  ███  Warnings, critical values
Warm Orange:     #ffa500  ███  Info, Froude number plots
```

### Neutral Colors
```
Background:      #1e1e1e  ███  Main canvas
Surface:         #2b2b2b  ███  Cards, inputs, panels
Border:          #3d3d3d  ███  Separators, outlines
Text Primary:    #ffffff  ███  Headers, important text
Text Secondary:  #e0e0e0  ███  Body text, labels
Text Muted:      #7d7d7d  ███  Disabled, placeholders
```

### Semantic Colors
```
Success:         #14a085  ███  ✓ Passed checks
Warning:         #ffa500  ███  ⚠️ Marginal values
Error:           #e63946  ███  ✗ Failed criteria
Info:            #0d7377  ███  ℹ️ Informational
```

---

## 📝 Typography

### Font Family
```
Primary:    'Segoe UI', Arial, sans-serif
Monospace:  'Consolas', 'Courier New', monospace
```

### Font Sizes
```
Header:     16pt Bold    (Main title)
Subtitle:   11pt Bold    (Section headers)
Body:       10pt Regular (Default text)
Label:      10pt Regular (Input labels)
Code:       9pt Monospace (Results, logs)
Small:      8pt Regular  (Footnotes)
```

### Font Weights
```
Bold:       600-700  (Headers, buttons, key values)
Regular:    400      (Body text, labels)
Light:      300      (Subtle text, less important)
```

---

## 🧩 Component Styles

### Buttons

#### Primary Action (Teal)
```css
Background:  #0d7377
Hover:       #14a085
Active:      #0a5f62
Text:        #ffffff
Padding:     10px 20px
Radius:      5px
Font:        10pt Bold
```

#### Secondary Action (Gray)
```css
Background:  #3d3d3d
Hover:       #4d4d4d
Text:        #ffffff
```

#### Critical Action (Red)
```css
Background:  #e63946
Hover:       #ff4c5c
Text:        #ffffff
```

### Input Fields
```css
Background:  #2b2b2b
Border:      1px solid #3d3d3d
Focus:       2px solid #0d7377
Padding:     6px
Radius:      4px
Text:        #ffffff
Placeholder: #7d7d7d
```

### Group Boxes
```css
Border:      2px solid #3d3d3d
Radius:      8px
Title Color: #14a085
Title Font:  10pt Bold
Padding:     15px
```

### Progress Bar
```css
Background:  #2b2b2b
Border:      1px solid #3d3d3d
Fill:        #0d7377
Height:      20px
Radius:      4px
Text:        Centered, #ffffff
```

### Text Areas
```css
Background:  #2b2b2b
Border:      1px solid #3d3d3d
Text:        #e0e0e0
Font:        Consolas 9pt
Padding:     10px
Scrollbar:   #0d7377 on #2b2b2b
```

---

## 📋 Tab Layouts

### 1️⃣ Parameters Tab

```
┌─────────────────────────────────────────────────┐
│  🔧 Hull Geometry                               │
│  ┌───────────────────────────────────────────┐  │
│  │  Total Length (m):     [0.450]           │  │
│  │  Beam (m):             [0.172]           │  │
│  │  Height (m):           [0.156]           │  │
│  │  Bow Length (m):       [0.050]           │  │
│  │  Draft (m):            [0.055]           │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ⚖️ Mass Distribution                           │
│  ┌───────────────────────────────────────────┐  │
│  │  Hull Mass (kg):       [1.200]           │  │
│  │  Electronics (kg):     [1.000]           │  │
│  │  Cargo (kg):           [2.500]           │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  🔬 Analysis Parameters                         │
│  ┌───────────────────────────────────────────┐  │
│  │  Design Velocity (m/s):[0.500]           │  │
│  │  Form Factor (k):      [0.200]           │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  [🔄 Stability] [🌊 Resistance] [⚡ Complete]   │
└─────────────────────────────────────────────────┘
```

### 2️⃣ Stability Tab

```
┌─────────────────────────────────────────────────┐
│  📊 STABILITY ANALYSIS RESULTS                  │
│  ════════════════════════════════════════════   │
│                                                  │
│  HULL GEOMETRY                                   │
│  ────────────────────────────────────────────   │
│    Length:              0.450 m                  │
│    Beam:                0.172 m                  │
│    Draft:               0.055 m                  │
│                                                  │
│  STABILITY PARAMETERS                            │
│  ────────────────────────────────────────────   │
│    KB:                  2.69 cm                  │
│    BM:                  4.32 cm                  │
│    GM:                  2.16 cm  ⚠ MARGINAL     │
│                                                  │
│  FLOTATION                                       │
│  ────────────────────────────────────────────   │
│    Buoyancy Force:      38.67 N ↑               │
│    Weight Force:        46.11 N ↓               │
│    Status:              ✗ SINKS                 │
│                                                  │
├─────────────────────────────────────────────────┤
│  [Chart: Stability Centers] [Chart: Mass Dist] │
└─────────────────────────────────────────────────┘
```

### 3️⃣ Resistance Tab

```
┌─────────────────────────────────────────────────┐
│  🌊 RESISTANCE ANALYSIS (ITTC-1957)             │
│  ════════════════════════════════════════════   │
│                                                  │
│  DESIGN VELOCITY: 0.50 m/s                      │
│  ────────────────────────────────────────────   │
│    Reynolds:            2.24×10⁵                │
│    Froude:              0.238 (displacement)    │
│    Resistance:          0.165 N                  │
│    Power:               0.083 W                  │
│                                                  │
├─────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │ Resistance vs V │  │  Power vs V    │      │
│  │                 │  │                 │      │
│  │   [Plot]        │  │   [Plot]        │      │
│  └─────────────────┘  └─────────────────┘      │
│  ┌─────────────────┐  ┌─────────────────┐      │
│  │ Reynolds vs V   │  │  Froude vs V   │      │
│  │   [Plot]        │  │   [Plot]        │      │
│  └─────────────────┘  └─────────────────┘      │
└─────────────────────────────────────────────────┘
```

### 4️⃣ 3D Visualization Tab

```
┌─────────────────────────────────────────────────┐
│                                                  │
│              ╱╲                                  │
│             ╱  ╲                                 │
│            ╱    ╲                                │
│           ╱      ╲                               │
│          ╱________╲                              │
│         ┌──────────┐                             │
│         │          │                             │
│         │   HULL   │                             │
│         │   3D     │                             │
│         │  RENDER  │                             │
│         └──────────┘                             │
│                                                  │
│  [🎨 Generate 3D] [💾 Export Image]             │
└─────────────────────────────────────────────────┘
```

### 5️⃣ Summary Report Tab

```
┌─────────────────────────────────────────────────┐
│  📊 COMPREHENSIVE ANALYSIS REPORT               │
│  ════════════════════════════════════════════   │
│                                                  │
│  Generated: 2025-11-20 15:30:45                 │
│  UMNG | Fluid Mechanics Project                 │
│                                                  │
│  HULL SPECIFICATIONS                             │
│  ────────────────────────────────────────────   │
│    Total Length:        0.450 m                  │
│    Beam:                0.172 m                  │
│    ...                                           │
│                                                  │
│  DESIGN COMPLIANCE                               │
│  ────────────────────────────────────────────   │
│    ✓ Length 0.35-0.60 m                         │
│    ✗ Draft < 6 cm        (6.56 cm)              │
│    ✓ Cargo ≥ 1.5 kg      (2.50 kg)             │
│    ✓ Power < 75 W        (0.22 W)              │
│                                                  │
│  [📄 Export TXT] [📊 Export JSON]               │
└─────────────────────────────────────────────────┘
```

---

## 🎭 Interactive Elements

### Hover States
```
Buttons:     Lighter background, slight shadow
Inputs:      Border highlights to #0d7377
Links:       Underline appears
Tabs:        Background changes to #14a085
```

### Focus States
```
Inputs:      2px border #0d7377, glow effect
Buttons:     Outline appears
Text Areas:  Border highlights
```

### Active States
```
Buttons:     Darker background, pressed effect
Tabs:        Underline indicator
```

### Disabled States
```
Background:  #3d3d3d
Text:        #7d7d7d
Cursor:      not-allowed
```

---

## 📐 Spacing & Layout

### Margins
```
Window:      10px
Section:     20px
Element:     10px
Group:       15px
```

### Padding
```
Container:   15px
Card:        20px
Input:       6px
Button:      10px 20px
```

### Grid System
```
Columns:     12-column flexible grid
Gutters:     10px
Breakpoints: Responsive to window resize
```

---

## 🖱️ User Interactions

### Workflow
```
1. User opens app → Parameters tab visible
2. User reviews/edits parameters
3. User clicks analysis button
4. Progress bar shows → Status updates
5. Results tab auto-switches
6. User reviews results/charts
7. User exports if needed
```

### Feedback
```
Button Click:    Visual press effect
Analysis Start:  Progress bar activates
Analysis Done:   Tab switches, status updates
Error:           Red text, error dialog
Success:         Green checkmarks
```

### Navigation
```
Tab switching:   Click tab header
Scrolling:       Mouse wheel in text areas
Plot zoom:       Matplotlib native controls
Export:          File dialog opens
```

---

## ✨ Special Features

### Progress Indicators
- Real-time percentage (0-100%)
- Status text updates ("Calculating KB...", "Complete!")
- Smooth animations

### Plot Customization
- Dark background (#1e1e1e)
- Colored grid lines (#3d3d3d)
- Teal/red/orange curves
- Auto-scaling axes
- Legend with dark background

### Data Validation
- Input ranges enforced
- Invalid values highlighted red
- Tooltips show acceptable ranges
- Auto-correction suggestions

### Export Options
- TXT: Human-readable reports
- JSON: Machine-readable data
- PNG: High-res plots (300 DPI)
- Timestamped filenames

---

## 📱 Responsive Design

### Window Sizes
```
Minimum:     1000x700 px
Optimal:     1400x900 px
Maximum:     No limit (scales)
```

### Adaptive Layout
- Tabs remain visible at all sizes
- Plots resize proportionally
- Text wraps appropriately
- Scrollbars appear when needed

---

## ♿ Accessibility

### Contrast Ratios
```
Text/Background:  WCAG AAA (7:1+)
Links:            WCAG AA (4.5:1+)
Buttons:          High contrast
```

### Keyboard Navigation
- Tab between fields
- Enter to submit
- Arrow keys in plots
- Esc to close dialogs

### Screen Reader
- Alt text for icons
- Labels for inputs
- Status announcements
- Error descriptions

---

## 🎬 Animation & Transitions

### Smooth Transitions
```
Tab switch:      150ms fade
Button hover:    100ms background
Progress bar:    Smooth fill
Plot render:     Fade in 200ms
```

### Loading States
```
Spinner:         Rotating icon
Progress:        Animated bar
Skeleton:        Pulsing placeholders
```

---

## 🔧 Technical Implementation

### Framework
```
GUI:         PyQt6
Plotting:    Matplotlib (Qt5Agg backend)
Threading:   QThread for background tasks
Styling:     Qt StyleSheets (CSS-like)
```

### Performance
```
Responsive:  Non-blocking UI
Memory:      Efficient plot recycling
Speed:       Multi-threaded analysis
Smooth:      60 FPS animations
```

---

**Design Version**: 1.0.0  
**Last Updated**: November 20, 2025  
**Status**: ✅ Implemented in hull_analysis_gui.py

🎨 **Beautiful, functional, professional!** 🚢
