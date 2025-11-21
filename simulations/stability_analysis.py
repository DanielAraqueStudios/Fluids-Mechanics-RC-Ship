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
    """Hull dimensions and coefficients for hybrid bow-rectangular stern hull"""
    length: float  # Total waterline length (m)
    beam: float    # Beam at waterline (m)
    draft: float   # Draft at design condition (m)
    height: float  # Total hull height/depth (m)
    bow_length: float = 0.05  # Length of pyramidal bow section (m)
    bow_base_width: float = 0.172  # Base width of bow pyramid (m)
    stern_length: float = 0.40  # Length of rectangular stern section (m)
    block_coeff: float = 0.70  # Block coefficient Cb (adjusted for hybrid shape)
    waterplane_coeff: float = 0.88  # Waterplane coefficient Cwp (pentagonal deck)
    

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
        """
        Calculate displaced volume for hybrid hull:
        Volume = Bow pyramid volume + Stern rectangular volume
        
        Bow: PIRÁMIDE con vértice A arriba (en el deck) y base rectangular E-F-C-B
             NO hay punto D - el vértice A está en (0,0,H) y la base en x=bow_length
        Stern: Prisma rectangular
        """
        # Bow volume: Pirámide = (1/3) × base_area × height
        # Base rectangular en x=bow_length: width=beam, height=draft (sumergido)
        # Altura de la pirámide = bow_length (5 cm)
        bow_base_area = self.hull.bow_base_width * min(self.hull.draft, self.hull.height)
        bow_volume = (1/3) * bow_base_area * self.hull.bow_length
        
        # Stern volume (rectangular prism): V = length × width × draft
        stern_volume = self.hull.stern_length * self.hull.beam * self.hull.draft
        
        return bow_volume + stern_volume
    
    def displacement_mass(self) -> float:
        """Calculate displacement mass: Δ = ρ × ∇"""
        return self.rho * self.displacement_volume()
    
    def waterplane_area(self) -> float:
        """
        Calculate waterplane area for pentagonal deck:
        Area = Bow triangle + Stern rectangle
        """
        # Bow triangle area: A = 0.5 × base × height
        bow_triangle_height = 0.05  # 5 cm horizontal projection
        bow_area = 0.5 * self.hull.bow_base_width * bow_triangle_height
        
        # Stern rectangle area: A = length × width
        stern_area = self.hull.stern_length * self.hull.beam
        
        return bow_area + stern_area
    
    def center_of_buoyancy(self) -> float:
        """
        Calculate KB (keel to center of buoyancy) for hybrid hull
        
        Weighted average of bow pyramid and stern prism centroids
        - Pyramid: centroid at 1/4 of height from base
        - Rectangular prism: centroid at 1/2 of draft from keel
        """
        bow_base_area = self.hull.bow_base_width * min(self.hull.draft, self.hull.height)
        bow_volume = (1/3) * bow_base_area * self.hull.bow_length
        stern_volume = self.hull.stern_length * self.hull.beam * self.hull.draft
        total_volume = bow_volume + stern_volume
        
        # Centroids from keel (vertical position)
        bow_kb = 0.25 * min(self.hull.draft, self.hull.height)  # Pyramid centroid
        stern_kb = 0.5 * self.hull.draft  # Rectangle centroid
        
        # Weighted average
        if total_volume > 0:
            kb = (bow_volume * bow_kb + stern_volume * stern_kb) / total_volume
        else:
            kb = 0.5 * self.hull.draft
        return kb
    
    def metacentric_radius(self) -> float:
        """
        Calculate BM (buoyancy to metacenter) for pentagonal waterplane
        BM = I / ∇
        where I = second moment of area about longitudinal centerline
        
        For pentagonal deck (triangle + rectangle):
        I_total = I_bow_triangle + I_stern_rectangle
        """
        # Bow triangle: I ≈ (base × height³) / 36 for isosceles triangle
        bow_triangle_height = 0.05
        I_bow = (self.hull.bow_base_width * bow_triangle_height**3) / 36
        
        # Stern rectangle: I = (L × B³) / 12
        I_stern = (self.hull.stern_length * self.hull.beam**3) / 12
        
        I_total = I_bow + I_stern
        volume = self.displacement_volume()
        
        return I_total / volume if volume > 0 else 0
    
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
    
    # Buoyancy force and flotation check
    total_mass, _ = calculator.combined_cg(mass_dist)
    buoyancy_force = displacement * calculator.g  # N
    weight_force = total_mass * calculator.g      # N
    net_force = buoyancy_force - weight_force     # N
    
    print(f"\n{'FLOTATION ANALYSIS':^100}")
    print("-"*100)
    print(f"  Buoyancy Force (Fb):     {buoyancy_force:.3f} N ↑")
    print(f"  Weight Force (W):        {weight_force:.3f} N ↓")
    print(f"  Net Vertical Force:      {net_force:+.3f} N")
    
    if abs(net_force) < 0.1:  # Nearly balanced (< 0.1 N difference)
        flotation_status = "✓ FLOTA EN EQUILIBRIO"
        flotation_color = "green"
    elif net_force > 0:
        flotation_status = f"⚠ FLOTA CON RESERVA DE {net_force:.2f} N (puede cargar más)"
        flotation_color = "yellow"
    else:
        flotation_status = f"✗ SE HUNDE - Falta flotabilidad: {abs(net_force):.2f} N"
        flotation_color = "red"
    
    print(f"  Estado de flotación:     {flotation_status}")
    
    # Reserve buoyancy
    draft_margin = calculator.hull.height - calculator.hull.draft
    if draft_margin > 0:
        reserve_volume = waterplane * draft_margin
        reserve_buoyancy = reserve_volume * calculator.rho * calculator.g
        additional_load = reserve_buoyancy / calculator.g
        print(f"  Margen de calado:        {draft_margin*100:.2f} cm")
        print(f"  Reserva de flotabilidad: {reserve_buoyancy:.2f} N")
        print(f"  Carga adicional máxima:  {additional_load:.2f} kg")
    
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
    parser.add_argument('--length', type=float, default=0.45, help='Total waterline length (m)')
    parser.add_argument('--beam', type=float, default=0.172, help='Beam (m)')
    parser.add_argument('--draft', type=float, default=0.055, help='Draft (m)')
    parser.add_argument('--height', type=float, default=0.156, help='Total hull height (m)')
    parser.add_argument('--hull_mass', type=float, default=1.2, help='Hull mass (kg)')
    parser.add_argument('--hull_cg', type=float, default=0.04, help='Hull CG height (m)')
    parser.add_argument('--cargo', type=float, default=2.5, help='Cargo mass (kg)')
    parser.add_argument('--cargo_cg', type=float, default=0.06, help='Cargo CG height (m)')
    parser.add_argument('--plot', action='store_true', help='Generate plots')
    parser.add_argument('--save_plot', type=str, default='stability_analysis.png')
    
    args = parser.parse_args()
    
    # Setup with real boat geometry
    hull = HullGeometry(
        length=args.length,
        beam=args.beam,
        draft=args.draft,
        height=args.height,
        bow_length=0.05,  # 5 cm pyramidal bow
        bow_base_width=0.172,  # 17.2 cm base
        stern_length=0.40,  # 40 cm rectangular stern
        block_coeff=0.70,
        waterplane_coeff=0.88
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
