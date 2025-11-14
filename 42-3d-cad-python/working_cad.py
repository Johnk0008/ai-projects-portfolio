#!/usr/bin/env python3
"""
Working 3D CAD Model Creation - Fixed JSON Serialization
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os

class WorkingCADGenerator:
    """CAD Generator using Plotly for 3D visualization"""
    
    def __init__(self):
        self.components = []
        
    def create_spur_gear(self, teeth=20, module=2, thickness=10, bore_diameter=8):
        """Create a spur gear and return mesh data"""
        
        # Gear calculations
        pitch_diameter = teeth * module
        outer_diameter = pitch_diameter + 2 * module
        root_diameter = pitch_diameter - 2.5 * module
        
        print(f"Gear Specifications:")
        print(f"  Teeth: {teeth}")
        print(f"  Module: {module} mm")
        print(f"  Pitch Diameter: {pitch_diameter:.2f} mm")
        print(f"  Outer Diameter: {outer_diameter:.2f} mm")
        print(f"  Root Diameter: {root_diameter:.2f} mm")
        print(f"  Thickness: {thickness} mm")
        
        # Generate gear points for 3D visualization
        theta = np.linspace(0, 2 * np.pi, teeth * 6)
        
        # Simplified gear profile
        radii = []
        for angle in theta:
            # Create tooth-like profile
            tooth_angle = (angle * teeth) % (2 * np.pi)
            if tooth_angle < np.pi / teeth:
                radius = outer_diameter / 2
            elif tooth_angle < 2 * np.pi / teeth:
                radius = root_diameter / 2
            else:
                radius = pitch_diameter / 2
            radii.append(radius)
        
        # Convert to regular Python lists for JSON serialization
        radii_list = [float(r) for r in radii]
        theta_list = [float(t) for t in theta]
        
        gear_data = {
            'type': 'spur_gear',
            'teeth': teeth,
            'module': module,
            'thickness': thickness,
            'pitch_diameter': float(pitch_diameter),
            'outer_diameter': float(outer_diameter),
            'root_diameter': float(root_diameter),
            'theta': theta_list,
            'radii': radii_list,
            'bore_diameter': bore_diameter,
            'material': 'Steel AISI 4140'
        }
        
        self.components.append(gear_data)
        return gear_data
    
    def create_bearing_housing(self, inner_diameter=30, outer_diameter=60, width=25):
        """Create bearing housing"""
        
        housing_data = {
            'type': 'bearing_housing',
            'inner_diameter': inner_diameter,
            'outer_diameter': outer_diameter,
            'width': width,
            'material': 'Cast Iron'
        }
        
        self.components.append(housing_data)
        return housing_data
    
    def plot_gear_2d(self, gear_data):
        """Create 2D technical drawing of gear"""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Convert back to numpy for plotting
        theta = np.array(gear_data['theta'])
        radii = np.array(gear_data['radii'])
        x = radii * np.cos(theta)
        y = radii * np.sin(theta)
        
        # Front view
        ax1.plot(x, y, 'b-', linewidth=2)
        ax1.set_aspect('equal')
        ax1.set_title('Front View')
        ax1.grid(True)
        ax1.set_xlabel('X (mm)')
        ax1.set_ylabel('Y (mm)')
        
        # Add dimensions
        outer_dia = gear_data['outer_diameter']
        pitch_dia = gear_data['pitch_diameter']
        bore_dia = gear_data['bore_diameter']
        
        # Outer diameter dimension
        ax1.plot([0, outer_dia/2], [0, 0], 'k--', alpha=0.5)
        ax1.annotate(f'Ø{outer_dia}', (outer_dia/4, 5), ha='center')
        
        # Pitch diameter
        ax1.add_patch(plt.Circle((0, 0), pitch_dia/2, fill=False, color='green', linestyle=':'))
        ax1.annotate(f'Pitch Ø{pitch_dia}', (0, -pitch_dia/2 - 5), ha='center')
        
        # Bore diameter
        ax1.add_patch(plt.Circle((0, 0), bore_dia/2, fill=False, color='red', linestyle='--'))
        ax1.annotate(f'Bore Ø{bore_dia}', (0, bore_dia/2 + 3), ha='center')
        
        # Side view
        thickness = gear_data['thickness']
        ax2.add_patch(plt.Rectangle((-outer_dia/2, -thickness/2), outer_dia, thickness, 
                                  fill=False, edgecolor='blue', linewidth=2))
        ax2.set_aspect('equal')
        ax2.set_title('Side View')
        ax2.grid(True)
        ax2.set_xlabel('Width (mm)')
        ax2.set_ylabel('Thickness (mm)')
        
        # Add thickness dimension
        ax2.plot([outer_dia/2 + 5, outer_dia/2 + 5], [-thickness/2, thickness/2], 'k-')
        ax2.annotate(f'{thickness}mm', (outer_dia/2 + 7, 0), va='center')
        
        # Tooth detail
        teeth = gear_data['teeth']
        module = gear_data['module']
        tooth_theta = np.linspace(0, 4*np.pi/teeth, 50)
        tooth_radii = []
        for angle in tooth_theta:
            tooth_angle = (angle * teeth) % (2 * np.pi)
            if tooth_angle < np.pi / teeth:
                radius = outer_dia / 2
            elif tooth_angle < 2 * np.pi / teeth:
                radius = pitch_dia / 2 - 1.25 * module
            else:
                radius = pitch_dia / 2
            tooth_radii.append(radius)
        
        ax3.plot(tooth_theta, tooth_radii, 'g-', linewidth=2)
        ax3.fill_between(tooth_theta, tooth_radii, alpha=0.3, color='green')
        ax3.set_title('Tooth Profile')
        ax3.grid(True)
        ax3.set_xlabel('Angle (rad)')
        ax3.set_ylabel('Radius (mm)')
        
        plt.tight_layout()
        return fig
    
    def create_3d_visualization(self):
        """Create interactive 3D visualization using Plotly"""
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{'is_3d': True}, {'is_3d': True}],
                   [{'is_3d': False}, {'is_3d': False}]],
            subplot_titles=['Spur Gear 3D', 'Bearing Housing 3D', 'Gear Specifications', 'Assembly Instructions'],
            print_grid=False
        )
        
        # Add spur gear visualization
        gear_data = next((comp for comp in self.components if comp['type'] == 'spur_gear'), None)
        if gear_data:
            # Convert to numpy for calculations
            theta = np.array(gear_data['theta'])
            radii = np.array(gear_data['radii'])
            thickness = gear_data['thickness']
            
            # Generate 3D points
            x_outer = radii * np.cos(theta)
            y_outer = radii * np.sin(theta)
            z_top = thickness / 2
            z_bottom = -thickness / 2
            
            # Add top surface
            fig.add_trace(go.Scatter3d(
                x=x_outer.tolist(), 
                y=y_outer.tolist(), 
                z=[z_top] * len(x_outer),
                mode='lines', 
                line=dict(color='blue', width=4),
                name='Gear Profile'
            ), row=1, col=1)
            
            # Add bore
            bore_theta = np.linspace(0, 2*np.pi, 50)
            bore_radius = gear_data['bore_diameter'] / 2
            x_bore = bore_radius * np.cos(bore_theta)
            y_bore = bore_radius * np.sin(bore_theta)
            
            fig.add_trace(go.Scatter3d(
                x=x_bore.tolist(),
                y=y_bore.tolist(),
                z=[z_top] * len(x_bore),
                mode='lines',
                line=dict(color='red', width=3),
                name='Bore'
            ), row=1, col=1)
        
        # Add bearing housing visualization
        housing_data = next((comp for comp in self.components if comp['type'] == 'bearing_housing'), None)
        if housing_data:
            # Create cylindrical surfaces
            theta = np.linspace(0, 2*np.pi, 50)
            width = housing_data['width']
            
            # Outer cylinder
            x_outer = (housing_data['outer_diameter']/2) * np.cos(theta)
            y_outer = (housing_data['outer_diameter']/2) * np.sin(theta)
            
            fig.add_trace(go.Scatter3d(
                x=x_outer.tolist(),
                y=y_outer.tolist(), 
                z=[width/2] * len(x_outer),
                mode='lines', 
                line=dict(color='green', width=4),
                name='Housing Outer'
            ), row=1, col=2)
            
            # Inner cylinder
            x_inner = (housing_data['inner_diameter']/2) * np.cos(theta)
            y_inner = (housing_data['inner_diameter']/2) * np.sin(theta)
            
            fig.add_trace(go.Scatter3d(
                x=x_inner.tolist(),
                y=y_inner.tolist(),
                z=[width/2] * len(x_inner),
                mode='lines',
                line=dict(color='orange', width=3),
                name='Housing Bore'
            ), row=1, col=2)
        
        # Add specifications table
        if gear_data:
            specs_text = f"""
            <b>Spur Gear Specifications:</b><br>
            • Teeth: {gear_data['teeth']}<br>
            • Module: {gear_data['module']} mm<br>
            • Pitch Ø: {gear_data['pitch_diameter']:.1f} mm<br>
            • Outer Ø: {gear_data['outer_diameter']:.1f} mm<br>
            • Thickness: {gear_data['thickness']} mm<br>
            • Bore Ø: {gear_data['bore_diameter']} mm<br>
            • Material: {gear_data['material']}<br>
            """
            
            fig.add_trace(go.Scatter(
                x=[0], y=[0],
                mode='text',
                text=[specs_text],
                textposition="middle left",
                showlegend=False
            ), row=2, col=1)
        
        # Add assembly instructions
        instructions_text = """
        <b>Assembly Instructions:</b><br>
        1. Press fit bearing into housing<br>
        2. Install gear on shaft with key<br>
        3. Secure with retaining ring<br>
        4. Lubricate with EP-2 grease<br>
        5. Torque bolts to 25 Nm<br>
        6. Check gear backlash: 0.1-0.2mm<br>
        """
        
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='text',
            text=[instructions_text],
            textposition="middle left",
            showlegend=False
        ), row=2, col=2)
        
        fig.update_layout(
            title_text="3D Mechanical Components Design",
            height=900,
            showlegend=True
        )
        
        # Update 3D scene settings
        fig.update_scenes(
            aspectmode='data',
            camera_eye=dict(x=1.5, y=1.5, z=1.5)
        )
        
        return fig
    
    def generate_technical_specs(self):
        """Generate technical specifications document"""
        specs = {
            "project": "Mechanical Components Design",
            "units": "mm",
            "components": [],
            "material_properties": {
                "Steel AISI 4140": {
                    "density": "7.85 g/cm³",
                    "tensile_strength": "655 MPa",
                    "yield_strength": "415 MPa",
                    "application": "Gears, shafts, high-strength components"
                },
                "Cast Iron": {
                    "density": "7.2 g/cm³", 
                    "tensile_strength": "250 MPa",
                    "compressive_strength": "1000 MPa",
                    "application": "Housings, frames, structural components"
                }
            },
            "design_notes": [
                "All dimensions in millimeters",
                "Tolerances: ISO 2768-m",
                "Surface finish: 1.6 μm Ra unless specified",
                "Remove sharp edges and burrs"
            ]
        }
        
        # Convert components to JSON-serializable format
        for comp in self.components:
            serializable_comp = comp.copy()
            # Remove numpy arrays if they exist
            if 'theta' in serializable_comp:
                serializable_comp['theta'] = serializable_comp['theta']  # Already converted to list
            if 'radii' in serializable_comp:
                serializable_comp['radii'] = serializable_comp['radii']  # Already converted to list
            specs["components"].append(serializable_comp)
        
        return specs
    
    def export_design(self, filename_prefix="mechanical_design"):
        """Export all design files"""
        os.makedirs("outputs", exist_ok=True)
        
        try:
            # Save technical specifications
            specs = self.generate_technical_specs()
            with open(f"outputs/{filename_prefix}_specs.json", "w") as f:
                json.dump(specs, f, indent=2, ensure_ascii=False)
            
            # Save 2D drawings
            gear_data = next((comp for comp in self.components if comp['type'] == 'spur_gear'), None)
            if gear_data:
                fig_2d = self.plot_gear_2d(gear_data)
                fig_2d.savefig(f"outputs/{filename_prefix}_2d_drawing.png", dpi=300, bbox_inches='tight')
                plt.close(fig_2d)
            
            # Save 3D visualization
            fig_3d = self.create_3d_visualization()
            fig_3d.write_html(f"outputs/{filename_prefix}_3d_view.html")
            
            # Generate manufacturing instructions
            self.generate_manufacturing_instructions(filename_prefix)
            
            # Generate a simple STEP file placeholder
            self.generate_step_placeholder(filename_prefix)
            
            print(f"✓ Design exported to 'outputs/' directory:")
            print(f"  - {filename_prefix}_specs.json (Technical specifications)")
            print(f"  - {filename_prefix}_2d_drawing.png (2D technical drawing)")
            print(f"  - {filename_prefix}_3d_view.html (Interactive 3D view)")
            print(f"  - {filename_prefix}_manufacturing.txt (Manufacturing instructions)")
            print(f"  - {filename_prefix}_model.step (CAD model placeholder)")
            
        except Exception as e:
            print(f"✗ Error during export: {e}")
            print("Please check if all directories are writable.")
    
    def generate_manufacturing_instructions(self, filename_prefix):
        """Generate basic manufacturing instructions"""
        instructions = "MANUFACTURING INSTRUCTIONS\n"
        instructions += "=" * 50 + "\n\n"
        
        for comp in self.components:
            if comp['type'] == 'spur_gear':
                instructions += f"SPUR GEAR MANUFACTURING:\n"
                instructions += f"Material: {comp['material']}\n"
                instructions += f"Number of teeth: {comp['teeth']}\n"
                instructions += f"Module: {comp['module']} mm\n"
                instructions += f"Pitch diameter: {comp['pitch_diameter']:.1f} mm\n"
                instructions += f"Outer diameter: {comp['outer_diameter']:.1f} mm\n"
                instructions += f"Bore diameter: {comp['bore_diameter']} mm\n"
                instructions += f"Thickness: {comp['thickness']} mm\n\n"
                
                instructions += "Manufacturing Steps:\n"
                instructions += f"1. Cut gear blank from {comp['material']} stock\n"
                instructions += "2. Rough turn to outer diameter\n"
                instructions += "3. Bore center hole to size\n"
                instructions += "4. Cut teeth using gear hobbing machine\n"
                instructions += "5. Heat treatment: Carburize and harden to 55-60 HRC\n"
                instructions += "6. Grind bore to final size\n"
                instructions += "7. Deburr and inspect\n\n"
                
                instructions += "Quality Requirements:\n"
                instructions += "- AGMA Quality Class 8 or better\n"
                instructions += "- Tooth profile tolerance: ±0.02 mm\n"
                instructions += "- Runout: < 0.05 mm\n"
                instructions += "- Surface finish: 0.8 μm Ra on teeth\n\n"
            
            elif comp['type'] == 'bearing_housing':
                instructions += f"BEARING HOUSING MANUFACTURING:\n"
                instructions += f"Material: {comp['material']}\n"
                instructions += f"Outer diameter: {comp['outer_diameter']} mm\n"
                instructions += f"Bore diameter: {comp['inner_diameter']} mm\n"
                instructions += f"Width: {comp['width']} mm\n\n"
                
                instructions += "Manufacturing Steps:\n"
                instructions += "1. Cast housing to near-net shape\n"
                instructions += "2. Rough machine all surfaces\n"
                instructions += "3. Finish bore to H7 tolerance\n"
                instructions += "4. Machine mounting surfaces\n"
                instructions += "5. Drill and tap bolt holes\n"
                instructions += "6. Deburr and clean\n\n"
                
                instructions += "Quality Requirements:\n"
                instructions += "- Bore tolerance: H7\n"
                instructions += "- Surface finish: 1.6 μm Ra in bore\n"
                instructions += "- Concentricity: 0.03 mm\n\n"
        
        instructions += "GENERAL NOTES:\n"
        instructions += "- All dimensions in millimeters\n"
        instructions += "- Apply anti-corrosion coating after machining\n"
        instructions += "- Use appropriate cutting fluids during machining\n"
        instructions += "- Follow all safety procedures\n"
        
        with open(f"outputs/{filename_prefix}_manufacturing.txt", "w") as f:
            f.write(instructions)
    
    def generate_step_placeholder(self, filename_prefix):
        """Generate a placeholder STEP file with metadata"""
        # Use double curly braces to escape them in f-strings
        component_type = self.components[0]['type'] if self.components else 'Unknown'
        
        step_content = f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Mechanical Component Design'), '2;1');
FILE_NAME('{filename_prefix}_model.step', '2024-01-01T00:00:00', 
    ('CAD Generator'), ('3D CAD Python System'), 'v1.0', '');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN {{ 1 0 10303 214 1 1 1 1 }}'));
ENDSEC;

DATA;
/* This is a placeholder STEP file */
/* Actual CAD geometry would be generated by commercial CAD software */
/* Component: {component_type} */
/* Generated by Python CAD System */

ENDSEC;
END-ISO-10303-21;
"""
        
        with open(f"outputs/{filename_prefix}_model.step", "w") as f:
            f.write(step_content)

def main():
    """Main demonstration function"""
    print("3D CAD Model Creation System")
    print("=" * 50)
    
    # Initialize CAD generator
    cad = WorkingCADGenerator()
    
    try:
        # Design components
        print("\n1. Designing Spur Gear...")
        gear = cad.create_spur_gear(
            teeth=24,
            module=2.5,
            thickness=15,
            bore_diameter=12
        )
        
        print("\n2. Designing Bearing Housing...")
        housing = cad.create_bearing_housing(
            inner_diameter=35,
            outer_diameter=65,
            width=30
        )
        
        print("\n3. Generating Technical Documentation...")
        specs = cad.generate_technical_specs()
        
        print("\n4. Exporting Design Files...")
        cad.export_design("my_mechanical_component")
        
        print("\n" + "=" * 50)
        print("DESIGN COMPLETED SUCCESSFULLY! 🎉")
        print("\nGenerated Files in 'outputs/' folder:")
        print("✅ 2D Technical drawings (PNG)")
        print("✅ 3D Interactive visualization (HTML)")
        print("✅ Technical specifications (JSON)")
        print("✅ Manufacturing instructions (TXT)")
        print("✅ CAD model placeholder (STEP)")
        print("\n📁 Open 'outputs/my_mechanical_component_3d_view.html' in your browser for 3D view!")
        print("📁 Check 'outputs/my_mechanical_component_2d_drawing.png' for technical drawing!")
        
    except Exception as e:
        print(f"\n❌ Error during design process: {e}")
        print("Please check the error message above.")

if __name__ == "__main__":
    main()