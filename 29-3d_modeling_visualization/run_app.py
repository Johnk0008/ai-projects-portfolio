#!/usr/bin/env python3
"""
Run script for 3D Modeling & Visualization Application
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import ModelingVisualizationApp

def main():
    """Main execution function"""
    print("Starting 3D Modeling & Visualization Application...")
    
    try:
        # Initialize and run the application
        app = ModelingVisualizationApp()
        
        # Run all designs
        results = app.run_all_designs()
        
        print("\n" + "="*60)
        print("APPLICATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nTo view your 3D models:")
        print("1. Check 'output/models/' for structure files (.json, .obj)")
        print("2. Check 'output/renders/' for rendered images (.png)")
        print("3. Check 'output/textures/' for generated textures")
        
        print("\nGenerated files include:")
        print("- House design with brick and wood materials")
        print("- Bridge component with concrete materials") 
        print("- Commercial block with concrete and glass materials")
        print("- Multiple view renders for each structure")
        print("- Composite overview images")
        
    except Exception as e:
        print(f"Error running application: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install numpy matplotlib plotly open3d pyvista torch pillow")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())