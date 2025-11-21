"""
RC Cargo Barge - Comprehensive Analysis Dashboard
Professional UI/UX with Dark Mode
Universidad Militar Nueva Granada - Fluid Mechanics Project
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess
import json

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox,
    QSpinBox, QDoubleSpinBox, QProgressBar, QFileDialog, QMessageBox,
    QSplitter, QFrame, QScrollArea, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

# Import analysis modules
try:
    from stability_analysis import (
        HullGeometry, MassDistribution, StabilityCalculator
    )
    from resistance_calc import (
        HullParameters, FluidProperties, ITTCResistanceCalculator
    )
    from visualize_hull_3d import create_hull_mesh
except ImportError as e:
    print(f"Warning: Could not import analysis modules: {e}")


class AnalysisWorker(QThread):
    """Worker thread for running analyses without blocking UI"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, analysis_type, parameters):
        super().__init__()
        self.analysis_type = analysis_type
        self.parameters = parameters

    def run(self):
        try:
            if self.analysis_type == "stability":
                results = self.run_stability_analysis()
            elif self.analysis_type == "resistance":
                results = self.run_resistance_analysis()
            elif self.analysis_type == "3d_visualization":
                results = self.run_3d_visualization()
            elif self.analysis_type == "complete":
                results = self.run_complete_analysis()
            else:
                raise ValueError(f"Unknown analysis type: {self.analysis_type}")
            
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

    def run_stability_analysis(self):
        """Run stability analysis with progress updates"""
        self.status.emit("Calculating hull geometry...")
        self.progress.emit(10)
        
        params = self.parameters
        hull = HullGeometry(
            length=params['length'],
            beam=params['beam'],
            height=params['height'],
            bow_length=params['bow_length'],
            draft=params['draft']
        )
        
        # Create mass distribution
        masses = MassDistribution(
            hull_mass=params['hull_mass'],
            hull_cg_height=params['height'] * 0.3,
            cargo_mass=params['cargo_mass'],
            cargo_cg_height=params['height'] * 0.5,
            electronics_mass=params['electronics_mass'],
            electronics_cg_height=0.03
        )
        
        # Create stability calculator
        calc = StabilityCalculator(hull)
        
        self.status.emit("Computing displacement volume...")
        self.progress.emit(25)
        displacement = calc.displacement_volume()
        
        self.status.emit("Calculating center of buoyancy...")
        self.progress.emit(40)
        kb = calc.center_of_buoyancy()
        
        self.status.emit("Computing waterplane area...")
        self.progress.emit(55)
        aw = calc.waterplane_area()
        
        self.status.emit("Calculating metacentric radius...")
        self.progress.emit(70)
        bm = calc.metacentric_radius()
        
        self.status.emit("Computing metacentric height...")
        self.progress.emit(85)
        total_mass, kg = calc.combined_cg(masses)
        gm = calc.metacentric_height(kg)
        
        # Flotation analysis
        self.status.emit("Analyzing flotation...")
        self.progress.emit(95)
        buoyancy_force = displacement * 1000 * 9.81
        weight_force = total_mass * 9.81
        net_force = buoyancy_force - weight_force
        
        results = {
            'hull': hull,
            'displacement': displacement,
            'displacement_mass': displacement * 1000,
            'kb': kb,
            'bm': bm,
            'kg': kg,
            'gm': gm,
            'aw': aw,
            'total_mass': total_mass,
            'buoyancy_force': buoyancy_force,
            'weight_force': weight_force,
            'net_force': net_force,
            'floats': net_force >= 0
        }
        
        self.progress.emit(100)
        self.status.emit("Stability analysis complete!")
        return results

    def run_resistance_analysis(self):
        """Run resistance analysis with progress updates"""
        self.status.emit("Initializing resistance calculations...")
        self.progress.emit(10)
        
        params = self.parameters
        
        # Create hull and fluid properties
        hull_params = HullParameters(
            length=params['length'],
            beam=params['beam'],
            draft=params['draft'],
            wetted_area=params['wetted_area'],
            form_factor=params['form_factor']
        )
        fluid = FluidProperties()
        
        # Create resistance calculator
        calc = ITTCResistanceCalculator(hull_params, fluid)
        
        velocities = np.linspace(0.1, 1.5, 30)
        results = {
            'velocities': velocities,
            'reynolds': [],
            'froude': [],
            'cf': [],
            'resistance': [],
            'power': []
        }
        
        for i, v in enumerate(velocities):
            progress = int(10 + (i / len(velocities)) * 85)
            self.progress.emit(progress)
            self.status.emit(f"Calculating for velocity {v:.2f} m/s...")
            
            re = calc.reynolds_number(v)
            fr = calc.froude_number(v)
            cf = calc.ittc_friction_coefficient(re)
            rf = calc.friction_resistance(v, cf)
            rv = calc.viscous_resistance(rf)
            rw = calc.wave_resistance(v, fr)
            rt = rv + rw
            pe = rt * v
            
            results['reynolds'].append(re)
            results['froude'].append(fr)
            results['cf'].append(cf)
            results['resistance'].append(rt)
            results['power'].append(pe)
        
        self.progress.emit(100)
        self.status.emit("Resistance analysis complete!")
        return results

    def run_3d_visualization(self):
        """Generate 3D hull visualization"""
        self.status.emit("Creating 3D hull mesh...")
        self.progress.emit(30)
        
        params = self.parameters
        hull = HullGeometry(
            length=params['length'],
            beam=params['beam'],
            height=params['height'],
            bow_length=params['bow_length'],
            draft=params['draft']
        )
        
        self.status.emit("Rendering 3D visualization...")
        self.progress.emit(70)
        
        vertices, faces = create_hull_mesh(
            L_total=hull.length,
            L_bow=hull.bow_length,
            B=hull.beam,
            H=hull.height,
            draft=hull.draft
        )
        
        results = {
            'vertices': vertices,
            'faces': faces,
            'hull': hull
        }
        
        self.progress.emit(100)
        self.status.emit("3D visualization ready!")
        return results

    def run_complete_analysis(self):
        """Run all analyses sequentially"""
        all_results = {}
        
        # Stability
        self.status.emit("Running stability analysis...")
        all_results['stability'] = self.run_stability_analysis()
        
        # Resistance
        self.status.emit("Running resistance analysis...")
        self.parameters['wetted_area'] = 0.165
        self.parameters['form_factor'] = 0.2
        all_results['resistance'] = self.run_resistance_analysis()
        
        # 3D Viz
        self.status.emit("Generating 3D visualization...")
        all_results['3d'] = self.run_3d_visualization()
        
        return all_results


class MatplotlibWidget(QWidget):
    """Matplotlib canvas embedded in PyQt6"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(facecolor='#1e1e1e')
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
    def clear(self):
        self.figure.clear()
        self.canvas.draw()


class MainWindow(QMainWindow):
    """Main application window with professional dark mode UI"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RC Cargo Barge - Comprehensive Analysis Dashboard")
        self.setGeometry(100, 100, 1400, 900)
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Initialize variables
        self.current_results = {}
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Main content area with tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background: #2b2b2b;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #3d3d3d;
                color: #ffffff;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #0d7377;
            }
            QTabBar::tab:hover {
                background: #14a085;
            }
        """)
        
        # Create tabs
        self.tab_parameters = self.create_parameters_tab()
        self.tab_stability = self.create_stability_tab()
        self.tab_resistance = self.create_resistance_tab()
        self.tab_3d = self.create_3d_tab()
        self.tab_summary = self.create_summary_tab()
        
        self.tabs.addTab(self.tab_parameters, "⚙️ Parameters")
        self.tabs.addTab(self.tab_stability, "⚖️ Stability")
        self.tabs.addTab(self.tab_resistance, "🌊 Resistance")
        self.tabs.addTab(self.tab_3d, "📐 3D Visualization")
        self.tabs.addTab(self.tab_summary, "📊 Summary Report")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = self.create_status_bar()
        main_layout.addWidget(self.status_bar)
        
        # Load default parameters
        self.load_default_parameters()

    def apply_dark_theme(self):
        """Apply professional dark theme"""
        dark_stylesheet = """
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }
            QGroupBox {
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                font-weight: bold;
                color: #14a085;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel {
                color: #e0e0e0;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 6px;
                color: #ffffff;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 2px solid #0d7377;
            }
            QPushButton {
                background-color: #0d7377;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5f62;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #7d7d7d;
            }
            QTextEdit {
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: #e0e0e0;
                font-family: 'Consolas', monospace;
            }
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                background-color: #2b2b2b;
            }
            QProgressBar::chunk {
                background-color: #0d7377;
                border-radius: 3px;
            }
            QScrollBar:vertical {
                background: #2b2b2b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #0d7377;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #14a085;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    def create_header(self):
        """Create application header"""
        header = QFrame()
        header.setFrameShape(QFrame.Shape.StyledPanel)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0d7377, stop:1 #14a085);
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(header)
        
        title = QLabel("🚢 RC Cargo Barge - Hydrodynamic Analysis Dashboard")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff;")
        
        subtitle = QLabel("Universidad Militar Nueva Granada | Fluid Mechanics Project | ITTC-1957 Method")
        subtitle.setFont(QFont("Segoe UI", 9))
        subtitle.setStyleSheet("color: #e0e0e0;")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        return header

    def create_parameters_tab(self):
        """Create parameters input tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Scroll area for parameters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Hull geometry group
        hull_group = QGroupBox("🔧 Hull Geometry")
        hull_layout = QVBoxLayout()
        
        self.length_input = self.create_parameter_input("Total Length (m):", 0.45, 0.01, 2.0)
        self.beam_input = self.create_parameter_input("Beam (m):", 0.172, 0.01, 1.0)
        self.height_input = self.create_parameter_input("Height (m):", 0.156, 0.01, 1.0)
        self.bow_length_input = self.create_parameter_input("Bow Length (m):", 0.05, 0.01, 0.5)
        self.draft_input = self.create_parameter_input("Draft (m):", 0.055, 0.001, 0.5)
        
        hull_layout.addLayout(self.length_input[0])
        hull_layout.addLayout(self.beam_input[0])
        hull_layout.addLayout(self.height_input[0])
        hull_layout.addLayout(self.bow_length_input[0])
        hull_layout.addLayout(self.draft_input[0])
        hull_group.setLayout(hull_layout)
        
        # Mass distribution group
        mass_group = QGroupBox("⚖️ Mass Distribution")
        mass_layout = QVBoxLayout()
        
        self.hull_mass_input = self.create_parameter_input("Hull Mass (kg):", 1.2, 0.1, 10.0)
        self.electronics_mass_input = self.create_parameter_input("Electronics Mass (kg):", 1.0, 0.1, 10.0)
        self.cargo_mass_input = self.create_parameter_input("Cargo Mass (kg):", 2.5, 0.0, 20.0)
        
        mass_layout.addLayout(self.hull_mass_input[0])
        mass_layout.addLayout(self.electronics_mass_input[0])
        mass_layout.addLayout(self.cargo_mass_input[0])
        mass_group.setLayout(mass_layout)
        
        # Analysis parameters group
        analysis_group = QGroupBox("🔬 Analysis Parameters")
        analysis_layout = QVBoxLayout()
        
        self.velocity_input = self.create_parameter_input("Design Velocity (m/s):", 0.5, 0.1, 5.0)
        self.form_factor_input = self.create_parameter_input("Form Factor (k):", 0.2, 0.05, 0.5)
        
        analysis_layout.addLayout(self.velocity_input[0])
        analysis_layout.addLayout(self.form_factor_input[0])
        analysis_group.setLayout(analysis_layout)
        
        scroll_layout.addWidget(hull_group)
        scroll_layout.addWidget(mass_group)
        scroll_layout.addWidget(analysis_group)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.btn_run_stability = QPushButton("🔄 Run Stability Analysis")
        self.btn_run_stability.clicked.connect(self.run_stability_analysis)
        
        self.btn_run_resistance = QPushButton("🌊 Run Resistance Analysis")
        self.btn_run_resistance.clicked.connect(self.run_resistance_analysis)
        
        self.btn_run_all = QPushButton("⚡ Run Complete Analysis")
        self.btn_run_all.clicked.connect(self.run_complete_analysis)
        self.btn_run_all.setStyleSheet("""
            QPushButton {
                background-color: #e63946;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #ff4c5c;
            }
        """)
        
        button_layout.addWidget(self.btn_run_stability)
        button_layout.addWidget(self.btn_run_resistance)
        button_layout.addWidget(self.btn_run_all)
        
        layout.addLayout(button_layout)
        
        return tab

    def create_parameter_input(self, label_text, default_value, min_value, max_value):
        """Create a labeled parameter input"""
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setMinimumWidth(200)
        
        spinbox = QDoubleSpinBox()
        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setValue(default_value)
        spinbox.setDecimals(3)
        spinbox.setSingleStep(0.01)
        
        layout.addWidget(label)
        layout.addWidget(spinbox)
        layout.addStretch()
        
        return (layout, spinbox)

    def create_stability_tab(self):
        """Create stability analysis results tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Results display
        self.stability_results = QTextEdit()
        self.stability_results.setReadOnly(True)
        self.stability_results.setPlaceholderText("Run stability analysis to see results here...")
        
        # Matplotlib plot
        self.stability_plot = MatplotlibWidget()
        
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.stability_results)
        splitter.addWidget(self.stability_plot)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        
        return tab

    def create_resistance_tab(self):
        """Create resistance analysis results tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Results display
        self.resistance_results = QTextEdit()
        self.resistance_results.setReadOnly(True)
        self.resistance_results.setPlaceholderText("Run resistance analysis to see results here...")
        
        # Matplotlib plot
        self.resistance_plot = MatplotlibWidget()
        
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.resistance_results)
        splitter.addWidget(self.resistance_plot)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        
        return tab

    def create_3d_tab(self):
        """Create 3D visualization tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Matplotlib 3D plot
        self.plot_3d = MatplotlibWidget()
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.btn_generate_3d = QPushButton("🎨 Generate 3D Visualization")
        self.btn_generate_3d.clicked.connect(self.generate_3d_visualization)
        
        self.btn_export_3d = QPushButton("💾 Export Image")
        self.btn_export_3d.clicked.connect(self.export_3d_image)
        
        button_layout.addWidget(self.btn_generate_3d)
        button_layout.addWidget(self.btn_export_3d)
        button_layout.addStretch()
        
        layout.addWidget(self.plot_3d)
        layout.addLayout(button_layout)
        
        return tab

    def create_summary_tab(self):
        """Create summary report tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Summary text area
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setPlaceholderText("Complete analysis results will appear here...")
        
        # Export buttons
        button_layout = QHBoxLayout()
        
        self.btn_export_report = QPushButton("📄 Export Report (TXT)")
        self.btn_export_report.clicked.connect(self.export_report_txt)
        
        self.btn_export_json = QPushButton("📊 Export Data (JSON)")
        self.btn_export_json.clicked.connect(self.export_report_json)
        
        button_layout.addWidget(self.btn_export_report)
        button_layout.addWidget(self.btn_export_json)
        button_layout.addStretch()
        
        layout.addWidget(self.summary_text)
        layout.addLayout(button_layout)
        
        return tab

    def create_status_bar(self):
        """Create status bar with progress indicator"""
        status_widget = QFrame()
        status_widget.setFrameShape(QFrame.Shape.StyledPanel)
        status_widget.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
        layout = QHBoxLayout(status_widget)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #14a085; font-weight: bold;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMaximumWidth(300)
        
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.progress_bar)
        
        return status_widget

    def load_default_parameters(self):
        """Load default parameters into inputs"""
        # Already set in create_parameter_input default values
        pass

    def get_parameters_from_inputs(self):
        """Extract current parameters from input widgets"""
        return {
            'length': self.length_input[1].value(),
            'beam': self.beam_input[1].value(),
            'height': self.height_input[1].value(),
            'bow_length': self.bow_length_input[1].value(),
            'draft': self.draft_input[1].value(),
            'hull_mass': self.hull_mass_input[1].value(),
            'electronics_mass': self.electronics_mass_input[1].value(),
            'cargo_mass': self.cargo_mass_input[1].value(),
            'velocity': self.velocity_input[1].value(),
            'form_factor': self.form_factor_input[1].value(),
        }

    def run_stability_analysis(self):
        """Run stability analysis in worker thread"""
        params = self.get_parameters_from_inputs()
        
        self.worker = AnalysisWorker("stability", params)
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.display_stability_results)
        self.worker.error.connect(self.display_error)
        
        self.disable_buttons()
        self.worker.start()

    def run_resistance_analysis(self):
        """Run resistance analysis in worker thread"""
        params = self.get_parameters_from_inputs()
        params['wetted_area'] = 0.165  # Calculated area
        
        self.worker = AnalysisWorker("resistance", params)
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.display_resistance_results)
        self.worker.error.connect(self.display_error)
        
        self.disable_buttons()
        self.worker.start()

    def run_complete_analysis(self):
        """Run complete analysis suite"""
        params = self.get_parameters_from_inputs()
        
        self.worker = AnalysisWorker("complete", params)
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.display_complete_results)
        self.worker.error.connect(self.display_error)
        
        self.disable_buttons()
        self.worker.start()

    def generate_3d_visualization(self):
        """Generate 3D hull visualization"""
        params = self.get_parameters_from_inputs()
        
        self.worker = AnalysisWorker("3d_visualization", params)
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.display_3d_results)
        self.worker.error.connect(self.display_error)
        
        self.disable_buttons()
        self.worker.start()

    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)

    def update_status(self, message):
        """Update status label"""
        self.status_label.setText(message)

    def disable_buttons(self):
        """Disable action buttons during analysis"""
        self.btn_run_stability.setEnabled(False)
        self.btn_run_resistance.setEnabled(False)
        self.btn_run_all.setEnabled(False)
        self.btn_generate_3d.setEnabled(False)

    def enable_buttons(self):
        """Re-enable action buttons"""
        self.btn_run_stability.setEnabled(True)
        self.btn_run_resistance.setEnabled(True)
        self.btn_run_all.setEnabled(True)
        self.btn_generate_3d.setEnabled(True)

    def display_stability_results(self, results):
        """Display stability analysis results"""
        self.current_results['stability'] = results
        
        # Format text results
        text = "=" * 80 + "\n"
        text += "STABILITY ANALYSIS RESULTS\n"
        text += "=" * 80 + "\n\n"
        
        text += "HULL GEOMETRY\n"
        text += "-" * 80 + "\n"
        text += f"  Length:              {results['hull'].length:.3f} m\n"
        text += f"  Beam:                {results['hull'].beam:.3f} m\n"
        text += f"  Height:              {results['hull'].height:.3f} m\n"
        text += f"  Draft:               {results['hull'].draft:.3f} m\n"
        text += f"  Bow Length:          {results['hull'].bow_length:.3f} m\n\n"
        
        text += "HYDROSTATIC PROPERTIES\n"
        text += "-" * 80 + "\n"
        text += f"  Displacement Volume: {results['displacement']:.6f} m³\n"
        text += f"  Displacement Mass:   {results['displacement_mass']:.3f} kg\n"
        text += f"  Waterplane Area:     {results['aw']:.4f} m²\n\n"
        
        text += "FLOTATION ANALYSIS\n"
        text += "-" * 80 + "\n"
        text += f"  Buoyancy Force:      {results['buoyancy_force']:.2f} N ↑\n"
        text += f"  Weight Force:        {results['weight_force']:.2f} N ↓\n"
        text += f"  Net Force:           {results['net_force']:.2f} N\n"
        floats_text = "✓ FLOATS" if results['floats'] else "✗ SINKS"
        text += f"  Status:              {floats_text}\n\n"
        
        text += "STABILITY PARAMETERS\n"
        text += "-" * 80 + "\n"
        text += f"  KB (Center of Buoyancy):    {results['kb']*100:.2f} cm\n"
        text += f"  BM (Metacentric Radius):    {results['bm']*100:.2f} cm\n"
        text += f"  KG (Center of Gravity):     {results['kg']*100:.2f} cm\n"
        text += f"  GM (Metacentric Height):    {results['gm']*100:.2f} cm\n"
        
        if results['gm'] < 0:
            text += "  Rating: ✗ UNSTABLE\n"
        elif results['gm'] < 0.05:
            text += "  Rating: ⚠ MARGINAL\n"
        else:
            text += "  Rating: ✓ STABLE\n"
        
        self.stability_results.setText(text)
        
        # Plot results
        self.plot_stability_results(results)
        
        # Switch to stability tab
        self.tabs.setCurrentIndex(1)
        
        self.enable_buttons()
        self.update_status("Stability analysis complete!")
        self.progress_bar.setValue(0)

    def plot_stability_results(self, results):
        """Plot stability visualization"""
        self.stability_plot.clear()
        fig = self.stability_plot.figure
        
        # Create subplots
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        # Plot 1: Centers vertical position
        centers = ['KB', 'KG', 'KM']
        values = [results['kb'], results['kg'], results['kb'] + results['bm']]
        colors = ['#0d7377', '#e63946', '#14a085']
        
        ax1.barh(centers, values, color=colors, alpha=0.8)
        ax1.set_xlabel('Height from Keel (m)', color='#e0e0e0')
        ax1.set_title('Stability Centers', color='#14a085', fontweight='bold')
        ax1.grid(True, alpha=0.3, color='#3d3d3d')
        ax1.set_facecolor('#1e1e1e')
        ax1.tick_params(colors='#e0e0e0')
        ax1.spines['bottom'].set_color('#3d3d3d')
        ax1.spines['left'].set_color('#3d3d3d')
        ax1.spines['top'].set_color('#3d3d3d')
        ax1.spines['right'].set_color('#3d3d3d')
        
        # Plot 2: Mass distribution
        masses = ['Hull', 'Electronics', 'Cargo']
        mass_values = [
            results['hull'].bow_length,  # Using hull param as placeholder
            1.0,
            2.5
        ]
        
        ax2.pie(mass_values, labels=masses, autopct='%1.1f%%',
                colors=['#0d7377', '#14a085', '#e63946'],
                textprops={'color': '#e0e0e0'})
        ax2.set_title('Mass Distribution', color='#14a085', fontweight='bold')
        ax2.set_facecolor('#1e1e1e')
        
        fig.tight_layout()
        self.stability_plot.canvas.draw()

    def display_resistance_results(self, results):
        """Display resistance analysis results"""
        self.current_results['resistance'] = results
        
        # Format text results
        text = "=" * 80 + "\n"
        text += "RESISTANCE ANALYSIS RESULTS (ITTC-1957)\n"
        text += "=" * 80 + "\n\n"
        
        # Find design velocity results
        design_v = self.velocity_input[1].value()
        idx = np.argmin(np.abs(np.array(results['velocities']) - design_v))
        
        text += f"DESIGN VELOCITY: {design_v:.2f} m/s\n"
        text += "-" * 80 + "\n"
        text += f"  Reynolds Number:     {results['reynolds'][idx]:.2e}\n"
        text += f"  Froude Number:       {results['froude'][idx]:.3f}\n"
        text += f"  Friction Coeff (Cf): {results['cf'][idx]:.5f}\n"
        text += f"  Total Resistance:    {results['resistance'][idx]:.3f} N\n"
        text += f"  Effective Power:     {results['power'][idx]:.3f} W\n\n"
        
        text += "VELOCITY RANGE ANALYSIS\n"
        text += "-" * 80 + "\n"
        text += f"  Min Velocity:        {results['velocities'][0]:.2f} m/s\n"
        text += f"  Max Velocity:        {results['velocities'][-1]:.2f} m/s\n"
        text += f"  Min Resistance:      {min(results['resistance']):.3f} N\n"
        text += f"  Max Resistance:      {max(results['resistance']):.3f} N\n"
        text += f"  Min Power:           {min(results['power']):.3f} W\n"
        text += f"  Max Power:           {max(results['power']):.3f} W\n"
        
        self.resistance_results.setText(text)
        
        # Plot results
        self.plot_resistance_results(results)
        
        # Switch to resistance tab
        self.tabs.setCurrentIndex(2)
        
        self.enable_buttons()
        self.update_status("Resistance analysis complete!")
        self.progress_bar.setValue(0)

    def plot_resistance_results(self, results):
        """Plot resistance curves"""
        self.resistance_plot.clear()
        fig = self.resistance_plot.figure
        
        # Create subplots
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(223)
        ax4 = fig.add_subplot(224)
        
        v = results['velocities']
        
        # Plot 1: Resistance vs Velocity
        ax1.plot(v, results['resistance'], color='#0d7377', linewidth=2)
        ax1.set_xlabel('Velocity (m/s)', color='#e0e0e0')
        ax1.set_ylabel('Resistance (N)', color='#e0e0e0')
        ax1.set_title('Total Resistance', color='#14a085', fontweight='bold')
        ax1.grid(True, alpha=0.3, color='#3d3d3d')
        ax1.set_facecolor('#1e1e1e')
        ax1.tick_params(colors='#e0e0e0')
        
        # Plot 2: Power vs Velocity
        ax2.plot(v, results['power'], color='#e63946', linewidth=2)
        ax2.set_xlabel('Velocity (m/s)', color='#e0e0e0')
        ax2.set_ylabel('Power (W)', color='#e0e0e0')
        ax2.set_title('Effective Power', color='#14a085', fontweight='bold')
        ax2.grid(True, alpha=0.3, color='#3d3d3d')
        ax2.set_facecolor('#1e1e1e')
        ax2.tick_params(colors='#e0e0e0')
        
        # Plot 3: Reynolds Number
        ax3.plot(v, results['reynolds'], color='#14a085', linewidth=2)
        ax3.set_xlabel('Velocity (m/s)', color='#e0e0e0')
        ax3.set_ylabel('Reynolds Number', color='#e0e0e0')
        ax3.set_title('Reynolds Number', color='#14a085', fontweight='bold')
        ax3.grid(True, alpha=0.3, color='#3d3d3d')
        ax3.set_facecolor('#1e1e1e')
        ax3.tick_params(colors='#e0e0e0')
        ax3.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        # Plot 4: Froude Number
        ax4.plot(v, results['froude'], color='#ffa500', linewidth=2)
        ax4.axhline(y=0.4, color='#e63946', linestyle='--', label='Fr=0.4 (displacement limit)')
        ax4.set_xlabel('Velocity (m/s)', color='#e0e0e0')
        ax4.set_ylabel('Froude Number', color='#e0e0e0')
        ax4.set_title('Froude Number', color='#14a085', fontweight='bold')
        ax4.grid(True, alpha=0.3, color='#3d3d3d')
        ax4.set_facecolor('#1e1e1e')
        ax4.tick_params(colors='#e0e0e0')
        ax4.legend(facecolor='#2b2b2b', edgecolor='#3d3d3d', labelcolor='#e0e0e0')
        
        for ax in [ax1, ax2, ax3, ax4]:
            for spine in ax.spines.values():
                spine.set_color('#3d3d3d')
        
        fig.tight_layout()
        self.resistance_plot.canvas.draw()

    def display_3d_results(self, results):
        """Display 3D visualization"""
        self.current_results['3d'] = results
        
        self.plot_3d.clear()
        fig = self.plot_3d.figure
        ax = fig.add_subplot(111, projection='3d')
        
        vertices = results['vertices']
        faces = results['faces']
        
        # Plot hull mesh
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        
        # Create face vertices list (faces is a list of vertex indices)
        face_vertices = [[vertices[idx] for idx in face] for face in faces]
        
        hull_collection = Poly3DCollection(
            face_vertices,
            alpha=0.7,
            facecolor='#0d7377',
            edgecolor='#14a085',
            linewidths=1
        )
        ax.add_collection3d(hull_collection)  # type: ignore
        
        # Set equal aspect ratio
        max_range = np.array([
            vertices[:, 0].max() - vertices[:, 0].min(),
            vertices[:, 1].max() - vertices[:, 1].min(),
            vertices[:, 2].max() - vertices[:, 2].min()
        ]).max() / 2.0
        
        mid_x = (vertices[:, 0].max() + vertices[:, 0].min()) * 0.5
        mid_y = (vertices[:, 1].max() + vertices[:, 1].min()) * 0.5
        mid_z = (vertices[:, 2].max() + vertices[:, 2].min()) * 0.5
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)  # type: ignore
        
        ax.set_xlabel('Length (m)', color='#e0e0e0')
        ax.set_ylabel('Beam (m)', color='#e0e0e0')
        ax.set_zlabel('Height (m)', color='#e0e0e0')  # type: ignore
        ax.set_title('3D Hull Geometry (Pyramidal Bow + Rectangular Stern)',
                     color='#14a085', fontweight='bold', pad=20)
        
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#1e1e1e')
        ax.tick_params(colors='#e0e0e0')
        ax.xaxis.pane.fill = False  # type: ignore
        ax.yaxis.pane.fill = False  # type: ignore
        ax.zaxis.pane.fill = False  # type: ignore
        ax.grid(color='#3d3d3d', alpha=0.3)
        
        self.plot_3d.canvas.draw()
        
        self.tabs.setCurrentIndex(3)
        
        self.enable_buttons()
        self.update_status("3D visualization complete!")
        self.progress_bar.setValue(0)

    def display_complete_results(self, results):
        """Display complete analysis results"""
        self.current_results = results
        
        # Display individual results
        if 'stability' in results:
            self.display_stability_results(results['stability'])
        if 'resistance' in results:
            self.display_resistance_results(results['resistance'])
        if '3d' in results:
            self.display_3d_results(results['3d'])
        
        # Generate summary report
        summary = self.generate_summary_report(results)
        self.summary_text.setText(summary)
        
        # Switch to summary tab
        self.tabs.setCurrentIndex(4)
        
        self.enable_buttons()
        self.update_status("Complete analysis finished!")
        self.progress_bar.setValue(0)

    def generate_summary_report(self, results):
        """Generate comprehensive summary report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = "=" * 90 + "\n"
        report += "RC CARGO BARGE - COMPREHENSIVE ANALYSIS REPORT\n"
        report += "=" * 90 + "\n\n"
        report += f"Generated: {timestamp}\n"
        report += "Universidad Militar Nueva Granada | Fluid Mechanics Project\n\n"
        
        if 'stability' in results:
            stab = results['stability']
            report += "HULL SPECIFICATIONS\n"
            report += "-" * 90 + "\n"
            report += f"  Total Length:          {stab['hull'].length:.3f} m\n"
            report += f"  Beam:                  {stab['hull'].beam:.3f} m\n"
            report += f"  Height:                {stab['hull'].height:.3f} m\n"
            report += f"  Draft:                 {stab['hull'].draft:.3f} m\n"
            report += f"  Bow Length (pyramid):  {stab['hull'].bow_length:.3f} m\n"
            report += f"  Stern Length (rect):   {stab['hull'].length - stab['hull'].bow_length:.3f} m\n\n"
            
            report += "MASS DISTRIBUTION\n"
            report += "-" * 90 + "\n"
            report += f"  Hull:                  {stab['total_mass'] - 3.5:.2f} kg\n"
            report += f"  Electronics:           1.00 kg\n"
            report += f"  Cargo:                 2.50 kg\n"
            report += f"  TOTAL:                 {stab['total_mass']:.2f} kg\n\n"
            
            report += "STABILITY ANALYSIS\n"
            report += "-" * 90 + "\n"
            report += f"  Displacement:          {stab['displacement_mass']:.3f} kg\n"
            report += f"  KB:                    {stab['kb']*100:.2f} cm\n"
            report += f"  BM:                    {stab['bm']*100:.2f} cm\n"
            report += f"  KG:                    {stab['kg']*100:.2f} cm\n"
            report += f"  GM:                    {stab['gm']*100:.2f} cm "
            if stab['gm'] < 0:
                report += "✗ UNSTABLE\n"
            elif stab['gm'] < 0.05:
                report += "⚠ MARGINAL\n"
            else:
                report += "✓ STABLE\n"
            
            report += f"\n  Buoyancy Force:        {stab['buoyancy_force']:.2f} N ↑\n"
            report += f"  Weight Force:          {stab['weight_force']:.2f} N ↓\n"
            report += f"  Net Force:             {stab['net_force']:.2f} N\n"
            report += f"  Flotation Status:      {'✓ FLOATS' if stab['floats'] else '✗ SINKS'}\n\n"
        
        if 'resistance' in results:
            res = results['resistance']
            design_v = self.velocity_input[1].value()
            idx = np.argmin(np.abs(np.array(res['velocities']) - design_v))
            
            report += "HYDRODYNAMIC PERFORMANCE (ITTC-1957)\n"
            report += "-" * 90 + "\n"
            report += f"  Design Velocity:       {design_v:.2f} m/s\n"
            report += f"  Reynolds Number:       {res['reynolds'][idx]:.2e}\n"
            report += f"  Froude Number:         {res['froude'][idx]:.3f} "
            if res['froude'][idx] < 0.4:
                report += "(Displacement mode)\n"
            else:
                report += "(Planing mode)\n"
            report += f"  Friction Coefficient:  {res['cf'][idx]:.5f}\n"
            report += f"  Total Resistance:      {res['resistance'][idx]:.3f} N\n"
            report += f"  Effective Power:       {res['power'][idx]:.3f} W\n"
            report += f"  Shaft Power (η=0.38):  {res['power'][idx]/0.38:.3f} W\n\n"
        
        report += "DESIGN COMPLIANCE\n"
        report += "-" * 90 + "\n"
        if 'stability' in results:
            draft_ok = "✓" if stab['hull'].draft <= 0.06 else "✗"
            report += f"  Draft < 6 cm           {draft_ok} ({stab['hull'].draft*100:.1f} cm)\n"
            cargo_ok = "✓" if stab['total_mass'] >= 4.0 else "✗"
            report += f"  Cargo ≥ 1.5 kg         {cargo_ok} ({stab['total_mass'] - 2.2:.1f} kg cargo)\n"
            gm_ok = "✓" if stab['gm'] > 0.05 else "⚠"
            report += f"  GM > 5 cm              {gm_ok} ({stab['gm']*100:.1f} cm)\n"
        if 'resistance' in results:
            power_ok = "✓" if res['power'][idx]/0.38 < 75 else "✗"
            report += f"  Power < 75 W           {power_ok} ({res['power'][idx]/0.38:.1f} W)\n"
        
        report += "\n" + "=" * 90 + "\n"
        report += "END OF REPORT\n"
        report += "=" * 90 + "\n"
        
        return report

    def display_error(self, error_message):
        """Display error message"""
        QMessageBox.critical(self, "Analysis Error", f"An error occurred:\n\n{error_message}")
        self.enable_buttons()
        self.update_status("Error occurred!")
        self.progress_bar.setValue(0)

    def export_3d_image(self):
        """Export 3D visualization as image"""
        if '3d' not in self.current_results:
            QMessageBox.warning(self, "No Data", "Please generate 3D visualization first!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save 3D Visualization",
            f"hull_3d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            "PNG Image (*.png);;All Files (*)"
        )
        
        if filename:
            self.plot_3d.figure.savefig(filename, dpi=300, facecolor='#1e1e1e')
            QMessageBox.information(self, "Success", f"Image saved to:\n{filename}")

    def export_report_txt(self):
        """Export summary report as text file"""
        if not self.current_results:
            QMessageBox.warning(self, "No Data", "Please run analysis first!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text File (*.txt);;All Files (*)"
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.summary_text.toPlainText())
            QMessageBox.information(self, "Success", f"Report saved to:\n{filename}")

    def export_report_json(self):
        """Export analysis data as JSON"""
        if not self.current_results:
            QMessageBox.warning(self, "No Data", "Please run analysis first!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Data",
            f"analysis_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON File (*.json);;All Files (*)"
        )
        
        if filename:
            # Convert numpy arrays to lists for JSON serialization
            export_data = {}
            
            if 'stability' in self.current_results:
                stab = self.current_results['stability']
                export_data['stability'] = {
                    'displacement': float(stab['displacement']),
                    'kb': float(stab['kb']),
                    'bm': float(stab['bm']),
                    'kg': float(stab['kg']),
                    'gm': float(stab['gm']),
                    'buoyancy_force': float(stab['buoyancy_force']),
                    'weight_force': float(stab['weight_force']),
                    'floats': bool(stab['floats'])
                }
            
            if 'resistance' in self.current_results:
                res = self.current_results['resistance']
                export_data['resistance'] = {
                    'velocities': [float(v) for v in res['velocities']],
                    'reynolds': [float(r) for r in res['reynolds']],
                    'froude': [float(f) for f in res['froude']],
                    'resistance': [float(r) for r in res['resistance']],
                    'power': [float(p) for p in res['power']]
                }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            QMessageBox.information(self, "Success", f"Data saved to:\n{filename}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("RC Barge Analysis Dashboard")
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
