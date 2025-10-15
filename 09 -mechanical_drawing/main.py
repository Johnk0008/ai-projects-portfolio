"""
Mechanical Drawing Generator - Flange Bearing Housing
JOHN AI/ML Engineer - Technical Drawing Solution
"""

from drawing_library import create_autocad_equivalent_files
import os

def main():
    print("=" * 60)
    print("MECHANICAL DRAWING GENERATOR")
    print("Flange Bearing Housing - Technical Drawing")
    print("=" * 60)
    
    # Create outputs directory if it doesn't exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
        print("Created 'outputs' directory")
    
    try:
        # Generate all drawings and specifications
        create_autocad_equivalent_files()
        
        print("\n" + "=" * 60)
        print("GENERATION COMPLETE!")
        print("=" * 60)
        print("\nGenerated Files:")
        print("✅ flange_drawing.pdf - Technical drawing (PDF format)")
        print("✅ technical_specifications.txt - Detailed specs")
        print("✅ flange_drawing.png - High-res image")
        print("\nThese files can be used as reference for AutoCAD drawing.")
        
    except Exception as e:
        print(f"Error during generation: {e}")

if __name__ == "__main__":
    main()