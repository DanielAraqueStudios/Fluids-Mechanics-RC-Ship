#!/usr/bin/env python3
"""
3D Hull Visualization - Real Geometry
Pyramidal bow (5cm) + Rectangular stern (40cm)

Vista frontal: V invertida (bow) → Rectángulo (stern)
Vista lateral: Bisel inclinado en proa
Vista superior: Pentágono (triángulo + rectángulo)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def create_hull_mesh(L_total=0.45, L_bow=0.05, B=0.172, H=0.156, draft=0.064):
    """
    Create 3D mesh of the hull
    
    Geometry CORREGIDA:
    - Bow (0 to 5cm): Pirámide con base rectangular en E-F y vértice A arriba
      NO hay punto D - A conecta directamente a la mitad de E-F
    - Stern (5cm to 45cm): Prisma rectangular
    """
    
    # Define key points
    vertices = []
    faces = []
    
    # BOW SECTION VERTICES
    # Top: Punto A (punta de proa en el deck)
    A_top_center = [0, 0, H]  # Punta proa arriba (deck)
    
    # Donde el bow se une al stern (en x=L_bow)
    B_top_left = [L_bow, -B/2, H]
    C_top_right = [L_bow, B/2, H]
    E_bot_left = [L_bow, -B/2, 0]
    F_bot_right = [L_bow, B/2, 0]
    
    # STERN SECTION VERTICES
    # Top corners at stern
    G_top_left = [L_total, -B/2, H]
    H_top_right = [L_total, B/2, H]
    
    # Bottom corners at stern
    I_bot_left = [L_total, -B/2, 0]
    J_bot_right = [L_total, B/2, 0]
    
    # Vertices list (sin punto D)
    vertices = [
        A_top_center,   # 0
        B_top_left,     # 1
        C_top_right,    # 2
        E_bot_left,     # 3
        F_bot_right,    # 4
        G_top_left,     # 5
        H_top_right,    # 6
        I_bot_left,     # 7
        J_bot_right     # 8
    ]
    
    # Define faces
    faces = [
        # BOW FACES (pirámide A-B-C-E-F)
        [0, 1, 3],      # Cara izquierda: A-B-E (triángulo)
        [0, 4, 2],      # Cara derecha: A-F-C (triángulo)
        [0, 2, 1],      # Top deck triangle: A-C-B
        [3, 4, 0],      # Cara frontal: E-F-A (triángulo del bisel)
        [3, 1, 2, 4],   # Base rectangular: E-B-C-F
        
        # STERN FACES (prisma rectangular)
        [1, 5, 7, 3],   # Left side: B-G-I-E
        [2, 4, 8, 6],   # Right side: C-F-J-H
        [1, 2, 6, 5],   # Top deck: B-C-H-G
        [3, 4, 8, 7],   # Bottom: E-F-J-I
        [5, 6, 8, 7],   # Stern transom: G-H-J-I
    ]
    
    return np.array(vertices), faces


def plot_hull_3d(draft=0.064, save_path='hull_3d_real.png'):
    """Generate 3D plot with real geometry"""
    
    L_total = 0.45  # 45 cm
    L_bow = 0.05    # 5 cm
    B = 0.172       # 17.2 cm
    H = 0.156       # 15.6 cm
    
    vertices, faces = create_hull_mesh(L_total, L_bow, B, H, draft)
    
    # Create figure
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot hull faces
    face_vertices = [[vertices[idx] for idx in face] for face in faces]
    hull_poly = Poly3DCollection(face_vertices, alpha=0.75, 
                                 facecolor='steelblue', 
                                 edgecolor='navy', linewidths=2)
    ax.add_collection3d(hull_poly)
    
    # Plot vertices with labels (SIN punto D)
    labels = ['A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'J']
    for i, (v, label) in enumerate(zip(vertices, labels)):
        ax.scatter(*v, c='red', s=100, marker='o', edgecolor='darkred', linewidth=1.5)
        offset = 0.015
        ax.text(v[0]+offset, v[1], v[2]+offset, f'  {label}', 
               fontsize=12, fontweight='bold', color='darkred')
    
    # Plot waterline
    n = 50
    # Bow waterline (triangular cross-section)
    x_bow = np.linspace(0, L_bow, n)
    # Width increases linearly from 0 to B
    y_left_bow = -B/2 * (x_bow / L_bow)
    y_right_bow = B/2 * (x_bow / L_bow)
    z_bow = np.full(n, draft)
    
    ax.plot(x_bow, y_left_bow, z_bow, 'cyan', linewidth=3, label='Waterline')
    ax.plot(x_bow, y_right_bow, z_bow, 'cyan', linewidth=3)
    
    # Stern waterline (rectangular)
    x_stern = np.linspace(L_bow, L_total, n)
    y_left_stern = np.full(n, -B/2)
    y_right_stern = np.full(n, B/2)
    z_stern = np.full(n, draft)
    
    ax.plot(x_stern, y_left_stern, z_stern, 'cyan', linewidth=3)
    ax.plot(x_stern, y_right_stern, z_stern, 'cyan', linewidth=3)
    
    # Close waterline at bow and stern
    ax.plot([0, 0], [0, 0], [0, draft], 'cyan', linewidth=3)
    ax.plot([L_total, L_total], [-B/2, B/2], [draft, draft], 'cyan', linewidth=3)
    
    # Add dimension annotations
    # Length
    ax.plot([0, L_total], [B/2+0.03, B/2+0.03], [H, H], 'k--', linewidth=1.5, alpha=0.7)
    ax.text(L_total/2, B/2+0.04, H+0.01, f'L = {L_total*100:.0f} cm', 
           ha='center', fontsize=11, fontweight='bold', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Beam
    ax.plot([L_total, L_total], [-B/2, B/2], [H+0.01, H+0.01], 'k--', linewidth=1.5, alpha=0.7)
    ax.text(L_total, 0, H+0.025, f'B = {B*100:.1f} cm', 
           ha='center', fontsize=11, fontweight='bold', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Height
    ax.plot([L_total+0.02, L_total+0.02], [-B/2, -B/2], [0, H], 'k--', linewidth=1.5, alpha=0.7)
    ax.text(L_total+0.03, -B/2, H/2, f'H = {H*100:.1f} cm', 
           ha='left', fontsize=11, fontweight='bold', rotation=90, va='center',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Draft
    ax.plot([0, 0], [-B/2-0.03, -B/2-0.03], [0, draft], 'r-', linewidth=3)
    ax.text(-0.01, -B/2-0.04, draft/2, f'T = {draft*100:.1f} cm', 
           ha='right', fontsize=11, color='red', fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Bow length
    ax.plot([0, L_bow], [-B/2-0.02, -B/2-0.02], [0, 0], 'g--', linewidth=1.5, alpha=0.7)
    ax.text(L_bow/2, -B/2-0.03, -0.01, f'{L_bow*100:.0f} cm\n(bow)', 
           ha='center', fontsize=9, color='green', fontweight='bold')
    
    # Stern length
    ax.plot([L_bow, L_total], [-B/2-0.02, -B/2-0.02], [0, 0], 'g--', linewidth=1.5, alpha=0.7)
    ax.text((L_bow+L_total)/2, -B/2-0.03, -0.01, f'{(L_total-L_bow)*100:.0f} cm\n(stern)', 
           ha='center', fontsize=9, color='green', fontweight='bold')
    
    # Labels
    ax.set_xlabel('Length (m)', fontsize=13, fontweight='bold', labelpad=10)
    ax.set_ylabel('Beam (m)', fontsize=13, fontweight='bold', labelpad=10)
    ax.set_zlabel('Height (m)', fontsize=13, fontweight='bold', labelpad=10)
    
    ax.set_title('RC Cargo Barge - Real Geometry\n'
                'Bow: Triangular prism (V-shape) | Stern: Rectangular prism\n'
                f'Draft = {draft*100:.1f} cm | Displacement = {calculate_displacement(draft):.2f} kg',
                fontsize=14, fontweight='bold', pad=20)
    
    # Set equal aspect ratio
    max_dim = max(L_total, B, H)
    ax.set_xlim([0, L_total])
    ax.set_ylim([-B/2-0.05, B/2+0.05])
    ax.set_zlim([0, H+0.05])
    
    # Set viewing angle
    ax.view_init(elev=25, azim=130)
    
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ 3D hull visualization saved: {save_path}")
    plt.show()


def calculate_displacement(draft):
    """Calculate displacement at given draft"""
    L_bow = 0.05
    L_stern = 0.40
    B = 0.172
    
    # Bow volume: triangular prism
    V_bow = 0.5 * B * draft * L_bow
    
    # Stern volume: rectangular prism
    V_stern = L_stern * B * draft
    
    # Total displacement (kg)
    displacement = (V_bow + V_stern) * 1000  # rho = 1000 kg/m³
    
    return displacement


def print_geometry_info(draft=0.064):
    """Print detailed geometry information"""
    
    print("\n" + "="*90)
    print(f"{'RC CARGO BARGE - REAL GEOMETRY SPECIFICATION':^90}")
    print("="*90)
    
    print(f"\n{'HULL SECTIONS':^90}")
    print("-"*90)
    print("  BOW (0-5 cm):")
    print("    - Type: PIRÁMIDE con base rectangular y vértice superior")
    print("    - Vértice A (arriba): Punta del deck (0, 0, H)")
    print("    - Base rectangular: E-F-C-B en x=5cm (17.2 cm × 15.6 cm)")
    print("    - Vista superior: Triángulo apuntando hacia adelante (A-B-C)")
    print("    - Vista lateral: Bisel inclinado A conecta a línea E-F")
    print("    - Vista frontal en x=5cm: Rectángulo 17.2 × 15.6 cm")
    print()
    print("  STERN (5-45 cm):")
    print("    - Type: Prisma rectangular")
    print("    - Vista superior: Rectángulo (B-C-H-G)")
    print("    - Vista frontal: Rectángulo 17.2 × 15.6 cm")
    print("    - Vista lateral: Caja rectangular")
    
    print(f"\n{'DIMENSIONS':^90}")
    print("-"*90)
    print(f"  Total Length:              45.0 cm  (5 cm bow + 40 cm stern)")
    print(f"  Beam:                      17.2 cm  (constant)")
    print(f"  Height:                    15.6 cm  (constant)")
    print(f"  Draft @ {draft*100:.1f} cm:            {draft*100:.1f} cm")
    
    print(f"\n{'HYDROSTATICS @ T={draft*100:.1f} cm':^90}")
    print("-"*90)
    
    L_bow = 0.05
    L_stern = 0.40
    B = 0.172
    H = 0.156
    
    # Volumes
    V_bow = 0.5 * B * draft * L_bow
    V_stern = L_stern * B * draft
    V_total = V_bow + V_stern
    displacement = V_total * 1000
    
    # Areas
    A_waterplane_bow = 0.5 * B * L_bow  # Triangle
    A_waterplane_stern = L_stern * B     # Rectangle
    A_waterplane_total = A_waterplane_bow + A_waterplane_stern
    
    # Wetted surface (simplified)
    # Bow: 2 triangular sides + bottom triangle
    bow_side_area = 2 * np.sqrt((L_bow)**2 + (draft)**2) * np.sqrt((B/2)**2 + (draft)**2)
    # Stern: 2 sides + bottom
    stern_wetted = 2 * L_stern * draft + L_stern * B
    
    print(f"  Bow volume:                {V_bow*1e6:.1f} cm³")
    print(f"  Stern volume:              {V_stern*1e6:.1f} cm³")
    print(f"  Total displaced volume:    {V_total*1e6:.1f} cm³")
    print(f"  Displacement:              {displacement:.2f} kg")
    print()
    print(f"  Waterplane area (bow):     {A_waterplane_bow*1e4:.1f} cm²")
    print(f"  Waterplane area (stern):   {A_waterplane_stern*1e4:.1f} cm²")
    print(f"  Total waterplane area:     {A_waterplane_total*1e4:.1f} cm²")
    print()
    print(f"  Block coefficient (Cb):    {V_total / (0.45 * B * draft):.3f}")
    print(f"  Waterplane coeff (Cwp):    {A_waterplane_total / (0.45 * B):.3f}")
    
    print("\n" + "="*90 + "\n")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='3D Hull Visualization')
    parser.add_argument('--draft', type=float, default=0.064, help='Draft in meters')
    parser.add_argument('--save', type=str, default='hull_3d_real.png', help='Output filename')
    
    args = parser.parse_args()
    
    print_geometry_info(args.draft)
    plot_hull_3d(args.draft, args.save)
