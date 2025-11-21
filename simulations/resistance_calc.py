#!/usr/bin/env python3
"""
ITTC-1957 Resistance Calculation for RC Cargo Barge
Universidad Militar Nueva Granada - Fluid Mechanics Course

This script calculates hydrodynamic resistance using the ITTC-1957 friction line
and estimates power requirements for various velocities.

Usage:
    python resistance_calc.py --length 0.45 --velocity 0.5 --wetted_area 0.18
    python resistance_calc.py --config hull_v2.json --velocity_range 0.2 0.8 0.1
"""

import argparse
import json
import math
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class HullParameters:
    """Hull geometry and parameters"""
    length: float  # Waterline length (m)
    beam: float    # Beam at waterline (m)
    draft: float   # Draft at design condition (m)
    wetted_area: float  # Wetted surface area (m²)
    form_factor: float = 0.2  # Form factor k (0.1-0.3 typical)
    block_coeff: float = 0.85  # Block coefficient
    prismatic_coeff: float = 0.80  # Prismatic coefficient
    
    
@dataclass
class FluidProperties:
    """Water properties"""
    density: float = 1000.0  # kg/m³
    kinematic_viscosity: float = 1.004e-6  # m²/s at 20°C
    gravity: float = 9.81  # m/s²
    

@dataclass
class ResistanceComponents:
    """Breakdown of resistance forces"""
    velocity: float
    reynolds: float
    froude: float
    friction_coeff: float
    friction_resistance: float
    viscous_resistance: float
    wave_resistance: float
    total_resistance: float
    effective_power: float
    

class ITTCResistanceCalculator:
    """Calculate ship resistance using ITTC-1957 method"""
    
    def __init__(self, hull: HullParameters, fluid: FluidProperties):
        self.hull = hull
        self.fluid = fluid
        
    def reynolds_number(self, velocity: float) -> float:
        """Calculate Reynolds number: Re = VL/ν"""
        return (velocity * self.hull.length) / self.fluid.kinematic_viscosity
    
    def froude_number(self, velocity: float) -> float:
        """Calculate Froude number: Fr = V/√(gL)"""
        return velocity / math.sqrt(self.fluid.gravity * self.hull.length)
    
    def ittc_friction_coefficient(self, reynolds: float) -> float:
        """
        ITTC-1957 friction line: Cf = 0.075 / (log10(Re) - 2)²
        Valid for Re > 10⁶ originally, but used for scale models
        """
        if reynolds < 1e4:
            raise ValueError(f"Reynolds number {reynolds:.2e} too low for ITTC method")
        
        log_re = math.log10(reynolds)
        return 0.075 / ((log_re - 2) ** 2)
    
    def friction_resistance(self, velocity: float, cf: float) -> float:
        """Friction resistance: Rf = 0.5 * ρ * V² * S * Cf"""
        return 0.5 * self.fluid.density * velocity**2 * self.hull.wetted_area * cf
    
    def viscous_resistance(self, friction_resistance: float) -> float:
        """Viscous resistance including form factor: Rv = (1 + k) * Rf"""
        return (1 + self.hull.form_factor) * friction_resistance
    
    def wave_resistance(self, velocity: float, froude: float) -> float:
        """
        Simplified wave resistance estimation
        For displacement hulls (Fr < 0.4): Rw ≈ 0.2 * Rv
        For transition (0.4 < Fr < 0.5): Rw increases significantly
        """
        if froude < 0.3:
            wave_factor = 0.1
        elif froude < 0.4:
            wave_factor = 0.2
        elif froude < 0.5:
            wave_factor = 0.5
        else:
            # Planing regime - simplified model
            wave_factor = 1.0
        
        # Wave resistance proportional to velocity^4 for simplicity
        base_wave = 0.01 * self.fluid.density * velocity**4 * self.hull.beam
        return wave_factor * base_wave
    
    def air_resistance(self, velocity: float) -> float:
        """
        Air resistance (typically negligible for small scale models)
        Ra = 0.5 * ρ_air * V² * A_frontal * Cd
        """
        rho_air = 1.225  # kg/m³
        frontal_area = self.hull.beam * 0.05  # Estimated above-water profile
        drag_coeff = 0.8  # Bluff body
        return 0.5 * rho_air * velocity**2 * frontal_area * drag_coeff
    
    def calculate_resistance(self, velocity: float) -> ResistanceComponents:
        """Calculate all resistance components at given velocity"""
        
        # Dimensionless numbers
        re = self.reynolds_number(velocity)
        fr = self.froude_number(velocity)
        
        # Friction
        cf = self.ittc_friction_coefficient(re)
        rf = self.friction_resistance(velocity, cf)
        
        # Viscous
        rv = self.viscous_resistance(rf)
        
        # Wave
        rw = self.wave_resistance(velocity, fr)
        
        # Air (small, often neglected)
        ra = self.air_resistance(velocity)
        
        # Total
        rt = rv + rw + ra
        
        # Effective power
        pe = rt * velocity
        
        return ResistanceComponents(
            velocity=velocity,
            reynolds=re,
            froude=fr,
            friction_coeff=cf,
            friction_resistance=rf,
            viscous_resistance=rv,
            wave_resistance=rw,
            total_resistance=rt,
            effective_power=pe
        )
    
    def power_curve(self, velocities: List[float]) -> List[ResistanceComponents]:
        """Calculate resistance at multiple velocities"""
        return [self.calculate_resistance(v) for v in velocities]
    
    def shaft_power(self, effective_power: float, efficiency: float = 0.5) -> float:
        """Convert effective power to shaft power: P_shaft = P_e / η_total"""
        return effective_power / efficiency
    

def plot_results(results: List[ResistanceComponents], hull: HullParameters, save_path: str = None):
    """Generate comprehensive plots of resistance analysis"""
    
    velocities = [r.velocity for r in results]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'ITTC-1957 Resistance Analysis - L={hull.length}m, S={hull.wetted_area}m²', 
                 fontsize=14, fontweight='bold')
    
    # Plot 1: Resistance components vs velocity
    ax1 = axes[0, 0]
    ax1.plot(velocities, [r.friction_resistance for r in results], 'b-', label='Friction (Rf)', linewidth=2)
    ax1.plot(velocities, [r.viscous_resistance for r in results], 'g-', label='Viscous (Rv)', linewidth=2)
    ax1.plot(velocities, [r.wave_resistance for r in results], 'r-', label='Wave (Rw)', linewidth=2)
    ax1.plot(velocities, [r.total_resistance for r in results], 'k--', label='Total (RT)', linewidth=2.5)
    ax1.set_xlabel('Velocity (m/s)', fontweight='bold')
    ax1.set_ylabel('Resistance (N)', fontweight='bold')
    ax1.set_title('Resistance Components')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Power requirements
    ax2 = axes[0, 1]
    pe_values = [r.effective_power for r in results]
    p_shaft_50 = [p / 0.5 for p in pe_values]
    p_shaft_40 = [p / 0.4 for p in pe_values]
    
    ax2.plot(velocities, pe_values, 'b-', label='Effective Power (PE)', linewidth=2)
    ax2.plot(velocities, p_shaft_50, 'g--', label='Shaft Power (η=50%)', linewidth=2)
    ax2.plot(velocities, p_shaft_40, 'r:', label='Shaft Power (η=40%)', linewidth=2)
    ax2.axhline(y=75, color='purple', linestyle='-.', label='Power Limit (75W)', linewidth=2)
    ax2.set_xlabel('Velocity (m/s)', fontweight='bold')
    ax2.set_ylabel('Power (W)', fontweight='bold')
    ax2.set_title('Power Requirements')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Reynolds number
    ax3 = axes[1, 0]
    ax3.plot(velocities, [r.reynolds for r in results], 'b-', linewidth=2)
    ax3.set_xlabel('Velocity (m/s)', fontweight='bold')
    ax3.set_ylabel('Reynolds Number', fontweight='bold')
    ax3.set_title('Reynolds Number vs Velocity')
    ax3.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Froude number and regime
    ax4 = axes[1, 1]
    ax4.plot(velocities, [r.froude for r in results], 'r-', linewidth=2)
    ax4.axhline(y=0.4, color='orange', linestyle='--', label='Displacement limit (Fr=0.4)', linewidth=2)
    ax4.fill_between(velocities, 0, 0.4, alpha=0.2, color='green', label='Displacement mode')
    ax4.fill_between(velocities, 0.4, max([r.froude for r in results]), alpha=0.2, color='yellow', label='Transition')
    ax4.set_xlabel('Velocity (m/s)', fontweight='bold')
    ax4.set_ylabel('Froude Number', fontweight='bold')
    ax4.set_title('Froude Number and Operating Regime')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    plt.show()


def print_summary(results: List[ResistanceComponents], hull: HullParameters):
    """Print formatted summary table"""
    
    print("\n" + "="*100)
    print(f"{'ITTC-1957 RESISTANCE CALCULATION SUMMARY':^100}")
    print("="*100)
    print(f"\nHull Parameters:")
    print(f"  Length (L):        {hull.length:.3f} m")
    print(f"  Beam (B):          {hull.beam:.3f} m")
    print(f"  Draft (T):         {hull.draft:.3f} m")
    print(f"  Wetted Area (S):   {hull.wetted_area:.3f} m²")
    print(f"  Form Factor (k):   {hull.form_factor:.2f}")
    print("\n" + "-"*100)
    print(f"{'V (m/s)':>8} {'Re':>12} {'Fr':>8} {'Cf':>10} {'Rf (N)':>10} {'Rv (N)':>10} {'Rw (N)':>10} {'RT (N)':>10} {'PE (W)':>10}")
    print("-"*100)
    
    for r in results:
        print(f"{r.velocity:8.2f} {r.reynolds:12.2e} {r.froude:8.3f} {r.friction_coeff:10.6f} "
              f"{r.friction_resistance:10.3f} {r.viscous_resistance:10.3f} {r.wave_resistance:10.3f} "
              f"{r.total_resistance:10.3f} {r.effective_power:10.3f}")
    
    print("-"*100)
    
    # Find optimal velocity (minimum specific resistance)
    specific_resistances = [(r.velocity, r.total_resistance / r.velocity) for r in results if r.velocity > 0]
    optimal = min(specific_resistances, key=lambda x: x[1])
    print(f"\nOptimal velocity (minimum RT/V): {optimal[0]:.2f} m/s")
    
    # Check power limit compliance
    print(f"\nPower Limit Check (75W @ η=50%):")
    for r in results:
        shaft_power = r.effective_power / 0.5
        status = "✓ OK" if shaft_power < 75 else "✗ EXCEEDS"
        print(f"  V={r.velocity:.2f} m/s → P_shaft={shaft_power:.2f} W {status}")
    
    print("\n" + "="*100 + "\n")


def main():
    parser = argparse.ArgumentParser(description='ITTC-1957 Resistance Calculator')
    parser.add_argument('--length', type=float, default=0.40, help='Waterline length (m)')
    parser.add_argument('--beam', type=float, default=0.172, help='Beam (m)')
    parser.add_argument('--draft', type=float, default=0.055, help='Draft (m)')
    parser.add_argument('--wetted_area', type=float, default=0.1258, help='Wetted surface area (m²)')
    parser.add_argument('--form_factor', type=float, default=0.25, help='Form factor k')
    parser.add_argument('--velocity', type=float, default=None, help='Single velocity to analyze (m/s)')
    parser.add_argument('--v_min', type=float, default=0.1, help='Minimum velocity for range (m/s)')
    parser.add_argument('--v_max', type=float, default=1.0, help='Maximum velocity for range (m/s)')
    parser.add_argument('--v_step', type=float, default=0.05, help='Velocity step (m/s)')
    parser.add_argument('--plot', action='store_true', help='Generate plots')
    parser.add_argument('--save_plot', type=str, default='resistance_analysis.png', help='Plot filename')
    parser.add_argument('--export_csv', type=str, default=None, help='Export results to CSV')
    
    args = parser.parse_args()
    
    # Setup hull and fluid
    hull = HullParameters(
        length=args.length,
        beam=args.beam,
        draft=args.draft,
        wetted_area=args.wetted_area,
        form_factor=args.form_factor
    )
    
    fluid = FluidProperties()
    
    calculator = ITTCResistanceCalculator(hull, fluid)
    
    # Calculate resistance
    if args.velocity is not None:
        results = [calculator.calculate_resistance(args.velocity)]
    else:
        velocities = np.arange(args.v_min, args.v_max + args.v_step, args.v_step)
        results = calculator.power_curve(velocities.tolist())
    
    # Print summary
    print_summary(results, hull)
    
    # Export CSV if requested
    if args.export_csv:
        import csv
        with open(args.export_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Velocity (m/s)', 'Reynolds', 'Froude', 'Cf', 'Rf (N)', 'Rv (N)', 
                           'Rw (N)', 'RT (N)', 'PE (W)', 'P_shaft_50% (W)', 'P_shaft_40% (W)'])
            for r in results:
                writer.writerow([r.velocity, r.reynolds, r.froude, r.friction_coeff,
                               r.friction_resistance, r.viscous_resistance, r.wave_resistance,
                               r.total_resistance, r.effective_power, 
                               r.effective_power/0.5, r.effective_power/0.4])
        print(f"Results exported to: {args.export_csv}")
    
    # Generate plots
    if args.plot and len(results) > 1:
        plot_results(results, hull, args.save_plot if args.save_plot else None)


if __name__ == "__main__":
    main()
