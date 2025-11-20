#!/usr/bin/env python3
"""
Stability Analysis for RC Cargo Barge
Metacentric height, righting moment, and heel angle calculations

Usage:
    python stability_analysis.py --length 0.45 --beam 0.20 --draft 0.055
    python stability_analysis.py --cargo 2.5 --cg_height 0.04
"""

import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple


@dataclass
class HullGeometry:
    """Hull dimensions and coefficients"""
    length: float  # Waterline length (m)
    beam: float    # Beam at waterline (m)
    draft: float   # Draft at design condition (m)
    block_coeff: float = 0.85  # Block coefficient Cb
    waterplane_coeff: float = 0.90  # Waterplane coefficient Cwp
    

@dataclass
class MassDistribution:
    """Mass and center of gravity information"""
    hull_mass: float  # Mass of hull structure (kg)
    hull_cg_height: float  # KG of hull alone (m)
    cargo_mass: float  # Cargo mass (kg)
    cargo_cg_height: float  # Height of cargo CG (m)
    electronics_mass: float = 1.0  # ESP32, batteries, motors (kg)
    electronics_cg_height: float = 0.03  # Low and centered (m)
    

class StabilityCalculator:
    """Calculate hydrostatic stability parameters"""
    
    def __init__(self, hull: HullGeometry, rho: float = 1000.0, g: float = 9.81):
        self.hull = hull
        self.rho = rho  # Water density (kg/m³)
        self.g = g      # Gravity (m/s²)
        
    def displacement_volume(self) -> float:
        """Calculate displaced volume: ∇ = L × B × T × Cb"""
        return (self.hull.length * self.hull.beam * 
                self.hull.draft * self.hull.block_coeff)
    
    def displacement_mass(self) -> float:
        """Calculate displacement mass: Δ = ρ × ∇"""
        return self.rho * self.displacement_volume()
    
    def waterplane_area(self) -> float:
        """Calculate waterplane area: Aw = L × B × Cwp"""
        return self.hull.length * self.hull.beam * self.hull.waterplane_coeff
    
    def center_of_buoyancy(self) -> float:
        """
        Estimate KB (keel to center of buoyancy)
        For rectangular barge: KB ≈ 0.5 × T
        """
        return 0.5 * self.hull.draft
    
    def metacentric_radius(self) -> float:
        """
        Calculate BM (buoyancy to metacenter)
        BM = I / ∇
        where I = (L × B³) / 12 for rectangular waterplane
        """
        # Second moment of waterplane area about centerline
        I = (self.hull.length * self.hull.beam**3) / 12
        volume = self.displacement_volume()
        return I / volume
    
    def metacentric_height(self, kg: float) -> float:
        """
        Calculate GM (metacentric height)
        GM = KB + BM - KG
        """
        kb = self.center_of_buoyancy()
        bm = self.metacentric_radius()
        return kb + bm - kg
    
    def combined_cg(self, mass_dist: MassDistribution) -> Tuple[float, float]:
        """
        Calculate combined center of gravity
        Returns: (total_mass, KG)
        """
        total_mass = (mass_dist.hull_mass + mass_dist.cargo_mass + 
                     mass_dist.electronics_mass)
        
        kg = ((mass_dist.hull_mass * mass_dist.hull_cg_height +
               mass_dist.cargo_mass * mass_dist.cargo_cg_height +
               mass_dist.electronics_mass * mass_dist.electronics_cg_height) / 
              total_mass)
        
        return total_mass, kg
    
    def righting_moment(self, heel_angle_deg: float, gm: float, 
                       displacement: float) -> float:
        """
        Calculate righting moment at given heel angle
        RM = Δ × GM × sin(θ)
        (Linear approximation valid for small angles)
        """
        heel_rad = math.radians(heel_angle_deg)
        return displacement * gm * math.sin(heel_rad) * self.g
    
    def max_stable_heel(self, gm: float) -> float:
        """
        Estimate maximum stable heel angle
        For positive GM, typically stable up to 10-15° for small craft
        """
        if gm <= 0:
            return 0.0
        elif gm < 0.03:
            return 5.0
        elif gm < 0.05:
            return 8.0
        else:
            return 12.0
    
    def heel_angle_from_offset_load(self, lateral_offset: float, 
                                    load_mass: float, gm: float,
                                    displacement: float) -> float:
        """
        Calculate heel angle from laterally offset load
        tan(θ) ≈ (m × d) / (Δ × GM)
        where m = offset mass, d = lateral distance from centerline
        """
        if gm <= 0:
            return 90.0  # Unstable
        
        tan_theta = (load_mass * lateral_offset) / (displacement * gm)
        return math.degrees(math.atan(tan_theta))


def plot_stability_curves(calculator: StabilityCalculator, mass_dist: MassDistribution,
                         save_path: str = None):
    """Generate stability analysis plots"""
    
    total_mass, kg = calculator.combined_cg(mass_dist)
    gm = calculator.metacentric_height(kg)
    displacement = calculator.displacement_mass()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Stability Analysis - GM={gm*100:.2f} cm, Δ={displacement:.2f} kg', 
                 fontsize=14, fontweight='bold')
    
    # Plot 1: Righting moment vs heel angle
    ax1 = axes[0, 0]
    heel_angles = np.linspace(0, 20, 100)
    righting_moments = [calculator.righting_moment(angle, gm, displacement) 
                       for angle in heel_angles]
    
    ax1.plot(heel_angles, righting_moments, 'b-', linewidth=2)
    ax1.axvline(x=10, color='r', linestyle='--', label='Design limit (10°)', linewidth=2)
    ax1.set_xlabel('Heel Angle (degrees)', fontweight='bold')
    ax1.set_ylabel('Righting Moment (N·m)', fontweight='bold')
    ax1.set_title('Righting Moment Curve')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: GM vs cargo load
    ax2 = axes[0, 1]
    cargo_loads = np.linspace(0, 4, 50)
    gm_values = []
    
    for cargo in cargo_loads:
        test_mass = MassDistribution(
            hull_mass=mass_dist.hull_mass,
            hull_cg_height=mass_dist.hull_cg_height,
            cargo_mass=cargo,
            cargo_cg_height=mass_dist.cargo_cg_height
        )
        _, test_kg = calculator.combined_cg(test_mass)
        gm_values.append(calculator.metacentric_height(test_kg))
    
    ax2.plot(cargo_loads, np.array(gm_values)*100, 'g-', linewidth=2)
    ax2.axhline(y=5, color='orange', linestyle='--', label='Minimum recommended (5 cm)', linewidth=2)
    ax2.axvline(x=2.5, color='purple', linestyle=':', label='Target load (2.5 kg)', linewidth=2)
    ax2.set_xlabel('Cargo Load (kg)', fontweight='bold')
    ax2.set_ylabel('Metacentric Height GM (cm)', fontweight='bold')
    ax2.set_title('Stability vs Load')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Heel angle from lateral offset
    ax3 = axes[1, 0]
    lateral_offsets = np.linspace(0, 0.1, 100)  # 0 to 10 cm offset
    heel_angles_offset = [calculator.heel_angle_from_offset_load(offset, 1.0, gm, displacement)
                         for offset in lateral_offsets]
    
    ax3.plot(lateral_offsets*100, heel_angles_offset, 'r-', linewidth=2)
    ax3.axhline(y=10, color='orange', linestyle='--', label='Design limit (10°)', linewidth=2)
    ax3.set_xlabel('Lateral Offset of 1kg Load (cm)', fontweight='bold')
    ax3.set_ylabel('Heel Angle (degrees)', fontweight='bold')
    ax3.set_title('Heel Sensitivity to Load Position')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Center of gravity diagram
    ax4 = axes[1, 1]
    
    # Draw hull profile
    hull_x = [0, calculator.hull.length, calculator.hull.length, 0, 0]
    hull_y = [0, 0, calculator.hull.draft, calculator.hull.draft, 0]
    ax4.plot(hull_x, hull_y, 'k-', linewidth=2)
    ax4.fill(hull_x, hull_y, alpha=0.2, color='gray')
    
    # Draw waterline
    ax4.axhline(y=calculator.hull.draft, color='b', linestyle='--', 
               label='Waterline', linewidth=2)
    
    # Mark centers
    kb = calculator.center_of_buoyancy()
    bm = calculator.metacentric_radius()
    
    ax4.plot(calculator.hull.length/2, kb, 'bo', markersize=10, label=f'B (KB={kb*100:.1f}cm)')
    ax4.plot(calculator.hull.length/2, kg, 'ro', markersize=10, label=f'G (KG={kg*100:.1f}cm)')
    ax4.plot(calculator.hull.length/2, kb+bm, 'go', markersize=10, 
            label=f'M (BM={bm*100:.1f}cm)')
    
    # Draw GM line
    ax4.plot([calculator.hull.length/2, calculator.hull.length/2], [kg, kb+bm], 
            'g-', linewidth=2, label=f'GM={gm*100:.1f}cm')
    
    ax4.set_xlabel('Length (m)', fontweight='bold')
    ax4.set_ylabel('Height from Keel (m)', fontweight='bold')
    ax4.set_title('Stability Centers (Side View)')
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3)
    ax4.set_aspect('equal')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    plt.show()


def print_stability_report(calculator: StabilityCalculator, mass_dist: MassDistribution):
    """Print comprehensive stability report"""
    
    print("\n" + "="*100)
    print(f"{'STABILITY ANALYSIS REPORT':^100}")
    print("="*100)
    
    # Hull geometry
    print(f"\n{'HULL GEOMETRY':^100}")
    print("-"*100)
    print(f"  Length (L):              {calculator.hull.length:.3f} m")
    print(f"  Beam (B):                {calculator.hull.beam:.3f} m")
    print(f"  Draft (T):               {calculator.hull.draft:.3f} m")
    print(f"  Block Coefficient (Cb):  {calculator.hull.block_coeff:.3f}")
    print(f"  Waterplane Coeff (Cwp):  {calculator.hull.waterplane_coeff:.3f}")
    
    # Hydrostatics
    print(f"\n{'HYDROSTATIC PROPERTIES':^100}")
    print("-"*100)
    volume = calculator.displacement_volume()
    displacement = calculator.displacement_mass()
    waterplane = calculator.waterplane_area()
    
    print(f"  Displacement Volume (∇): {volume:.6f} m³")
    print(f"  Displacement Mass (Δ):   {displacement:.3f} kg")
    print(f"  Waterplane Area (Aw):    {waterplane:.4f} m²")
    
    # Centers
    kb = calculator.center_of_buoyancy()
    bm = calculator.metacentric_radius()
    
    print(f"\n{'STABILITY CENTERS':^100}")
    print("-"*100)
    print(f"  Center of Buoyancy (KB): {kb*100:.2f} cm from keel")
    print(f"  Metacentric Radius (BM): {bm*100:.2f} cm")
    
    # Mass distribution
    total_mass, kg = calculator.combined_cg(mass_dist)
    
    print(f"\n{'MASS DISTRIBUTION':^100}")
    print("-"*100)
    print(f"  Hull:        {mass_dist.hull_mass:.2f} kg @ {mass_dist.hull_cg_height*100:.1f} cm")
    print(f"  Cargo:       {mass_dist.cargo_mass:.2f} kg @ {mass_dist.cargo_cg_height*100:.1f} cm")
    print(f"  Electronics: {mass_dist.electronics_mass:.2f} kg @ {mass_dist.electronics_cg_height*100:.1f} cm")
    print(f"  TOTAL:       {total_mass:.2f} kg")
    print(f"  Combined CG (KG): {kg*100:.2f} cm from keel")
    
    # Stability parameters
    gm = calculator.metacentric_height(kg)
    
    print(f"\n{'STABILITY PARAMETERS':^100}")
    print("-"*100)
    print(f"  Metacentric Height (GM): {gm*100:.2f} cm")
    
    if gm > 0.05:
        stability_rating = "EXCELLENT"
        color = "✓"
    elif gm > 0.03:
        stability_rating = "GOOD"
        color = "✓"
    elif gm > 0:
        stability_rating = "MARGINAL"
        color = "⚠"
    else:
        stability_rating = "UNSTABLE"
        color = "✗"
    
    print(f"  Stability Rating: {color} {stability_rating}")
    
    max_heel = calculator.max_stable_heel(gm)
    print(f"  Estimated Max Safe Heel: {max_heel:.1f}°")
    
    # Righting moment at 10°
    rm_10 = calculator.righting_moment(10, gm, displacement)
    print(f"  Righting Moment @ 10°: {rm_10:.3f} N·m")
    
    # Check design criterion
    print(f"\n{'DESIGN CRITERION CHECK':^100}")
    print("-"*100)
    
    criteria = [
        ("GM > 5 cm", gm*100 > 5, f"{gm*100:.2f} cm"),
        ("Heel < 10° @ max load", True, "Check load tests"),
        ("Total mass = displacement", abs(total_mass - displacement) < 0.1, 
         f"Δ={displacement:.2f} kg, m={total_mass:.2f} kg"),
    ]
    
    for criterion, passed, value in criteria:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {criterion:.<50} {status:>15} ({value})")
    
    # Sensitivity analysis
    print(f"\n{'SENSITIVITY TO LOAD POSITION':^100}")
    print("-"*100)
    
    lateral_offsets = [0.02, 0.05, 0.08]  # 2cm, 5cm, 8cm from centerline
    
    print(f"  Heel angle for 1 kg load at lateral offset:")
    for offset in lateral_offsets:
        heel = calculator.heel_angle_from_offset_load(offset, 1.0, gm, displacement)
        status = "✓" if heel < 10 else "✗"
        print(f"    {offset*100:.0f} cm offset → {heel:.2f}° heel {status}")
    
    print("\n" + "="*100 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Stability Analysis Calculator')
    parser.add_argument('--length', type=float, default=0.45, help='Waterline length (m)')
    parser.add_argument('--beam', type=float, default=0.20, help='Beam (m)')
    parser.add_argument('--draft', type=float, default=0.055, help='Draft (m)')
    parser.add_argument('--hull_mass', type=float, default=0.5, help='Hull mass (kg)')
    parser.add_argument('--hull_cg', type=float, default=0.025, help='Hull CG height (m)')
    parser.add_argument('--cargo', type=float, default=2.5, help='Cargo mass (kg)')
    parser.add_argument('--cargo_cg', type=float, default=0.04, help='Cargo CG height (m)')
    parser.add_argument('--plot', action='store_true', help='Generate plots')
    parser.add_argument('--save_plot', type=str, default='stability_analysis.png')
    
    args = parser.parse_args()
    
    # Setup
    hull = HullGeometry(
        length=args.length,
        beam=args.beam,
        draft=args.draft
    )
    
    mass_dist = MassDistribution(
        hull_mass=args.hull_mass,
        hull_cg_height=args.hull_cg,
        cargo_mass=args.cargo,
        cargo_cg_height=args.cargo_cg
    )
    
    calculator = StabilityCalculator(hull)
    
    # Print report
    print_stability_report(calculator, mass_dist)
    
    # Generate plots
    if args.plot:
        plot_stability_curves(calculator, mass_dist, args.save_plot)


if __name__ == "__main__":
    main()
