#!/usr/bin/env python3
"""
Automated Analysis Suite - RC Cargo Barge
Runs all calculations and generates comprehensive reports

This script automates:
1. Hull geometry visualization (3D)
2. Stability analysis with flotation check
3. Resistance and power calculations (ITTC-1957)
4. Summary report generation

Usage:
    python run_all_analysis.py
    python run_all_analysis.py --cargo 2.5 --velocity 0.5
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse
from datetime import datetime


class AnalysisSuite:
    """Automated analysis suite for RC cargo barge"""
    
    def __init__(self, cargo_mass=2.5, max_velocity=1.0, draft=None):
        self.cargo_mass = cargo_mass
        self.max_velocity = max_velocity
        self.draft = draft
        
        # Boat geometry (real dimensions)
        self.L = 0.45      # 45 cm total length
        self.L_bow = 0.05  # 5 cm pyramidal bow
        self.L_stern = 0.40  # 40 cm rectangular stern
        self.B = 0.172     # 17.2 cm beam
        self.H = 0.156     # 15.6 cm height
        
        # Mass estimates
        self.hull_mass = 1.2      # kg (MDF 4mm + paint)
        self.electronics_mass = 0.8  # kg (ESP32, battery, motors)
        self.total_empty = self.hull_mass + self.electronics_mass
        
        # Calculate draft if not provided
        if self.draft is None:
            self.draft = self.calculate_required_draft()
        
        # Output directory
        self.output_dir = Path("analysis_results")
        self.output_dir.mkdir(exist_ok=True)
        
        # Timestamp for report
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def calculate_required_draft(self):
        """Calculate draft needed to displace total mass"""
        total_mass = self.total_empty + self.cargo_mass
        # Volume coefficient: (1/3)*B*L_bow + L_stern*B
        vol_coef = (1/3) * self.B * self.L_bow + self.L_stern * self.B
        draft = total_mass / (1000 * vol_coef)  # rho = 1000 kg/m³
        return draft
    
    def run_command(self, cmd, description):
        """Run a command and return success status"""
        print(f"\n{'='*80}")
        print(f"  {description}")
        print(f"{'='*80}")
        print(f"Command: {' '.join(cmd)}\n")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=False, text=True)
            print(f"\n✓ {description} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n✗ {description} failed with error code {e.returncode}")
            return False
        except FileNotFoundError:
            print(f"\n✗ Command not found: {cmd[0]}")
            return False
    
    def step1_hull_visualization(self):
        """Generate 3D hull visualization"""
        cmd = [
            sys.executable,
            "visualize_hull_3d.py",
            "--draft", str(self.draft),
            "--save", str(self.output_dir / f"hull_3d_{self.timestamp}.png")
        ]
        return self.run_command(cmd, "STEP 1: 3D Hull Visualization")
    
    def step2_stability_analysis(self):
        """Run stability analysis with flotation check"""
        cmd = [
            sys.executable,
            "stability_analysis.py",
            "--length", str(self.L),
            "--beam", str(self.B),
            "--draft", str(self.draft),
            "--height", str(self.H),
            "--hull_mass", str(self.hull_mass),
            "--cargo", str(self.cargo_mass),
            "--hull_cg", "0.04",
            "--cargo_cg", "0.06",
            "--plot",
            "--save_plot", str(self.output_dir / f"stability_{self.timestamp}.png")
        ]
        return self.run_command(cmd, "STEP 2: Stability Analysis")
    
    def step3_resistance_calculation(self):
        """Run resistance and power calculations"""
        cmd = [
            sys.executable,
            "resistance_calc.py",
            "--length", str(self.L),
            "--beam", str(self.B),
            "--draft", str(self.draft),
            "--v_max", str(self.max_velocity),
            "--plot",
            "--save_plot", str(self.output_dir / f"resistance_{self.timestamp}.png")
        ]
        return self.run_command(cmd, "STEP 3: Resistance & Power Calculation (ITTC-1957)")
    
    def generate_summary_report(self, results):
        """Generate comprehensive summary report"""
        report_path = self.output_dir / f"analysis_report_{self.timestamp}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*90 + "\n")
            f.write(f"{'RC CARGO BARGE - COMPREHENSIVE ANALYSIS REPORT':^90}\n")
            f.write("="*90 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Design specifications
            f.write(f"{'DESIGN SPECIFICATIONS':^90}\n")
            f.write("-"*90 + "\n")
            f.write(f"  Total Length:              {self.L*100:.1f} cm\n")
            f.write(f"  Beam:                      {self.B*100:.1f} cm\n")
            f.write(f"  Height:                    {self.H*100:.1f} cm\n")
            f.write(f"  Bow section:               {self.L_bow*100:.1f} cm (pyramidal)\n")
            f.write(f"  Stern section:             {self.L_stern*100:.1f} cm (rectangular)\n")
            f.write(f"  Material:                  MDF 4mm + waterproofing paint\n\n")
            
            # Mass breakdown
            f.write(f"{'MASS DISTRIBUTION':^90}\n")
            f.write("-"*90 + "\n")
            f.write(f"  Hull (MDF + paint):        {self.hull_mass:.2f} kg\n")
            f.write(f"  Electronics (ESP32+motor): {self.electronics_mass:.2f} kg\n")
            f.write(f"  Cargo:                     {self.cargo_mass:.2f} kg\n")
            f.write(f"  TOTAL:                     {self.total_empty + self.cargo_mass:.2f} kg\n\n")
            
            # Calculated parameters
            f.write(f"{'CALCULATED PARAMETERS':^90}\n")
            f.write("-"*90 + "\n")
            f.write(f"  Required draft:            {self.draft*100:.2f} cm\n")
            f.write(f"  Draft margin (< 6 cm):     {(0.06 - self.draft)*100:+.2f} cm ")
            if self.draft <= 0.06:
                f.write("✓ CUMPLE\n")
            else:
                f.write("✗ EXCEDE\n")
            
            # Calculate volume and displacement
            V_bow = (1/3) * self.B * self.draft * self.L_bow
            V_stern = self.L_stern * self.B * self.draft
            V_total = V_bow + V_stern
            displacement = V_total * 1000
            
            f.write(f"  Displaced volume:          {V_total*1e6:.1f} cm³\n")
            f.write(f"  Displacement:              {displacement:.2f} kg\n")
            f.write(f"  Buoyancy force:            {displacement*9.81:.2f} N\n")
            f.write(f"  Weight force:              {(self.total_empty + self.cargo_mass)*9.81:.2f} N\n\n")
            
            # Analysis results
            f.write(f"{'ANALYSIS RESULTS':^90}\n")
            f.write("-"*90 + "\n")
            for step, success in results.items():
                status = "✓ SUCCESS" if success else "✗ FAILED"
                f.write(f"  {step:<60} {status:>20}\n")
            
            f.write("\n" + "="*90 + "\n")
            f.write(f"{'OUTPUT FILES':^90}\n")
            f.write("="*90 + "\n")
            f.write(f"  3D Hull:      {self.output_dir / f'hull_3d_{self.timestamp}.png'}\n")
            f.write(f"  Stability:    {self.output_dir / f'stability_{self.timestamp}.png'}\n")
            f.write(f"  Resistance:   {self.output_dir / f'resistance_{self.timestamp}.png'}\n")
            f.write(f"  This report:  {report_path}\n")
            f.write("\n" + "="*90 + "\n\n")
            
            # Design recommendations
            f.write(f"{'DESIGN RECOMMENDATIONS':^90}\n")
            f.write("="*90 + "\n")
            if self.draft > 0.06:
                f.write("  ⚠ Draft exceeds 6 cm limit\n")
                max_load_6cm = 0.06 * ((1/3) * self.B * self.L_bow + self.L_stern * self.B) * 1000
                f.write(f"     → Maximum total mass for T<6cm: {max_load_6cm:.2f} kg\n")
                f.write(f"     → Current total mass: {self.total_empty + self.cargo_mass:.2f} kg\n")
                f.write(f"     → Reduce mass by: {(self.total_empty + self.cargo_mass - max_load_6cm):.2f} kg\n\n")
            
            f.write("  Stability improvements:\n")
            f.write("    • Increase beam width for higher GM\n")
            f.write("    • Lower center of gravity (add ballast at keel)\n")
            f.write("    • Reduce top-heavy loads\n")
            f.write("    • Test with actual load distribution\n\n")
            
            f.write("  Performance optimization:\n")
            f.write("    • Smooth hull surface (reduce form factor k)\n")
            f.write("    • Optimize propeller efficiency\n")
            f.write("    • Minimize wetted surface area\n")
            f.write("    • Test at different velocities for optimal IT\n\n")
            
        print(f"\n{'='*80}")
        print(f"  Summary report generated: {report_path}")
        print(f"{'='*80}\n")
        
        return report_path
    
    def run_all(self):
        """Run complete analysis suite"""
        print("\n" + "="*80)
        print(f"{'RC CARGO BARGE - AUTOMATED ANALYSIS SUITE':^80}")
        print("="*80)
        print(f"\nConfiguration:")
        print(f"  Cargo mass:    {self.cargo_mass:.2f} kg")
        print(f"  Total mass:    {self.total_empty + self.cargo_mass:.2f} kg")
        print(f"  Draft:         {self.draft*100:.2f} cm")
        print(f"  Max velocity:  {self.max_velocity:.2f} m/s")
        print(f"  Output dir:    {self.output_dir}")
        
        results = {}
        
        # Run all analysis steps
        results["3D Hull Visualization"] = self.step1_hull_visualization()
        results["Stability Analysis"] = self.step2_stability_analysis()
        results["Resistance Calculation"] = self.step3_resistance_calculation()
        
        # Generate summary
        report_path = self.generate_summary_report(results)
        
        # Final summary
        print("\n" + "="*80)
        print(f"{'ANALYSIS COMPLETE':^80}")
        print("="*80)
        
        success_count = sum(results.values())
        total_count = len(results)
        
        print(f"\nResults: {success_count}/{total_count} steps completed successfully")
        
        for step, success in results.items():
            status = "✓" if success else "✗"
            print(f"  {status} {step}")
        
        print(f"\n📊 All results saved to: {self.output_dir}/")
        print(f"📄 Summary report: {report_path}")
        
        if success_count == total_count:
            print("\n✓ All analyses completed successfully!")
            return 0
        else:
            print(f"\n⚠ {total_count - success_count} step(s) failed")
            return 1


def main():
    parser = argparse.ArgumentParser(
        description='Automated Analysis Suite for RC Cargo Barge',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all_analysis.py
  python run_all_analysis.py --cargo 2.5 --velocity 0.5
  python run_all_analysis.py --cargo 3.0 --draft 0.065
        """
    )
    
    parser.add_argument('--cargo', type=float, default=2.5,
                       help='Cargo mass in kg (default: 2.5)')
    parser.add_argument('--velocity', type=float, default=1.0,
                       help='Maximum velocity for analysis in m/s (default: 1.0)')
    parser.add_argument('--draft', type=float, default=None,
                       help='Draft in meters (default: auto-calculate)')
    
    args = parser.parse_args()
    
    # Change to simulations directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Create and run analysis suite
    suite = AnalysisSuite(
        cargo_mass=args.cargo,
        max_velocity=args.velocity,
        draft=args.draft
    )
    
    exit_code = suite.run_all()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
