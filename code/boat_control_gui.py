"""
ESP32 Boat Control - Modern PyQt6 Interface
Professional UI for controlling RC cargo barge via ESP32 ESP-NOW
"""

import sys
import serial
import serial.tools.list_ports
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QGroupBox, QSlider, QTextEdit,
    QGridLayout, QFrame, QStatusBar, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor


class SerialThread(QThread):
    """Thread for handling serial communication"""
    data_received = pyqtSignal(str)
    connection_status = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.running = False

    def connect(self, port, baudrate=115200):
        """Connect to serial port"""
        try:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            
            self.serial_port = serial.Serial(port, baudrate, timeout=0.1)
            self.running = True
            self.connection_status.emit(True)
            return True
        except Exception as e:
            self.connection_status.emit(False)
            return False

    def disconnect(self):
        """Disconnect from serial port"""
        self.running = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.connection_status.emit(False)

    def send_command(self, command):
        """Send command to ESP32"""
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(f"{command}\n".encode())
                return True
            except Exception as e:
                print(f"Error sending command: {e}")
                return False
        return False

    def run(self):
        """Read serial data continuously"""
        while self.running:
            if self.serial_port and self.serial_port.is_open:
                try:
                    if self.serial_port.in_waiting:
                        data = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
                        if data:
                            self.data_received.emit(data)
                except Exception as e:
                    print(f"Error reading serial: {e}")
            self.msleep(50)


class ModernButton(QPushButton):
    """Custom styled button with modern appearance"""
    def __init__(self, text, color="#2196F3", parent=None):
        super().__init__(text, parent)
        self.default_color = color
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {self._lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(color)};
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
                color: #666666;
            }}
        """)

    def _lighten_color(self, color):
        """Lighten color for hover effect"""
        color_map = {
            "#2196F3": "#42A5F5",
            "#4CAF50": "#66BB6A",
            "#F44336": "#EF5350",
            "#FF9800": "#FFA726",
            "#9C27B0": "#AB47BC",
        }
        return color_map.get(color, "#64B5F6")

    def _darken_color(self, color):
        """Darken color for pressed effect"""
        color_map = {
            "#2196F3": "#1976D2",
            "#4CAF50": "#388E3C",
            "#F44336": "#D32F2F",
            "#FF9800": "#F57C00",
            "#9C27B0": "#7B1FA2",
        }
        return color_map.get(color, "#1976D2")


class BoatControlGUI(QMainWindow):
    """Main GUI window for boat control"""
    
    def __init__(self):
        super().__init__()
        self.serial_thread = SerialThread()
        self.serial_thread.data_received.connect(self.on_serial_data)
        self.serial_thread.connection_status.connect(self.on_connection_status)
        
        self.current_velocity = 200
        self.is_connected = False
        
        self.init_ui()
        self.refresh_ports()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🚤 ESP32 Boat Control - Fluid Mechanics Project")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set modern dark theme
        self.set_dark_theme()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Connection & Control
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.create_connection_group())
        left_panel.addWidget(self.create_control_group())
        left_panel.addWidget(self.create_velocity_group())
        left_panel.addStretch()
        
        # Right panel - Telemetry & Logs
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.create_telemetry_group())
        right_panel.addWidget(self.create_log_group())
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready - Not connected")
        
        # Update timer for telemetry
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_telemetry)
        self.update_timer.start(1000)

    def set_dark_theme(self):
        """Apply modern dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                border: 2px solid #3C3C3C;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2196F3;
            }
            QLabel {
                color: #E0E0E0;
                font-size: 13px;
            }
            QComboBox {
                background-color: #2C2C2C;
                border: 2px solid #3C3C3C;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
                min-height: 30px;
            }
            QComboBox:hover {
                border-color: #2196F3;
            }
            QComboBox::drop-down {
                border: none;
            }
            QTextEdit {
                background-color: #252525;
                border: 2px solid #3C3C3C;
                border-radius: 6px;
                padding: 8px;
                color: #E0E0E0;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #3C3C3C;
                height: 8px;
                background: #2C2C2C;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                border: 2px solid #1976D2;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #42A5F5;
            }
            QProgressBar {
                border: 2px solid #3C3C3C;
                border-radius: 6px;
                background-color: #2C2C2C;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 4px;
            }
        """)

    def create_connection_group(self):
        """Create connection control group"""
        group = QGroupBox("🔌 Connection")
        layout = QVBoxLayout()
        
        # Port selection
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("COM Port:"))
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(150)
        port_layout.addWidget(self.port_combo)
        
        self.refresh_btn = ModernButton("🔄", "#9C27B0")
        self.refresh_btn.setMaximumWidth(50)
        self.refresh_btn.clicked.connect(self.refresh_ports)
        port_layout.addWidget(self.refresh_btn)
        layout.addLayout(port_layout)
        
        # Connect/Disconnect buttons
        btn_layout = QHBoxLayout()
        self.connect_btn = ModernButton("Connect", "#4CAF50")
        self.connect_btn.clicked.connect(self.toggle_connection)
        btn_layout.addWidget(self.connect_btn)
        layout.addLayout(btn_layout)
        
        # Connection status indicator
        self.status_label = QLabel("● Disconnected")
        self.status_label.setStyleSheet("color: #F44336; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        group.setLayout(layout)
        return group

    def create_control_group(self):
        """Create movement control group"""
        group = QGroupBox("🎮 Movement Control")
        layout = QGridLayout()
        
        # Movement buttons with directional layout
        self.forward_btn = ModernButton("⬆\nADELANTE", "#2196F3")
        self.forward_btn.clicked.connect(lambda: self.send_movement_command("w"))
        layout.addWidget(self.forward_btn, 0, 1)
        
        self.left_btn = ModernButton("⬅\nIZQUIERDA", "#2196F3")
        self.left_btn.clicked.connect(lambda: self.send_movement_command("a"))
        layout.addWidget(self.left_btn, 1, 0)
        
        self.stop_btn = ModernButton("⏹\nPARAR", "#F44336")
        self.stop_btn.clicked.connect(lambda: self.send_movement_command("p"))
        layout.addWidget(self.stop_btn, 1, 1)
        
        self.right_btn = ModernButton("➡\nDERECHA", "#2196F3")
        self.right_btn.clicked.connect(lambda: self.send_movement_command("d"))
        layout.addWidget(self.right_btn, 1, 2)
        
        self.backward_btn = ModernButton("⬇\nATRAS", "#2196F3")
        self.backward_btn.clicked.connect(lambda: self.send_movement_command("s"))
        layout.addWidget(self.backward_btn, 2, 1)
        
        # Disable buttons initially
        self.set_control_buttons_enabled(False)
        
        group.setLayout(layout)
        return group

    def create_velocity_group(self):
        """Create velocity control group"""
        group = QGroupBox("⚡ Velocity Control (PWM)")
        layout = QVBoxLayout()
        
        # Velocity slider
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("0"))
        
        self.velocity_slider = QSlider(Qt.Orientation.Horizontal)
        self.velocity_slider.setMinimum(0)
        self.velocity_slider.setMaximum(255)
        self.velocity_slider.setValue(200)
        self.velocity_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.velocity_slider.setTickInterval(50)
        self.velocity_slider.valueChanged.connect(self.on_velocity_changed)
        slider_layout.addWidget(self.velocity_slider)
        
        slider_layout.addWidget(QLabel("255"))
        layout.addLayout(slider_layout)
        
        # Velocity display
        self.velocity_label = QLabel(f"Current: {self.current_velocity} PWM")
        self.velocity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.velocity_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3;")
        layout.addWidget(self.velocity_label)
        
        # Preset buttons
        preset_layout = QHBoxLayout()
        
        slow_btn = ModernButton("Slow (100)", "#4CAF50")
        slow_btn.clicked.connect(lambda: self.set_velocity(100))
        preset_layout.addWidget(slow_btn)
        
        medium_btn = ModernButton("Medium (180)", "#FF9800")
        medium_btn.clicked.connect(lambda: self.set_velocity(180))
        preset_layout.addWidget(medium_btn)
        
        fast_btn = ModernButton("Fast (255)", "#F44336")
        fast_btn.clicked.connect(lambda: self.set_velocity(255))
        preset_layout.addWidget(fast_btn)
        
        layout.addLayout(preset_layout)
        
        group.setLayout(layout)
        return group

    def create_telemetry_group(self):
        """Create telemetry display group"""
        group = QGroupBox("📊 Telemetry")
        layout = QVBoxLayout()
        
        # Status indicators
        self.boat_status_label = QLabel("Boat Status: Waiting...")
        self.boat_status_label.setStyleSheet("font-size: 14px; padding: 8px;")
        layout.addWidget(self.boat_status_label)
        
        self.last_command_label = QLabel("Last Command: None")
        self.last_command_label.setStyleSheet("font-size: 14px; padding: 8px;")
        layout.addWidget(self.last_command_label)
        
        # Signal strength indicator (simulated)
        signal_layout = QHBoxLayout()
        signal_layout.addWidget(QLabel("Signal Strength:"))
        self.signal_bar = QProgressBar()
        self.signal_bar.setValue(85)
        signal_layout.addWidget(self.signal_bar)
        layout.addLayout(signal_layout)
        
        # Connection time
        self.connection_time_label = QLabel("Connection Time: --:--:--")
        self.connection_time_label.setStyleSheet("font-size: 13px; padding: 8px;")
        layout.addWidget(self.connection_time_label)
        
        self.connection_start_time = None
        
        group.setLayout(layout)
        return group

    def create_log_group(self):
        """Create log display group"""
        group = QGroupBox("📝 Serial Monitor Log")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(300)
        layout.addWidget(self.log_text)
        
        # Log control buttons
        btn_layout = QHBoxLayout()
        
        clear_btn = ModernButton("Clear Log", "#F44336")
        clear_btn.clicked.connect(self.clear_log)
        btn_layout.addWidget(clear_btn)
        
        save_btn = ModernButton("Save Log", "#4CAF50")
        save_btn.clicked.connect(self.save_log)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        return group

    def refresh_ports(self):
        """Refresh available COM ports"""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}")
        
        if ports:
            self.log_message("✓ Ports refreshed", "#4CAF50")
        else:
            self.log_message("⚠ No COM ports found", "#FF9800")

    def toggle_connection(self):
        """Toggle serial connection"""
        if not self.is_connected:
            port = self.port_combo.currentText().split(" - ")[0]
            if self.serial_thread.connect(port):
                self.serial_thread.start()
                self.is_connected = True
                self.connect_btn.setText("Disconnect")
                self.connect_btn.setStyleSheet(self.connect_btn.styleSheet().replace("#4CAF50", "#F44336"))
                self.connection_start_time = datetime.now()
                self.log_message(f"✓ Connected to {port}", "#4CAF50")
        else:
            self.serial_thread.disconnect()
            self.serial_thread.wait()
            self.is_connected = False
            self.connect_btn.setText("Connect")
            self.connect_btn.setStyleSheet(self.connect_btn.styleSheet().replace("#F44336", "#4CAF50"))
            self.connection_start_time = None
            self.log_message("⚠ Disconnected", "#FF9800")

    def on_connection_status(self, connected):
        """Handle connection status change"""
        if connected:
            self.status_label.setText("● Connected")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.set_control_buttons_enabled(True)
            self.statusBar.showMessage(f"Connected to {self.port_combo.currentText()}")
        else:
            self.status_label.setText("● Disconnected")
            self.status_label.setStyleSheet("color: #F44336; font-weight: bold;")
            self.set_control_buttons_enabled(False)
            self.statusBar.showMessage("Not connected")

    def set_control_buttons_enabled(self, enabled):
        """Enable/disable control buttons"""
        self.forward_btn.setEnabled(enabled)
        self.backward_btn.setEnabled(enabled)
        self.left_btn.setEnabled(enabled)
        self.right_btn.setEnabled(enabled)
        self.stop_btn.setEnabled(enabled)

    def send_movement_command(self, command):
        """Send movement command to ESP32 with current velocity"""
        # Send command with velocity parameter
        full_command = f"{command}"
        if self.serial_thread.send_command(full_command):
            command_names = {
                'w': 'ADELANTE',
                's': 'ATRAS',
                'a': 'IZQUIERDA',
                'd': 'DERECHA',
                'p': 'PARAR'
            }
            cmd_name = command_names.get(command, command)
            self.last_command_label.setText(f"Last Command: {cmd_name} @ {self.current_velocity} PWM")
            self.log_message(f"→ Sent: {cmd_name} @ PWM {self.current_velocity}", "#2196F3")

    def on_velocity_changed(self, value):
        """Handle velocity slider change"""
        self.current_velocity = value
        self.velocity_label.setText(f"Current: {value} PWM")
        # Update velocity in real-time without sending command
        # Velocity will be included automatically with next movement command
        if self.is_connected and hasattr(self, '_last_velocity_update'):
            # Debounce: only send velocity command every 500ms
            if (datetime.now() - self._last_velocity_update).total_seconds() > 0.5:
                self.serial_thread.send_command(f"vel {value}")
                self.log_message(f"⚡ Velocity set to {value}", "#FF9800")
                self._last_velocity_update = datetime.now()
        elif self.is_connected:
            self._last_velocity_update = datetime.now()
            self.serial_thread.send_command(f"vel {value}")
            self.log_message(f"⚡ Velocity set to {value}", "#FF9800")

    def set_velocity(self, value):
        """Set velocity to preset value"""
        self.velocity_slider.setValue(value)

    def on_serial_data(self, data):
        """Handle incoming serial data"""
        self.log_message(f"← {data}", "#4CAF50")
        
        # Parse boat status
        if "ESTADO DEL BARCO" in data or "Estado:" in data:
            self.boat_status_label.setText(f"Boat Status: {data}")

    def update_telemetry(self):
        """Update telemetry display"""
        if self.connection_start_time:
            elapsed = datetime.now() - self.connection_start_time
            hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.connection_time_label.setText(f"Connection Time: {hours:02d}:{minutes:02d}:{seconds:02d}")

    def log_message(self, message, color="#E0E0E0"):
        """Add message to log with timestamp and color"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f'<span style="color: {color};">[{timestamp}] {message}</span>')
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def clear_log(self):
        """Clear log display"""
        self.log_text.clear()
        self.log_message("Log cleared", "#9C27B0")

    def save_log(self):
        """Save log to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"boat_control_log_{timestamp}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.toPlainText())
            self.log_message(f"✓ Log saved to {filename}", "#4CAF50")
        except Exception as e:
            self.log_message(f"✗ Error saving log: {e}", "#F44336")

    def closeEvent(self, event):
        """Handle window close event"""
        if self.is_connected:
            self.serial_thread.disconnect()
            self.serial_thread.wait()
        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    window = BoatControlGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
