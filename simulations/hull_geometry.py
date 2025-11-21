#!/usr/bin/env python3
"""
Hull Geometry Calculator for Custom Pentagonal Barge
Calculates wetted surface area, volume, and coefficients for the specific design

Design specifications:
- Length: 40 cm
- Beam (popa): 17.2 cm  
- Height: 15.6 cm
- Bow: Pointed on deck (2x10cm), straight on bottom
- Material: MDF 4mm with waterproof paint
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class CustomHullGeometry:
    """Calculate geometric properties of the custom pentagonal barge"""
    
    def __init__(self):
        # Main dimensions (meters)
        self.length = 0.40  # 40 cm
        self.beam = 0.172   # 17.2 cm at stern
        self.height = 0.156 # 15.6 cm total height
        self.bow_length = 0.10  # 10 cm each side of bow point
        
        # Material properties
        self.mdf_thickness = 0.004  # 4 mm
        self.mdf_density = 700  # kg/m³
        self.paint_weight = 0.05  # kg (estimated)
        
    def deck_area(self):
        """Calculate deck area (pentagonal top view)"""
        # Rectangular section + triangular bow
        rect_length = self.length - self.bow_length
        rect_area = rect_length * self.beam
        
        # Triangular bow (isosceles triangle)
        # Base = beam, height = bow_length
        triangle_area = 0.5 * self.beam * self.bow_length
        
        return rect_area + triangle_area
    
    def bottom_area(self):
        """Calculate bottom area (rectangular - straight bow at bottom)"""
        return self.length * self.beam
    
    def wetted_surface_area(self, draft):
        """
        Calculate wetted surface area at given draft
        
        Args:
            draft: Draft in meters
            
        Returns:
            Wetted surface area in m²
        """
        if draft <= 0:
            return 0.0
        
        # Bottom area (fully submerged if draft > 0)
        bottom = self.bottom_area()
        
        # Side walls - rectangular section
        rect_length = self.length - self.bow_length
        side_rect = 2 * rect_length * draft
        
        # Stern (popa) - rectangular
        stern = self.beam * draft
        
        # Bow sides - two trapezoids
        # At bottom: beam wide
        # At draft height: depends on taper
        # Simplified: assume linear taper from beam to point over bow_length
        bow_width_at_draft = self.beam * (1 - draft / self.height)
        if bow_width_at_draft < 0:
            bow_width_at_draft = 0
        
        # Two trapezoidal bow faces
        # Height = draft, parallel sides = beam and bow_width_at_draft, slant height ≈ bow_length
        avg_bow_width = (self.beam + bow_width_at_draft) / 2
        bow_perimeter = 2 * np.sqrt(self.bow_length**2 + (self.beam/2)**2)
        bow_sides = bow_perimeter * draft
        
        total_wetted = bottom + side_rect + stern + bow_sides
        
        return total_wetted
    
    def displaced_volume(self, draft):
        """
        Calculate displaced volume at given draft
        
        Args:
            draft: Draft in meters
            
        Returns:
            Displaced volume in m³
        """
        if draft <= 0:
            return 0.0
        
        # Rectangular section volume
        rect_length = self.length - self.bow_length
        rect_volume = rect_length * self.beam * draft
        
        # Bow volume - wedge/pyramid
        # Base area at draft level varies linearly
        # Simplified: trapezoidal prism
        bow_base_bottom = self.beam
        bow_base_top = self.beam * (1 - draft / self.height)
        if bow_base_top < 0:
            bow_base_top = 0
        
        avg_bow_base = (bow_base_bottom + bow_base_top) / 2
        bow_volume = avg_bow_base * self.bow_length * draft / 2
        
        total_volume = rect_volume + bow_volume
        
        return total_volume
    
    def block_coefficient(self, draft):
        """Calculate block coefficient Cb"""
        volume = self.displaced_volume(draft)
        return volume / (self.length * self.beam * draft)
    
    def waterplane_area(self, draft):
        """Calculate waterplane area at given draft (pentagonal)"""
        # At waterline, bow tapers
        bow_width = self.beam * (1 - draft / self.height)
        if bow_width < 0:
            bow_width = 0
        
        rect_length = self.length - self.bow_length
        rect_area = rect_length * self.beam
        triangle_area = 0.5 * (self.beam + bow_width) * self.bow_length
        
        return rect_area + triangle_area
    
    def waterplane_coefficient(self, draft):
        """Calculate waterplane coefficient Cwp"""
        aw = self.waterplane_area(draft)
        return aw / (self.length * self.beam)
    
    def hull_weight(self):
        """Calculate weight of MDF hull + paint"""
        # Bottom
        bottom_area = self.bottom_area()
        
        # Sides (approximate as sum of rectangles)
        rect_length = self.length - self.bow_length
        side_area = 2 * rect_length * self.height + 2 * self.bow_length * self.height
        
        # Stern
        stern_area = self.beam * self.height
        
        # Deck (pentagonal)
        deck_area = self.deck_area()
        
        total_area = bottom_area + side_area + stern_area + deck_area
        
        # Volume of MDF
        mdf_volume = total_area * self.mdf_thickness
        mdf_weight = mdf_volume * self.mdf_density
        
        return mdf_weight + self.paint_weight
    
    def center_of_buoyancy(self, draft):
        """Estimate KB (keel to center of buoyancy)"""
        # For box-like hull, approximately half the draft
        return draft / 2
    
    def second_moment_waterplane(self, draft):
        """Calculate second moment of waterplane area about centerline"""
        # Simplified for rectangular + triangle
        # I = (L × B³)/12 for rectangle
        rect_length = self.length - self.bow_length
        I_rect = rect_length * self.beam**3 / 12
        
        # Triangle contribution (approximated)
        bow_width = self.beam * (1 - draft / self.height)
        I_triangle = self.bow_length * self.beam**3 / 36
        
        return I_rect + I_triangle
    
    def print_summary(self, draft_design=0.055):
        """Print geometric summary"""
        print("\n" + "="*80)
        print(f"{'CUSTOM PENTAGONAL BARGE - GEOMETRIC PROPERTIES':^80}")
        print("="*80)
        
        print(f"\nMAIN DIMENSIONS:")
        print(f"  Length:           {self.length*100:.1f} cm")
        print(f"  Beam (stern):     {self.beam*100:.1f} cm")
        print(f"  Height:           {self.height*100:.1f} cm")
        print(f"  Bow length:       {self.bow_length*100:.1f} cm")
        print(f"  Material:         MDF {self.mdf_thickness*1000:.0f}mm + waterproof paint")
        
        print(f"\nAREAS:")
        print(f"  Deck area:        {self.deck_area():.6f} m²")
        print(f"  Bottom area:      {self.bottom_area():.6f} m²")
        print(f"  Hull weight:      {self.hull_weight():.3f} kg")
        
        print(f"\nAT DESIGN DRAFT ({draft_design*100:.1f} cm):")
        draft = draft_design
        print(f"  Wetted area (S):  {self.wetted_surface_area(draft):.6f} m²")
        print(f"  Displaced vol:    {self.displaced_volume(draft):.6f} m³")
        print(f"  Displacement:     {self.displaced_volume(draft)*1000:.3f} kg")
        print(f"  Block coeff (Cb): {self.block_coefficient(draft):.3f}")
        print(f"  Waterplane area:  {self.waterplane_area(draft):.6f} m²")
        print(f"  Cwp:              {self.waterplane_coefficient(draft):.3f}")
        print(f"  KB:               {self.center_of_buoyancy(draft)*100:.2f} cm")
        
        print("\n" + "="*80 + "\n")
    
    def plot_hull_lines(self):
        """Generate 3D visualization of hull"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Bottom rectangle
        x_bottom = [0, self.length, self.length, 0, 0]
        y_bottom = [0, 0, self.beam, self.beam, 0]
        z_bottom = [0, 0, 0, 0, 0]
        
        # Deck (pentagonal)
        x_deck = [0, self.length-self.bow_length, self.length, 
                  self.length-self.bow_length, 0, 0]
        y_deck = [self.beam/2, 0, self.beam/2, self.beam, self.beam/2, self.beam/2]
        z_deck = [self.height]*6
        
        # Sides
        ax.plot(x_bottom, y_bottom, z_bottom, 'b-', linewidth=2, label='Bottom')
        ax.plot(x_deck, y_deck, z_deck, 'r-', linewidth=2, label='Deck')
        
        # Vertical edges
        for i in range(4):
            ax.plot([x_bottom[i], x_deck[i]], [y_bottom[i], y_deck[i]], 
                   [z_bottom[i], z_deck[i]], 'g-', linewidth=1)
        
        # Waterline at 5.5 cm
        draft = 0.055
        x_wl = x_bottom
        y_wl = y_bottom
        z_wl = [draft]*5
        ax.plot(x_wl, y_wl, z_wl, 'c--', linewidth=2, label=f'Waterline @ {draft*100:.1f}cm')
        
        ax.set_xlabel('Length (m)')
        ax.set_ylabel('Beam (m)')
        ax.set_zlabel('Height (m)')
        ax.set_title('Custom Pentagonal Barge - 3D Hull Lines')
        ax.legend()
        ax.set_box_aspect([4, 1.72, 1.56])
        
        plt.tight_layout()
        plt.savefig('hull_geometry_3d.png', dpi=300, bbox_inches='tight')
        print("3D visualization saved as 'hull_geometry_3d.png'")
        plt.show()
    
    def plot_draft_curves(self):
        """Plot displacement and wetted area vs draft"""
        drafts = np.linspace(0.01, 0.10, 100)
        
        wetted_areas = [self.wetted_surface_area(d) for d in drafts]
        volumes = [self.displaced_volume(d) for d in drafts]
        displacements = [v * 1000 for v in volumes]  # kg
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Wetted area
        ax1.plot(drafts*100, wetted_areas, 'b-', linewidth=2)
        ax1.axvline(x=5.5, color='r', linestyle='--', label='Design draft (5.5 cm)')
        ax1.set_xlabel('Draft (cm)', fontweight='bold')
        ax1.set_ylabel('Wetted Surface Area (m²)', fontweight='bold')
        ax1.set_title('Wetted Area vs Draft')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Displacement
        ax2.plot(drafts*100, displacements, 'g-', linewidth=2)
        ax2.axvline(x=5.5, color='r', linestyle='--', label='Design draft (5.5 cm)')
        ax2.axhline(y=3.44, color='orange', linestyle=':', label='Target displacement (3.44 kg)')
        ax2.set_xlabel('Draft (cm)', fontweight='bold')
        ax2.set_ylabel('Displacement (kg)', fontweight='bold')
        ax2.set_title('Displacement vs Draft')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('hull_draft_curves.png', dpi=300, bbox_inches='tight')
        print("Draft curves saved as 'hull_draft_curves.png'")
        plt.show()


def main():
    hull = CustomHullGeometry()
    
    # Print summary
    hull.print_summary(draft_design=0.055)
    
    # Generate plots
    print("Generating visualizations...")
    hull.plot_draft_curves()
    hull.plot_hull_lines()
    
    # Export key values for other scripts
    print("\nKEY VALUES FOR resistance_calc.py:")
    print(f"  --length {hull.length:.3f}")
    print(f"  --beam {hull.beam:.3f}")
    print(f"  --draft 0.055")
    print(f"  --wetted_area {hull.wetted_surface_area(0.055):.6f}")
    print(f"  --form_factor 0.25")  # Slightly higher due to bow shape


if __name__ == "__main__":
    main()
