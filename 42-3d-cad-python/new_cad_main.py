#!/usr/bin/env python3
"""
3D CAD Model Creation - Working Version
No PyVista/VTK dependencies - Uses Matplotlib and Plotly only
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import math

class CADGenerator:
    """Main CAD Generator Class"""
    
    def __init__(self):
        self.components = []
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_spur_gear(self, teeth=20, module=2, thickness=10, bore_diameter=10, material="Steel AISI 4140"):
        """Create a spur gear with proper dimensions"""
        
        # Gear calculations
        pitch_diameter = teeth * module
        outer_diameter = pitch_diameter + 2 * module
        root_diameter = pitch_diameter - 2.5 * module
        circular_pitch = math.pi * module
        
        print(f"🔧 Creating Spur Gear:")
        print(f"   Teeth: {teeth}")
        print(f"   Module: {module} mm")
        print(f"   Pitch Diameter: {pitch_diameter:.2f} mm")
        print(f"   Outer Diameter: {outer_diameter:.2f} mm")
        print(f"   Root Diameter: {root_diameter:.2f} mm")
        print(f"   Thickness: {thickness} mm")
        print(f"   Bore: {bore_diameter} mm")
        print(f"   Material: {material}")
        
        gear_data = {
            'type': 'spur_gear',
            'name': f'Spur_Gear_{teeth}T_{module}M',
            'teeth': teeth,
            'module': module,
            'thickness': thickness,
            'bore_diameter': bore_diameter,
            'material': material,
            'pitch_diameter': pitch_diameter,
            'outer_diameter': outer_diameter,
            'root_diameter': root_diameter,
            'circular_pitch': circular_pitch
        }
        
        self.components.append(gear_data)
        return gear_data
    
    def create_bearing_housing(self, inner_diameter=30, outer_diameter=60, width=25, 
                              bolt_hole_diameter=6, material="Cast Iron"):
        """Create a bearing housing"""
        
        print(f"🏠 Creating Bearing Housing:")
        print(f"   Inner Diameter: {inner_diameter} mm")
        print(f"   Outer Diameter: {outer_diameter} mm")
        print(f"   Width: {width} mm")
        print(f"   Bolt Holes: {bolt_hole_diameter} mm")
        print(f"   Material: {material}")
        
        housing_data = {
            'type': 'bearing_housing',
            'name': f'Bearing_Housing_ID{inner_diameter}_OD{outer_diameter}',
            'inner_diameter': inner_diameter,
            'outer_diameter': outer_diameter,
            'width': width,
            'bolt_hole_diameter': bolt_hole_diameter,
            'material': material
        }
        
        self.components.append(housing_data)
        return housing_data
    
    def create_2d_technical_drawing(self):
        """Create 2D technical drawings"""
        print("📐 Generating 2D Technical Drawings...")
        
        for component in self.components:
            if component['type'] == 'spur_gear':
                self._draw_gear_2d(component)
            elif component['type'] == 'bearing_housing':
                self._draw_housing_2d(component)
    
    def _draw_gear_2d(self, gear):
        """Create 2D drawing for spur gear"""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Front View
        teeth = gear['teeth']
        outer_radius = gear['outer_diameter'] / 2
        pitch_radius = gear['pitch_diameter'] / 2
        root_radius = gear['root_diameter'] / 2
        bore_radius = gear['bore_diameter'] / 2
        
        # Draw circles
        circle_outer = plt.Circle((0, 0), outer_radius, fill=False, color='blue', linewidth=2, label='Outer Diameter')
        circle_pitch = plt.Circle((0, 0), pitch_radius, fill=False, color='red', linestyle='--', linewidth=1, label='Pitch Diameter')
        circle_root = plt.Circle((0, 0), root_radius, fill=False, color='green', linestyle=':', linewidth=1, label='Root Diameter')
        circle_bore = plt.Circle((0, 0), bore_radius, fill=False, color='black', linewidth=2, label='Bore')
        
        ax1.add_patch(circle_outer)
        ax1.add_patch(circle_pitch)
        ax1.add_patch(circle_root)
        ax1.add_patch(circle_bore)
        
        ax1.set_xlim(-outer_radius*1.2, outer_radius*1.2)
        ax1.set_ylim(-outer_radius*1.2, outer_radius*1.2)
        ax1.set_aspect('equal')
        ax1.set_title(f'Front View - {gear["name"]}')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Side View
        thickness = gear['thickness']
        ax2.add_patch(plt.Rectangle((-outer_radius, -thickness/2), outer_radius*2, thickness, 
                                  fill=False, edgecolor='blue', linewidth=2))
        ax2.add_patch(plt.Rectangle((-bore_radius, -thickness/2), bore_radius*2, thickness, 
                                  fill=False, edgecolor='black', linewidth=2))
        
        ax2.set_xlim(-outer_radius*1.2, outer_radius*1.2)
        ax2.set_ylim(-thickness*0.7, thickness*0.7)
        ax2.set_aspect('equal')
        ax2.set_title('Side View')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('Diameter (mm)')
        ax2.set_ylabel('Thickness (mm)')
        
        # Tooth Profile
        theta = np.linspace(0, 4*np.pi/teeth, 100)
        tooth_profile = []
        for angle in theta:
            tooth_angle = (angle * teeth) % (2 * np.pi)
            if tooth_angle < np.pi / teeth:
                radius = outer_radius
            elif tooth_angle < 2 * np.pi / teeth:
                radius = root_radius
            else:
                radius = pitch_radius
            tooth_profile.append(radius)
        
        ax3.plot(np.degrees(theta), tooth_profile, 'g-', linewidth=2)
        ax3.set_title('Tooth Profile')
        ax3.grid(True, alpha=0.3)
        ax3.set_xlabel('Angle (degrees)')
        ax3.set_ylabel('Radius (mm)')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{gear["name"]}_2d_drawing.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ Saved: {gear['name']}_2d_drawing.png")
    
    def _draw_housing_2d(self, housing):
        """Create 2D drawing for bearing housing"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        inner_radius = housing['inner_diameter'] / 2
        outer_radius = housing['outer_diameter'] / 2
        width = housing['width']
        bolt_radius = housing['bolt_hole_diameter'] / 2
        
        # Front View
        circle_outer = plt.Circle((0, 0), outer_radius, fill=False, color='blue', linewidth=2, label='Outer Diameter')
        circle_inner = plt.Circle((0, 0), inner_radius, fill=False, color='red', linewidth=2, label='Inner Diameter')
        
        # Bolt holes
        bolt_positions = [
            (outer_radius * 0.7, 0),
            (-outer_radius * 0.7, 0),
            (0, outer_radius * 0.7),
            (0, -outer_radius * 0.7)
        ]
        
        ax1.add_patch(circle_outer)
        ax1.add_patch(circle_inner)
        
        for pos in bolt_positions:
            bolt = plt.Circle(pos, bolt_radius, fill=False, color='green', linewidth=1, label='Bolt Hole' if pos == bolt_positions[0] else "")
            ax1.add_patch(bolt)
        
        ax1.set_xlim(-outer_radius*1.2, outer_radius*1.2)
        ax1.set_ylim(-outer_radius*1.2, outer_radius*1.2)
        ax1.set_aspect('equal')
        ax1.set_title(f'Front View - {housing["name"]}')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Side View
        ax2.add_patch(plt.Rectangle((-outer_radius, -width/2), outer_radius*2, width, 
                                  fill=False, edgecolor='blue', linewidth=2))
        ax2.add_patch(plt.Rectangle((-inner_radius, -width/2), inner_radius*2, width, 
                                  fill=False, edgecolor='red', linewidth=2))
        
        ax2.set_xlim(-outer_radius*1.2, outer_radius*1.2)
        ax2.set_ylim(-width*0.7, width*0.7)
        ax2.set_aspect('equal')
        ax2.set_title('Side View')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('Diameter (mm)')
        ax2.set_ylabel('Width (mm)')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{housing["name"]}_2d_drawing.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ Saved: {housing['name']}_2d_drawing.png")
    
    def create_3d_visualization(self):
        """Create interactive 3D visualization using Plotly"""
        print("🎨 Creating 3D Visualizations...")
        
        for component in self.components:
            if component['type'] == 'spur_gear':
                self._create_gear_3d(component)
            elif component['type'] == 'bearing_housing':
                self._create_housing_3d(component)
    
    def _create_gear_3d(self, gear):
        """Create 3D visualization for gear"""
        fig = go.Figure()
        
        teeth = gear['teeth']
        outer_radius = gear['outer_diameter'] / 2
        thickness = gear['thickness']
        
        # Generate gear profile points
        theta = np.linspace(0, 2 * np.pi, teeth * 10)
        radii = []
        
        for angle in theta:
            tooth_angle = (angle * teeth) % (2 * np.pi)
            if tooth_angle < np.pi / teeth:
                radius = outer_radius
            elif tooth_angle < 2 * np.pi / teeth:
                radius = outer_radius * 0.85  # Simplified root
            else:
                radius = outer_radius * 0.95  # Simplified pitch
            radii.append(radius)
        
        radii = np.array(radii)
        
        # Create 3D surface
        z_top = thickness / 2
        z_bottom = -thickness / 2
        
        # Top surface
        x_top = radii * np.cos(theta)
        y_top = radii * np.sin(theta)
        
        # Bottom surface
        x_bottom = radii * np.cos(theta)
        y_bottom = radii * np.sin(theta)
        
        # Add surfaces to plot
        fig.add_trace(go.Mesh3d(
            x=np.concatenate([x_top, x_bottom]),
            y=np.concatenate([y_top, y_bottom]),
            z=np.concatenate([np.full_like(x_top, z_top), np.full_like(x_bottom, z_bottom)]),
            color='lightblue',
            opacity=0.8,
            name='Gear Body'
        ))
        
        fig.update_layout(
            title=f'3D View - {gear["name"]}',
            scene=dict(
                xaxis_title='X (mm)',
                yaxis_title='Y (mm)',
                zaxis_title='Z (mm)',
                aspectmode='data'
            ),
            height=600
        )
        
        fig.write_html(f'{self.output_dir}/{gear["name"]}_3d_view.html')
        print(f"   ✅ Saved: {gear['name']}_3d_view.html")
    
    def _create_housing_3d(self, housing):
        """Create 3D visualization for bearing housing"""
        fig = go.Figure()
        
        inner_radius = housing['inner_diameter'] / 2
        outer_radius = housing['outer_diameter'] / 2
        width = housing['width']
        
        # Generate cylindrical surfaces
        theta = np.linspace(0, 2 * np.pi, 50)
        z = np.linspace(-width/2, width/2, 10)
        
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        # Outer surface
        x_outer = outer_radius * np.cos(theta_grid)
        y_outer = outer_radius * np.sin(theta_grid)
        
        # Inner surface  
        x_inner = inner_radius * np.cos(theta_grid)
        y_inner = inner_radius * np.sin(theta_grid)
        
        # Combine surfaces
        x_combined = np.concatenate([x_outer.flatten(), x_inner.flatten()])
        y_combined = np.concatenate([y_outer.flatten(), y_inner.flatten()]) 
        z_combined = np.concatenate([z_grid.flatten(), z_grid.flatten()])
        
        fig.add_trace(go.Mesh3d(
            x=x_combined,
            y=y_combined,
            z=z_combined,
            color='lightcoral',
            opacity=0.7,
            name='Housing Body'
        ))
        
        fig.update_layout(
            title=f'3D View - {housing["name"]}',
            scene=dict(
                xaxis_title='X (mm)',
                yaxis_title='Y (mm)',
                zaxis_title='Z (mm)',
                aspectmode='data'
            ),
            height=600
        )
        
        fig.write_html(f'{self.output_dir}/{housing["name"]}_3d_view.html')
        print(f"   ✅ Saved: {housing['name']}_3d_view.html")
    
    def generate_technical_documentation(self):
        """Generate comprehensive technical documentation"""
        print("📋 Generating Technical Documentation...")
        
        docs = {
            "project": "Mechanical Components CAD Design",
            "author": "CAD Generator v1.0",
            "date": "2024",
            "units": "millimeters (mm)",
            "components": [],
            "material_specifications": {
                "Steel AISI 4140": {
                    "density": "7.85 g/cm³",
                    "tensile_strength": "655 MPa",
                    "yield_strength": "415 MPa",
                    "hardness": "28-32 HRC",
                    "applications": "Gears, shafts, high-strength components"
                },
                "Cast Iron": {
                    "density": "7.2 g/cm³",
                    "tensile_strength": "250 MPa", 
                    "compressive_strength": "1000 MPa",
                    "hardness": "180-250 HB",
                    "applications": "Housings, frames, structural components"
                }
            },
            "manufacturing_guidelines": {
                "gear_manufacturing": [
                    "Use gear hobbing or shaping process",
                    "Heat treatment: Carburizing and hardening",
                    "Surface finish: 0.8-1.6 μm Ra",
                    "AGMA quality standard: Class 8 or better"
                ],
                "housing_manufacturing": [
                    "CNC machining for precision",
                    "Bore tolerance: H7",
                    "Surface finish: 1.6-3.2 μm Ra", 
                    "Stress relief annealing recommended"
                ]
            }
        }
        
        for component in self.components:
            docs["components"].append(component)
        
        # Save JSON documentation
        with open(f'{self.output_dir}/technical_documentation.json', 'w') as f:
            json.dump(docs, f, indent=2)
        
        # Save human-readable version
        self._save_human_readable_docs(docs)
        
        print("   ✅ Saved: technical_documentation.json")
        print("   ✅ Saved: manufacturing_instructions.txt")
    
    def _save_human_readable_docs(self, docs):
        """Save human-readable documentation"""
        with open(f'{self.output_dir}/manufacturing_instructions.txt', 'w') as f:
            f.write("MANUFACTURING INSTRUCTIONS\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("COMPONENTS SUMMARY:\n")
            f.write("-" * 20 + "\n")
            
            for comp in docs['components']:
                if comp['type'] == 'spur_gear':
                    f.write(f"\nSPUR GEAR: {comp['name']}\n")
                    f.write(f"  Teeth: {comp['teeth']}\n")
                    f.write(f"  Module: {comp['module']} mm\n")
                    f.write(f"  Pitch Diameter: {comp['pitch_diameter']:.2f} mm\n")
                    f.write(f"  Outer Diameter: {comp['outer_diameter']:.2f} mm\n")
                    f.write(f"  Thickness: {comp['thickness']} mm\n")
                    f.write(f"  Bore: {comp['bore_diameter']} mm\n")
                    f.write(f"  Material: {comp['material']}\n")
                    
                    f.write("\n  MANUFACTURING STEPS:\n")
                    f.write("  1. Rough turn gear blank\n")
                    f.write("  2. Gear tooth cutting (hobbing/shaping)\n")
                    f.write("  3. Heat treatment\n")
                    f.write("  4. Finish grinding\n")
                    f.write("  5. Quality inspection\n")
                
                elif comp['type'] == 'bearing_housing':
                    f.write(f"\nBEARING HOUSING: {comp['name']}\n")
                    f.write(f"  Inner Diameter: {comp['inner_diameter']} mm\n")
                    f.write(f"  Outer Diameter: {comp['outer_diameter']} mm\n")
                    f.write(f"  Width: {comp['width']} mm\n")
                    f.write(f"  Bolt Holes: {comp['bolt_hole_diameter']} mm\n")
                    f.write(f"  Material: {comp['material']}\n")
                    
                    f.write("\n  MANUFACTURING STEPS:\n")
                    f.write("  1. Cast or machine housing blank\n")
                    f.write("  2. Bore inner diameter to H7 tolerance\n")
                    f.write("  3. Drill and tap bolt holes\n")
                    f.write("  4. Surface finishing\n")
                    f.write("  5. Assembly preparation\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("QUALITY CONTROL CHECKLIST:\n")
            f.write("- Dimensional accuracy verification\n")
            f.write("- Material certification review\n")
            f.write("- Surface finish measurement\n")
            f.write("- Hardness testing (if applicable)\n")
            f.write("- Final inspection and approval\n")
    
    def export_all_files(self):
        """Export all generated files"""
        print("\n📦 Exporting All Files...")
        self.create_2d_technical_drawing()
        self.create_3d_visualization()
        self.generate_technical_documentation()
        
        # Create a summary file
        self._create_project_summary()
        
        print("\n" + "="*60)
        print("🎉 PROJECT COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        print("\n📁 GENERATED FILES:")
        print("   2D Technical Drawings (.png)")
        print("   3D Interactive Views (.html)") 
        print("   Technical Documentation (.json)")
        print("   Manufacturing Instructions (.txt)")
        print("   Project Summary (.txt)")
        
        print(f"\n📂 All files saved in: {self.output_dir}/")
        print("\n🌐 Open the .html files in your browser for interactive 3D views!")
    
    def _create_project_summary(self):
        """Create a project summary file"""
        summary = f"""
3D CAD MODEL CREATION PROJECT SUMMARY
=====================================

Project: Mechanical Components Design
Generated: {len(self.components)} components

COMPONENTS:
-----------
"""
        
        for comp in self.components:
            if comp['type'] == 'spur_gear':
                summary += f"""
Spur Gear: {comp['name']}
- Teeth: {comp['teeth']}
- Module: {comp['module']} mm  
- Pitch Diameter: {comp['pitch_diameter']:.2f} mm
- Outer Diameter: {comp['outer_diameter']:.2f} mm
- Thickness: {comp['thickness']} mm
- Material: {comp['material']}
"""
            elif comp['type'] == 'bearing_housing':
                summary += f"""
Bearing Housing: {comp['name']}
- Inner Diameter: {comp['inner_diameter']} mm
- Outer Diameter: {comp['outer_diameter']} mm  
- Width: {comp['width']} mm
- Bolt Holes: {comp['bolt_hole_diameter']} mm
- Material: {comp['material']}
"""
        
        summary += f"""
FILES GENERATED:
----------------
- 2D Technical Drawings: {len([c for c in self.components])} files
- 3D Interactive Views: {len([c for c in self.components])} files  
- Technical Documentation: 1 file
- Manufacturing Instructions: 1 file

NEXT STEPS:
-----------
1. Review 2D drawings for dimensional accuracy
2. Open HTML files for 3D visualization
3. Check manufacturing instructions
4. Proceed with prototyping/manufacturing

=====================================
        """
        
        with open(f'{self.output_dir}/project_summary.txt', 'w') as f:
            f.write(summary)

def main():
    """Main function to run the CAD generator"""
    print("🚀 3D CAD Model Creation System")
    print("==========================================")
    
    # Initialize CAD generator
    cad = CADGenerator()
    
    # Design mechanical components
    print("\n1. DESIGNING MECHANICAL COMPONENTS...")
    
    # Create a spur gear
    gear = cad.create_spur_gear(
        teeth=24,
        module=2.5, 
        thickness=15,
        bore_diameter=12,
        material="Steel AISI 4140"
    )
    
    # Create a bearing housing
    housing = cad.create_bearing_housing(
        inner_diameter=35,
        outer_diameter=65, 
        width=30,
        bolt_hole_diameter=6,
        material="Cast Iron"
    )
    
    # Export all files
    cad.export_all_files()

if __name__ == "__main__":
    main()