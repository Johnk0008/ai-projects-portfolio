import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import numpy as np
import os
import sys

class FloorPlanGenerator:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(15, 10))
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(0, 40)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title('2D Floor Plan - Residential House', fontsize=16, fontweight='bold')
        
    def draw_wall(self, x, y, width, height, thickness=0.3, color='#8B4513'):
        """Draw walls with specified thickness"""
        wall = Rectangle((x, y), width, height, 
                        facecolor=color, 
                        edgecolor='black',
                        linewidth=1)
        self.ax.add_patch(wall)
        
    def draw_room(self, x, y, width, height, room_name, door_position=None, window_positions=None):
        """Draw a room with walls and label"""
        # Draw walls
        self.draw_wall(x, y, width, height)
        
        # Draw door if specified
        if door_position:
            door_x, door_y, door_width = door_position
            door = Rectangle((door_x, door_y), door_width, 0.1, 
                           facecolor='#654321', edgecolor='black')
            self.ax.add_patch(door)
            
        # Draw windows if specified
        if window_positions:
            for win_x, win_y, win_width in window_positions:
                window = Rectangle((win_x, win_y), win_width, 0.1,
                                 facecolor='#87CEEB', edgecolor='black', alpha=0.7)
                self.ax.add_patch(window)
        
        # Add room label
        self.ax.text(x + width/2, y + height/2, room_name, 
                    ha='center', va='center', fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
        
        # Add dimensions
        self.add_dimensions(x, y, width, height)
    
    def add_dimensions(self, x, y, width, height):
        """Add dimension lines to the room"""
        # Horizontal dimension
        self.ax.plot([x, x + width], [y - 1, y - 1], 'k-', lw=1)
        self.ax.plot([x, x], [y - 0.8, y - 1.2], 'k-', lw=1)
        self.ax.plot([x + width, x + width], [y - 0.8, y - 1.2], 'k-', lw=1)
        self.ax.text(x + width/2, y - 1.5, f'{width}m', ha='center', va='top', fontsize=8)
        
        # Vertical dimension
        self.ax.plot([x - 1, x - 1], [y, y + height], 'k-', lw=1)
        self.ax.plot([x - 1.2, x - 0.8], [y, y], 'k-', lw=1)
        self.ax.plot([x - 1.2, x - 0.8], [y + height, y + height], 'k-', lw=1)
        self.ax.text(x - 1.5, y + height/2, f'{height}m', ha='center', va='center', 
                    fontsize=8, rotation=90)
    
    def draw_furniture(self, room_type, x, y, width, height):
        """Draw furniture based on room type"""
        furniture_color = '#D2B48C'
        
        if room_type == "Bedroom":
            # Bed
            bed = Rectangle((x + 1, y + 1), 2, 1.5, facecolor=furniture_color, edgecolor='black')
            self.ax.add_patch(bed)
            self.ax.text(x + 2, y + 1.75, 'Bed', ha='center', va='center', fontsize=8)
            
            # Wardrobe
            wardrobe = Rectangle((x + width - 1.5, y + 1), 0.8, 1.2, 
                               facecolor='#A0522D', edgecolor='black')
            self.ax.add_patch(wardrobe)
            
            # Nightstand
            nightstand = Rectangle((x + 0.5, y + 1), 0.4, 0.4, facecolor='#8B4513', edgecolor='black')
            self.ax.add_patch(nightstand)
            
        elif room_type == "Living Room":
            # Sofa
            sofa = Rectangle((x + 1, y + 1), 2.5, 0.8, facecolor=furniture_color, edgecolor='black')
            self.ax.add_patch(sofa)
            self.ax.text(x + 2.25, y + 1.4, 'Sofa', ha='center', va='center', fontsize=8)
            
            # TV Stand
            tv_stand = Rectangle((x + width - 2, y + 1), 1.5, 0.4, facecolor='#A0522D', edgecolor='black')
            self.ax.add_patch(tv_stand)
            self.ax.text(x + width - 1.25, y + 1.2, 'TV', ha='center', va='center', fontsize=8)
            
        elif room_type == "Kitchen":
            # Counter
            counter = Rectangle((x + 1, y + 1), width - 2, 0.6, facecolor='#696969', edgecolor='black')
            self.ax.add_patch(counter)
            
            # Sink
            sink = Circle((x + 2, y + 1.3), 0.2, facecolor='white', edgecolor='black')
            self.ax.add_patch(sink)
            
            # Stove
            stove = Rectangle((x + width - 2, y + 1), 0.8, 0.6, facecolor='black', edgecolor='black')
            self.ax.add_patch(stove)
            
        elif room_type == "Bathroom":
            # Toilet
            toilet = Rectangle((x + 1, y + 1), 0.6, 0.8, facecolor='white', edgecolor='black')
            self.ax.add_patch(toilet)
            
            # Shower
            shower = Rectangle((x + width - 2, y + 1), 1.2, 1.2, facecolor='#708090', edgecolor='black')
            self.ax.add_patch(shower)
    
    def create_floor_plan(self):
        """Create the complete floor plan"""
        
        # Main structure
        main_width, main_height = 35, 30
        self.draw_wall(5, 5, main_width, main_height, thickness=0.3)
        
        # Bedroom 1 (Master Bedroom)
        self.draw_room(7, 22, 8, 10, "Master Bedroom", 
                      door_position=(12, 22, 0.8),
                      window_positions=[(8, 31.7, 2)])
        self.draw_furniture("Bedroom", 7, 22, 8, 10)
        
        # Bedroom 2
        self.draw_room(17, 22, 8, 10, "Bedroom 2",
                      door_position=(22, 22, 0.8),
                      window_positions=[(18, 31.7, 2)])
        self.draw_furniture("Bedroom", 17, 22, 8, 10)
        
        # Bathroom
        self.draw_room(27, 22, 10, 6, "Bathroom",
                      door_position=(27, 22, 0.8))
        self.draw_furniture("Bathroom", 27, 22, 10, 6)
        
        # Living Room
        self.draw_room(7, 10, 18, 10, "Living Room",
                      door_position=(12, 10, 0.8),
                      window_positions=[(8, 19.7, 3), (15, 19.7, 3)])
        self.draw_furniture("Living Room", 7, 10, 18, 10)
        
        # Kitchen
        self.draw_room(27, 10, 10, 10, "Kitchen",
                      door_position=(27, 10, 0.8),
                      window_positions=[(29, 19.7, 2)])
        self.draw_furniture("Kitchen", 27, 10, 10, 10)
        
        # Hallway
        hallway = Rectangle((12, 10), 13, 12, 
                          facecolor='#F5F5F5', edgecolor='black', alpha=0.5)
        self.ax.add_patch(hallway)
        self.ax.text(18.5, 16, 'Hallway', ha='center', va='center', fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Main entrance
        entrance = Rectangle((18, 5), 4, 0.3, facecolor='#654321', edgecolor='black')
        self.ax.add_patch(entrance)
        self.ax.text(20, 4.5, 'Main Entrance', ha='center', va='top', fontsize=10, fontweight='bold')
        
        # Add scale
        self.ax.plot([5, 10], [3, 3], 'k-', lw=2)
        self.ax.text(7.5, 2.5, '5 meters', ha='center', va='top', fontsize=10)
        
    def save_as_pdf(self, filename='floor_plan.pdf'):
        """Save the floor plan as PDF"""
        plt.savefig(filename, dpi=300, bbox_inches='tight', format='pdf')
        print(f"PDF saved as {filename}")
    
    def show_plan(self):
        """Display the floor plan"""
        plt.tight_layout()
        plt.show()

def create_simple_pdf_report():
    """Create a simple PDF report without reportlab dependency"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        
        c = canvas.Canvas("floor_plan_report.pdf", pagesize=A4)
        width, height = A4
        
        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(100, height - 100, "2D Floor Plan - Residential House")
        
        # Description
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 140, "Project: AI-Generated Floor Plan")
        c.drawString(100, height - 160, "Created by: AI/ML Engineer")
        c.drawString(100, height - 180, "Date: 2024")
        
        # Specifications
        c.drawString(100, height - 220, "Specifications:")
        c.drawString(120, height - 240, "- 2 Bedrooms (Master + Regular)")
        c.drawString(120, height - 260, "- Living Room with entertainment area")
        c.drawString(120, height - 280, "- Modern Kitchen layout")
        c.drawString(120, height - 300, "- Full Bathroom with shower")
        c.drawString(120, height - 320, "- Central Hallway")
        c.drawString(120, height - 340, "- Total Area: Approximately 105 sqm")
        
        c.save()
        print("Detailed PDF report created: floor_plan_report.pdf")
        
    except Exception as e:
        print(f"ReportLab PDF creation failed: {e}")
        print("Creating alternative text report...")
        create_text_report()

def create_text_report():
    """Create a simple text report as fallback"""
    with open("floor_plan_report.txt", "w") as f:
        f.write("2D FLOOR PLAN - RESIDENTIAL HOUSE\n")
        f.write("=" * 50 + "\n\n")
        f.write("Project: AI-Generated Floor Plan\n")
        f.write("Created by: AI/ML Engineer\n")
        f.write("Date: 2024\n\n")
        
        f.write("SPECIFICATIONS:\n")
        f.write("- 2 Bedrooms (Master + Regular)\n")
        f.write("- Living Room with entertainment area\n")
        f.write("- Modern Kitchen layout\n")
        f.write("- Full Bathroom with shower\n")
        f.write("- Central Hallway\n")
        f.write("- Total Area: Approximately 105 sqm\n\n")
        
        f.write("ROOM DIMENSIONS:\n")
        f.write("- Master Bedroom: 8m x 10m\n")
        f.write("- Bedroom 2: 8m x 10m\n")
        f.write("- Living Room: 18m x 10m\n")
        f.write("- Kitchen: 10m x 10m\n")
        f.write("- Bathroom: 10m x 6m\n")
        f.write("- Hallway: 13m x 12m\n")
    
    print("Text report created: floor_plan_report.txt")

def main():
    """Main function to generate the floor plan"""
    print("Generating 2D Floor Plan...")
    
    # Create floor plan
    generator = FloorPlanGenerator()
    generator.create_floor_plan()
    
    # Save as PDF
    generator.save_as_pdf('floor_plan.pdf')
    
    # Also save as PNG for reference
    plt.savefig('floor_plan.png', dpi=300, bbox_inches='tight')
    
    # Create detailed report (with fallback)
    create_simple_pdf_report()
    
    # Show the plan
    generator.show_plan()
    
    print("\n" + "="*50)
    print("FILES GENERATED:")
    print("1. floor_plan.pdf - Main floor plan drawing")
    print("2. floor_plan.png - High-resolution image")
    print("3. floor_plan_report.pdf/.txt - Project report")
    print("="*50)

if __name__ == "__main__":
    main()