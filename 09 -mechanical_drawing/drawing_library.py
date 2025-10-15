import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Wedge
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

class MechanicalDrawing:
    def __init__(self):
        self.fig = None
        self.axs = None
        
    def create_flange_bearing_housing(self):
        """Create a flange bearing housing with multiple views"""
        self.fig, self.axs = plt.subplots(2, 2, figsize=(15, 12))
        self.fig.suptitle('FLANGE BEARING HOUSING - TECHNICAL DRAWING', fontsize=16, fontweight='bold')
        
        # Remove the fourth subplot
        self.fig.delaxes(self.axs[1, 1])
        
        # Create different views
        self._create_front_view(self.axs[0, 0])
        self._create_top_view(self.axs[0, 1])
        self._create_side_view(self.axs[1, 0])
        
        # Add title block
        self._add_title_block()
        
        plt.tight_layout()
        return self.fig
    
    def _create_front_view(self, ax):
        """Create front view of the flange bearing housing"""
        ax.set_title('FRONT VIEW', fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Main flange
        flange_outer = Circle((0, 0), 60, fill=False, linewidth=2, color='black')
        flange_inner = Circle((0, 0), 40, fill=False, linewidth=2, color='black')
        
        # Bolt holes
        bolt_hole_positions = []
        for angle in np.linspace(0, 2*np.pi, 6, endpoint=False):
            x = 50 * np.cos(angle)
            y = 50 * np.sin(angle)
            bolt_hole = Circle((x, y), 5, fill=False, linewidth=1.5, color='black')
            ax.add_patch(bolt_hole)
            bolt_hole_positions.append((x, y))
        
        # Bearing housing
        housing_outer = Circle((0, 0), 30, fill=False, linewidth=2, color='red')
        housing_inner = Circle((0, 0), 20, fill=False, linewidth=2, color='red')
        
        # Add patches
        ax.add_patch(flange_outer)
        ax.add_patch(flange_inner)
        ax.add_patch(housing_outer)
        ax.add_patch(housing_inner)
        
        # Dimensions
        self._add_dimension(ax, -60, -60, 60, -60, 70, 'Ø120')
        self._add_dimension(ax, -40, -40, 40, -40, 50, 'Ø80')
        self._add_dimension(ax, -30, -30, 30, -30, 35, 'Ø60')
        self._add_dimension(ax, -20, -20, 20, -20, 25, 'Ø40')
        
        ax.set_xlim(-70, 70)
        ax.set_ylim(-70, 70)
        ax.set_xlabel('Width (mm)')
        ax.set_ylabel('Height (mm)')
    
    def _create_top_view(self, ax):
        """Create top view of the flange bearing housing"""
        ax.set_title('TOP VIEW', fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Main body
        main_body = Rectangle((-60, -15), 120, 30, fill=False, linewidth=2, color='black')
        
        # Flange extensions
        flange_left = Rectangle((-70, -25), 10, 50, fill=False, linewidth=2, color='black')
        flange_right = Rectangle((60, -25), 10, 50, fill=False, linewidth=2, color='black')
        
        # Bolt holes in top view
        for y in [-20, 20]:
            for x in [-55, -35, 35, 55]:
                bolt_hole = Rectangle((x-2.5, y-2.5), 5, 5, fill=False, linewidth=1.5, color='black')
                ax.add_patch(bolt_hole)
        
        # Bearing housing
        housing = Rectangle((-30, -10), 60, 20, fill=False, linewidth=2, color='red')
        
        # Add patches
        ax.add_patch(main_body)
        ax.add_patch(flange_left)
        ax.add_patch(flange_right)
        ax.add_patch(housing)
        
        # Dimensions
        self._add_dimension(ax, -60, -40, 60, -40, -45, '120')
        self._add_dimension(ax, -70, -50, -60, -50, -55, '10')
        self._add_dimension(ax, 60, -50, 70, -50, 65, '10')
        
        ax.set_xlim(-80, 80)
        ax.set_ylim(-60, 60)
        ax.set_xlabel('Length (mm)')
        ax.set_ylabel('Width (mm)')
    
    def _create_side_view(self, ax):
        """Create side view of the flange bearing housing"""
        ax.set_title('SIDE VIEW', fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Side profile
        # Base
        base = Rectangle((-60, 0), 120, 10, fill=False, linewidth=2, color='black')
        
        # Housing
        housing_outer = Rectangle((-30, 10), 60, 40, fill=False, linewidth=2, color='red')
        housing_inner = Rectangle((-20, 10), 40, 35, fill=False, linewidth=2, color='red')
        
        # Flange
        flange_left = Rectangle((-70, 0), 10, 15, fill=False, linewidth=2, color='black')
        flange_right = Rectangle((60, 0), 10, 15, fill=False, linewidth=2, color='black')
        
        # Add patches
        ax.add_patch(base)
        ax.add_patch(housing_outer)
        ax.add_patch(housing_inner)
        ax.add_patch(flange_left)
        ax.add_patch(flange_right)
        
        # Dimensions
        self._add_dimension(ax, -60, -15, 60, -15, -20, '120')
        self._add_dimension(ax, -30, -25, 30, -25, -35, '60')
        self._add_dimension(ax, 0, 0, 0, 50, 5, '50')
        
        ax.set_xlim(-80, 80)
        ax.set_ylim(-30, 60)
        ax.set_xlabel('Length (mm)')
        ax.set_ylabel('Height (mm)')
    
    def _add_dimension(self, ax, x1, y1, x2, y2, offset, text):
        """Add dimension lines and text"""
        # Dimension line
        ax.plot([x1, x2], [y1, y2], 'k--', alpha=0.7, linewidth=1)
        
        # Extension lines
        ax.plot([x1, x1], [y1, offset], 'k-', linewidth=0.8)
        ax.plot([x2, x2], [y2, offset], 'k-', linewidth=0.8)
        
        # Dimension text
        ax.text((x1 + x2) / 2, offset - 3, text, 
                ha='center', va='top', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    def _add_title_block(self):
        """Add title block with specifications"""
        title_block_text = """
TECHNICAL SPECIFICATIONS:
- Material: Cast Iron Grade 25
- Flange Diameter: Ø120 mm
- Bearing Bore: Ø40 mm
- Bolt Holes: 6x Ø10 mm equally spaced
- Surface Finish: 3.2 μm Ra
- Tolerance: ±0.1 mm
- Weight: ~2.5 kg

MANUFACTURING NOTES:
1. All sharp edges to be broken with 0.5 mm chamfer
2. Heat treatment: Stress relief annealing
3. Painting: Industrial gray enamel
4. All dimensions in millimeters

DRAWN BY: AI/ML Engineer
DATE: 2024
SCALE: 1:2
"""
        
        self.fig.text(0.02, 0.02, title_block_text, 
                     fontsize=9, family='monospace',
                     bbox=dict(boxstyle="round,pad=1", facecolor='lightgray', alpha=0.8))
    
    def save_as_pdf(self, filename='flange_bearing_housing.pdf'):
        """Save the drawing as PDF"""
        if self.fig:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"PDF saved as: {filename}")
        else:
            print("No figure to save. Please create drawing first.")
    
    def generate_technical_specs(self, filename='technical_specifications.txt'):
        """Generate technical specifications text file"""
        specs = """
FLANGE BEARING HOUSING - TECHNICAL SPECIFICATION

PART NUMBER: FBH-2024-001
DESCRIPTION: Flange Mounted Bearing Housing
MATERIAL: Cast Iron Grade 25

DIMENSIONS:
- Overall Flange Diameter: 120 mm
- Flange Thickness: 15 mm
- Bearing Bore Diameter: 40 mm
- Housing Outer Diameter: 60 mm
- Bolt Circle Diameter: 100 mm
- Number of Bolt Holes: 6
- Bolt Hole Diameter: 10 mm
- Overall Height: 50 mm

MATERIAL PROPERTIES:
- Tensile Strength: 250 MPa
- Hardness: 180-220 HB
- Density: 7.2 g/cm³

MANUFACTURING REQUIREMENTS:
1. All dimensions according to ISO 2768-m
2. Machining tolerance: ±0.1 mm
3. Surface roughness: 3.2 μm Ra
4. Deburr all sharp edges
5. Stress relief annealing required
6. Pressure test: 5 bar for 10 minutes

APPLICATION:
- Industrial machinery
- Power transmission systems
- Medium duty bearing support

NOTES:
- Use suitable sealing arrangement
- Lubrication fitting M8x1.25 required
- Mounting surface to be machined flat within 0.05 mm
"""
        
        with open(filename, 'w') as f:
            f.write(specs)
        print(f"Technical specifications saved as: {filename}")

def create_autocad_equivalent_files():
    """Create files that can be used as reference for AutoCAD"""
    drawing = MechanicalDrawing()
    
    # Generate the drawing
    fig = drawing.create_flange_bearing_housing()
    
    # Save as PDF
    drawing.save_as_pdf('outputs/flange_drawing.pdf')
    
    # Generate technical specs
    drawing.generate_technical_specs('outputs/technical_specifications.txt')
    
    # Save as high-resolution image
    plt.savefig('outputs/flange_drawing.png', dpi=300, bbox_inches='tight')
    
    plt.show()
    
    print("All files generated successfully!")
    print("1. flange_drawing.pdf - Technical drawing with multiple views")
    print("2. technical_specifications.txt - Detailed specifications")
    print("3. flange_drawing.png - High-resolution image")

if __name__ == "__main__":
    create_autocad_equivalent_files()