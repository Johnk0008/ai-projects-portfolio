#!/usr/bin/env python3
"""
3D CAD Model Creation System
Mechanical Component Generator
"""

import os
import json
from src.cad_generator import CADGenerator
from src.gear_design import SpurGear, BearingHousing
from src.visualization import CADVisualizer
from src.export_utils import ExportManager

def main():
    """Main function to demonstrate CAD model creation"""
    print("=== 3D CAD Model Creation System ===")
    
    # Initialize components
    cad_gen = CADGenerator()
    visualizer = CADVisualizer()
    exporter = ExportManager()
    
    # Create output directory
    os.makedirs("outputs", exist_ok=True)
    
    # Example 1: Create a Spur Gear
    print("\n1. Creating Spur Gear...")
    gear_params = {
        "module": 2.0,
        "teeth": 20,
        "pressure_angle": 20,
        "thickness": 10,
        "bore_diameter": 10,
        "material": "Steel AISI 4140"
    }
    
    spur_gear = SpurGear(**gear_params)
    gear_mesh = spur_gear.generate()
    
    # Visualize gear
    visualizer.plot_mesh(gear_mesh, "Spur Gear")
    visualizer.save_render("outputs/spur_gear_render.png")
    
    # Export gear
    exporter.export_stl(gear_mesh, "outputs/spur_gear.stl")
    exporter.export_step(gear_mesh, "outputs/spur_gear.step")
    
    # Example 2: Create Bearing Housing
    print("\n2. Creating Bearing Housing...")
    bearing_params = {
        "inner_diameter": 30,
        "outer_diameter": 60,
        "width": 25,
        "bolt_hole_diameter": 6,
        "material": "Cast Iron"
    }
    
    bearing_housing = BearingHousing(**bearing_params)
    housing_mesh = bearing_housing.generate()
    
    # Visualize housing
    visualizer.plot_mesh(housing_mesh, "Bearing Housing")
    visualizer.save_render("outputs/bearing_housing_render.png")
    
    # Export housing
    exporter.export_stl(housing_mesh, "outputs/bearing_housing.stl")
    
    # Generate technical documentation
    generate_documentation(gear_params, bearing_params)
    
    print("\n=== CAD Model Generation Complete ===")
    print("Check 'outputs' directory for generated files:")
    print("- STL files for 3D printing")
    print("- STEP files for CAD software")
    print("- Rendered images")
    print("- Technical specifications")

def generate_documentation(gear_params, bearing_params):
    """Generate technical documentation"""
    doc = {
        "project": "3D CAD Mechanical Components",
        "components": {
            "spur_gear": {
                **gear_params,
                "description": "Standard spur gear for power transmission",
                "applications": ["Gearboxes", "Power transmission systems"]
            },
            "bearing_housing": {
                **bearing_params,
                "description": "Bearing housing for radial ball bearings",
                "applications": ["Motor mounts", "Machine frames"]
            }
        },
        "material_properties": {
            "Steel AISI 4140": {
                "density": "7.85 g/cm³",
                "tensile_strength": "655 MPa",
                "yield_strength": "415 MPa"
            },
            "Cast Iron": {
                "density": "7.2 g/cm³",
                "tensile_strength": "250 MPa",
                "compressive_strength": "1000 MPa"
            }
        }
    }
    
    with open("outputs/technical_specifications.json", "w") as f:
        json.dump(doc, f, indent=2)

if __name__ == "__main__":
    main()