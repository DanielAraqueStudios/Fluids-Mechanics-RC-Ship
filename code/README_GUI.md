# 🚤 ESP32 Boat Control - Professional GUI

Modern PyQt6 interface for controlling the RC cargo barge via ESP32 ESP-NOW.

## ✨ Features

- **🎮 Intuitive Control**: Directional buttons for forward, backward, left, right movements
- **⚡ Variable Speed**: Real-time PWM velocity control (0-255) with slider and presets
- **📊 Live Telemetry**: Real-time status monitoring and signal strength
- **📝 Serial Monitor**: Built-in log viewer with color-coded messages
- **🔌 Easy Connection**: Auto-detect COM ports with one-click connect
- **🌙 Modern Dark Theme**: Professional UI/UX with smooth animations
- **💾 Data Logging**: Save session logs for analysis

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the GUI
python boat_control_gui.py
```

## 📖 User Guide

### 1. Connect to ESP32

1. Click **🔄** to refresh available COM ports
2. Select the COM port connected to your ESP32 Control
3. Click **Connect** button
4. Wait for "● Connected" status (green)

### 2. Control the Boat

**Movement Controls:**
- **⬆ ADELANTE**: Move forward
- **⬇ ATRAS**: Move backward
- **⬅ IZQUIERDA**: Turn left
- **➡ DERECHA**: Turn right
- **⏹ PARAR**: Stop all motors

**Velocity Control:**
- Use slider to set PWM value (0-255)
- Quick presets: Slow (100), Medium (180), Fast (255)
- Changes apply immediately

### 3. Monitor Telemetry

- **Boat Status**: Current boat state and command
- **Signal Strength**: Communication quality indicator
- **Connection Time**: Active session duration
- **Serial Log**: All sent/received messages with timestamps

### 4. Save Data

- **Clear Log**: Reset the serial monitor
- **Save Log**: Export session data to timestamped `.txt` file

## 🎨 Interface Overview

```
┌─────────────────────────────────────────────────────────────┐
│  🚤 ESP32 Boat Control - Fluid Mechanics Project             │
├──────────────────┬──────────────────────────────────────────┤
│  🔌 Connection   │  📊 Telemetry                             │
│  - COM Port      │  - Boat Status: ADELANTE                  │
│  - Connect       │  - Last Command: ADELANTE                 │
│  ● Connected     │  - Signal: ████████░░ 85%                 │
│                  │  - Connection Time: 00:05:32              │
│  🎮 Control      │                                            │
│      [⬆]         │  📝 Serial Monitor Log                    │
│  [⬅] [⏹] [➡]    │  ┌────────────────────────────────────┐  │
│      [⬇]         │  │ [10:23:45] ✓ Connected to COM3     │  │
│                  │  │ [10:23:46] → Sent: ADELANTE        │  │
│  ⚡ Velocity     │  │ [10:23:46] ← [TX] Comando OK       │  │
│  [0]━━●━━━[255] │  │ [10:23:47] ← [RX] ESTADO BARCO     │  │
│  Current: 200    │  │ [10:23:48] ⚡ Velocity set to 180  │  │
│  [Slow][Med][Fast│  └────────────────────────────────────┘  │
│                  │  [Clear Log]  [Save Log]                  │
└──────────────────┴──────────────────────────────────────────┘
```

## 🛠️ Technical Details

### Architecture

- **Main Thread**: UI rendering and user interaction
- **Serial Thread**: Asynchronous serial communication (non-blocking)
- **Update Timer**: 1Hz telemetry refresh rate

### Serial Communication

- **Baudrate**: 115200 bps (default)
- **Protocol**: Text-based commands compatible with EspControl.ino
- **Commands**: w, s, a, d, p, vel [0-255]

### Color Coding

- 🔵 **Blue (#2196F3)**: Sent commands
- 🟢 **Green (#4CAF50)**: Successful operations / Received data
- 🟠 **Orange (#FF9800)**: Warnings / Velocity changes
- 🔴 **Red (#F44336)**: Errors / Disconnections
- 🟣 **Purple (#9C27B0)**: System messages

## 🔧 Customization

### Change Theme Colors

Edit `set_dark_theme()` method in `boat_control_gui.py`:

```python
# Example: Change primary color to green
border-color: #4CAF50;  # Replace #2196F3
```

### Add Custom Commands

Add buttons in `create_control_group()`:

```python
custom_btn = ModernButton("Custom\nCommand", "#FF9800")
custom_btn.clicked.connect(lambda: self.send_custom_command("custom"))
layout.addWidget(custom_btn, row, col)
```

### Adjust PWM Range

Modify velocity slider in `create_velocity_group()`:

```python
self.velocity_slider.setMaximum(180)  # Limit to 180 instead of 255
```

## 📊 Data Analysis Integration

The GUI can be extended to log telemetry for IT (Transport Index) calculation:

```python
# Add to SerialThread
def log_telemetry(self, timestamp, command, velocity, voltage, current):
    with open('telemetry_log.csv', 'a') as f:
        f.write(f"{timestamp},{command},{velocity},{voltage},{current}\n")
```

## 🐛 Troubleshooting

### Port Not Found
- Verify ESP32 is connected via USB
- Check Device Manager (Windows) or `ls /dev/tty*` (Linux)
- Install CH340/CP2102 drivers if needed

### No Response from Boat
- Verify ESP32 Control has correct MAC address configured
- Check Serial Monitor in Arduino IDE first
- Ensure boat ESP32 is powered and within 20m range

### GUI Freezes
- Serial thread should prevent this - check for exceptions
- Increase `timeout` in SerialThread.connect()

## 📝 License

Part of the Fluids-Mechanics-RC-Ship project for Universidad Militar Nueva Granada.
Based on [ESP32-Boat-Control-ESPNOW](https://github.com/2J5R6/ESP32-Boat-Control-ESPNOW-).

## 🤝 Contributing

Improvements welcome! Focus areas:
- Gamepad/joystick support
- Real-time power consumption graphs
- GPS position tracking
- Autonomous waypoint navigation
