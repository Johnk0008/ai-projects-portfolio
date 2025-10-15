import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import json
import os

class AdvancedFloorPlanGenerator:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(16, 12))
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(0, 40)
        self.ax.grid(True, alpha=0.2)
        self.ax.set_title('Advanced 2D Floor Plan - Residential House', 
                         fontsize=18, fontweight='bold', pad=20)
        self.room_data = {}  # This will store all room information
        
    def draw_wall(self, x, y, width, height, thickness=0.3, color='#8B4513', style='solid'):
        """Draw walls with specified thickness and style"""
        wall = Rectangle((x, y), width, height, 
                        facecolor=color, 
                        edgecolor='black',
                        linewidth=2,
                        linestyle=style,
                        alpha=0.8)
        self.ax.add_patch(wall)
        
    def draw_door(self, x, y, width, direction='horizontal'):
        """Draw detailed doors with swing direction"""
        if direction == 'horizontal':
            door = Rectangle((x, y), width, 0.1, 
                           facecolor='#654321', edgecolor='black', linewidth=1)
            self.ax.add_patch(door)
            # Door swing arc
            swing_angle = np.linspace(0, 90, 30)
            swing_x = x + width * np.cos(np.radians(swing_angle))
            swing_y = y + width * np.sin(np.radians(swing_angle))
            self.ax.plot(swing_x, swing_y, 'k--', alpha=0.5, linewidth=1)
        else:
            door = Rectangle((x, y), 0.1, width, 
                           facecolor='#654321', edgecolor='black', linewidth=1)
            self.ax.add_patch(door)
            
    def draw_window(self, x, y, width, height=0.1):
        """Draw detailed windows"""
        window = Rectangle((x, y), width, height,
                         facecolor='#87CEEB', edgecolor='darkblue', 
                         linewidth=2, alpha=0.8)
        self.ax.add_patch(window)
        # Window divisions
        divisions = 3
        for i in range(1, divisions):
            div_x = x + (width / divisions) * i
            self.ax.plot([div_x, div_x], [y, y + height], 'darkblue', linewidth=1)
        
    def draw_room(self, x, y, width, height, room_name, room_type, 
                  door_positions=None, window_positions=None):
        """Draw a room with enhanced features"""
        # Store room data for reporting
        self.room_data[room_name] = {
            'type': room_type,
            'position': (x, y),
            'dimensions': (width, height),
            'area': width * height,
            'doors': len(door_positions) if door_positions else 0,
            'windows': len(window_positions) if window_positions else 0
        }
        
        # Draw walls
        self.draw_wall(x, y, width, height)
        
        # Draw doors
        if door_positions:
            for door_x, door_y, door_width, direction in door_positions:
                self.draw_door(door_x, door_y, door_width, direction)
            
        # Draw windows
        if window_positions:
            for win_x, win_y, win_width in window_positions:
                self.draw_window(win_x, win_y, win_width)
        
        # Add room label with background
        self.ax.text(x + width/2, y + height/2, f"{room_name}\n{width}m × {height}m\n{width*height:.1f} sqm", 
                    ha='center', va='center', fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.4", facecolor='lightblue', 
                             edgecolor='navy', alpha=0.8))
        
        # Add dimensions
        self.add_dimensions(x, y, width, height)
    
    def add_dimensions(self, x, y, width, height):
        """Add detailed dimension lines"""
        # Horizontal dimension
        dim_y = y - 1.5
        self.ax.plot([x, x + width], [dim_y, dim_y], 'k-', lw=1)
        self.ax.plot([x, x], [dim_y - 0.2, dim_y + 0.2], 'k-', lw=1)
        self.ax.plot([x + width, x + width], [dim_y - 0.2, dim_y + 0.2], 'k-', lw=1)
        self.ax.text(x + width/2, dim_y - 0.5, f'{width:.1f}m', 
                    ha='center', va='top', fontsize=8, fontweight='bold')
        
        # Vertical dimension
        dim_x = x - 1.5
        self.ax.plot([dim_x, dim_x], [y, y + height], 'k-', lw=1)
        self.ax.plot([dim_x - 0.2, dim_x + 0.2], [y, y], 'k-', lw=1)
        self.ax.plot([dim_x - 0.2, dim_x + 0.2], [y + height, y + height], 'k-', lw=1)
        self.ax.text(dim_x - 0.8, y + height/2, f'{height:.1f}m', 
                    ha='center', va='center', fontsize=8, fontweight='bold', rotation=90)
    
    def draw_advanced_furniture(self, room_type, x, y, width, height):
        """Draw enhanced furniture with more details"""
        furniture_color = '#D2B48C'
        dark_wood = '#8B4513'
        
        if room_type == "Bedroom":
            # Bed with pillows
            bed = Rectangle((x + 1, y + 1), 2, 1.5, facecolor=furniture_color, 
                          edgecolor='black', linewidth=1)
            self.ax.add_patch(bed)
            
            # Pillows
            pillow1 = Rectangle((x + 1.2, y + 2), 0.6, 0.3, facecolor='white', edgecolor='gray')
            pillow2 = Rectangle((x + 2.2, y + 2), 0.6, 0.3, facecolor='white', edgecolor='gray')
            self.ax.add_patch(pillow1)
            self.ax.add_patch(pillow2)
            
            # Wardrobe
            wardrobe = Rectangle((x + width - 1.5, y + 1), 0.8, 1.8, 
                               facecolor=dark_wood, edgecolor='black')
            self.ax.add_patch(wardrobe)
            
            # Dresser
            dresser = Rectangle((x + 0.5, y + 1), 1.2, 0.4, facecolor=dark_wood, edgecolor='black')
            self.ax.add_patch(dresser)
            
        elif room_type == "Living Room":
            # Sectional Sofa
            sofa_main = Rectangle((x + 1, y + 1), 2.5, 0.8, facecolor=furniture_color, edgecolor='black')
            sofa_side = Rectangle((x + 1, y + 1), 0.8, 1.5, facecolor=furniture_color, edgecolor='black')
            self.ax.add_patch(sofa_main)
            self.ax.add_patch(sofa_side)
            
            # Coffee Table
            table = Rectangle((x + 2, y + 2), 1, 0.6, facecolor=dark_wood, edgecolor='black')
            self.ax.add_patch(table)
            
            # TV Stand with TV
            tv_stand = Rectangle((x + width - 2, y + 1), 1.5, 0.4, facecolor=dark_wood, edgecolor='black')
            tv = Rectangle((x + width - 1.8, y + 1.5), 1, 0.6, facecolor='black', edgecolor='gray')
            self.ax.add_patch(tv_stand)
            self.ax.add_patch(tv)
            
        elif room_type == "Kitchen":
            # L-shaped counter
            counter1 = Rectangle((x + 1, y + 1), width - 2, 0.6, facecolor='#696969', edgecolor='black')
            counter2 = Rectangle((x + 1, y + 1), 0.6, 2, facecolor='#696969', edgecolor='black')
            self.ax.add_patch(counter1)
            self.ax.add_patch(counter2)
            
            # Sink
            sink = Circle((x + 2, y + 1.3), 0.2, facecolor='lightgray', edgecolor='black')
            self.ax.add_patch(sink)
            
            # Stove with burners
            stove = Rectangle((x + width - 2, y + 1), 0.8, 0.6, facecolor='black', edgecolor='black')
            self.ax.add_patch(stove)
            for i in range(2):
                for j in range(2):
                    burner = Circle((x + width - 1.6 + i*0.3, y + 1.2 + j*0.2), 0.08, 
                                  facecolor='gray', edgecolor='white')
                    self.ax.add_patch(burner)
                    
        elif room_type == "Bathroom":
            # Toilet
            toilet = Rectangle((x + 1, y + 1), 0.6, 0.8, facecolor='white', edgecolor='black')
            self.ax.add_patch(toilet)
            
            # Sink
            sink = Rectangle((x + 2, y + 1), 0.6, 0.4, facecolor='white', edgecolor='black')
            self.ax.add_patch(sink)
            
            # Shower
            shower = Rectangle((x + width - 2, y + 1), 1.2, 1.2, facecolor='#708090', edgecolor='black')
            self.ax.add_patch(shower)
    
    def create_advanced_floor_plan(self):
        """Create enhanced floor plan with more details"""
        
        # Main structure
        main_width, main_height = 35, 30
        self.draw_wall(5, 5, main_width, main_height, thickness=0.3)
        
        # Bedroom 1 (Master Bedroom)
        self.draw_room(7, 22, 8, 10, "Master Bedroom", "Bedroom",
                      door_positions=[(12, 22, 0.8, 'horizontal')],
                      window_positions=[(8, 31.7, 2)])
        self.draw_advanced_furniture("Bedroom", 7, 22, 8, 10)
        
        # Bedroom 2
        self.draw_room(17, 22, 8, 10, "Bedroom 2", "Bedroom",
                      door_positions=[(22, 22, 0.8, 'horizontal')],
                      window_positions=[(18, 31.7, 2)])
        self.draw_advanced_furniture("Bedroom", 17, 22, 8, 10)
        
        # Bathroom
        self.draw_room(27, 22, 10, 6, "Bathroom", "Bathroom",
                      door_positions=[(27, 22, 0.8, 'horizontal')])
        self.draw_advanced_furniture("Bathroom", 27, 22, 10, 6)
        
        # Living Room
        self.draw_room(7, 10, 18, 10, "Living Room", "Living Room",
                      door_positions=[(12, 10, 0.8, 'horizontal')],
                      window_positions=[(8, 19.7, 3), (15, 19.7, 3)])
        self.draw_advanced_furniture("Living Room", 7, 10, 18, 10)
        
        # Kitchen
        self.draw_room(27, 10, 10, 10, "Kitchen", "Kitchen",
                      door_positions=[(27, 10, 0.8, 'horizontal')],
                      window_positions=[(29, 19.7, 2)])
        self.draw_advanced_furniture("Kitchen", 27, 10, 10, 10)
        
        # Hallway
        hallway = Rectangle((12, 10), 13, 12, 
                          facecolor='#F5F5F5', edgecolor='black', alpha=0.3, linestyle='--')
        self.ax.add_patch(hallway)
        self.ax.text(18.5, 16, 'HALLWAY', ha='center', va='center', fontsize=11, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.4", facecolor='white', edgecolor='gray'))
        
        # Main entrance
        entrance = Rectangle((18, 5), 4, 0.3, facecolor='#654321', edgecolor='black')
        self.ax.add_patch(entrance)
        self.ax.text(20, 4.5, 'MAIN ENTRANCE', ha='center', va='top', 
                    fontsize=11, fontweight='bold', style='italic')
        
        # Add scale and north arrow
        self.add_scale_and_arrow()
        
        # Add legend
        self.add_legend()
    
    def add_scale_and_arrow(self):
        """Add scale bar and north arrow"""
        # Scale bar
        scale_length = 5
        self.ax.plot([5, 5 + scale_length], [3, 3], 'k-', lw=3)
        self.ax.text(7.5, 2.5, f'{scale_length} meters', ha='center', va='top', 
                    fontsize=10, fontweight='bold')
        
        # North arrow
        arrow_x, arrow_y = 45, 35
        self.ax.arrow(arrow_x, arrow_y, 0, 2, head_width=0.5, head_length=0.5, 
                     fc='red', ec='red', linewidth=2)
        self.ax.text(arrow_x, arrow_y - 1, 'N', ha='center', va='bottom', 
                    fontsize=12, fontweight='bold', color='red')
    
    def add_legend(self):
        """Add a legend to the floor plan"""
        legend_elements = [
            ('Walls', '#8B4513'),
            ('Doors', '#654321'),
            ('Windows', '#87CEEB'),
            ('Furniture', '#D2B48C')
        ]
        
        legend_x, legend_y = 40, 15
        for i, (label, color) in enumerate(legend_elements):
            self.ax.add_patch(Rectangle((legend_x, legend_y - i*1.5), 1, 0.8, 
                                      facecolor=color, edgecolor='black'))
            self.ax.text(legend_x + 1.2, legend_y - i*1.5 + 0.4, label, 
                        ha='left', va='center', fontsize=9)
    
    def generate_room_data_json(self):
        """Generate JSON data for room specifications and return the data"""
        total_area = sum(room['area'] for room in self.room_data.values())
        
        spec_data = {
            "project": "Advanced Residential Floor Plan",
            "total_area_sqm": total_area,
            "room_count": len(self.room_data),
            "rooms": self.room_data,
            "specifications": {
                "wall_thickness": "0.3m",
                "ceiling_height": "2.7m",
                "floor_material": "Hardwood & Tile",
                "window_type": "Double-glazed",
                "door_type": "Solid core"
            }
        }
        
        with open('room_specifications.json', 'w') as f:
            json.dump(spec_data, f, indent=2)
        
        print("Room specifications JSON generated: room_specifications.json")
        return spec_data  # Return the data, not just the filename
    
    def get_room_data(self):
        """Get the room data dictionary"""
        return self.room_data
    
    def save_as_pdf(self, filename='advanced_floor_plan.pdf'):
        """Save the floor plan as high-quality PDF"""
        plt.savefig(filename, dpi=300, bbox_inches='tight', format='pdf')
        print(f"Advanced PDF saved as {filename}")
    
    def show_plan(self):
        """Display the floor plan"""
        plt.tight_layout()
        plt.show()

def create_professional_pdf_report(room_data):
    """Create a professional PDF report with multiple pages"""
    doc = SimpleDocTemplate("professional_floor_plan_report.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("PROFESSIONAL FLOOR PLAN REPORT", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Project Overview
    overview = Paragraph("Project Overview", styles['Heading2'])
    story.append(overview)
    
    # Calculate total area from room data
    total_area = sum(room_info['area'] for room_info in room_data.values())
    
    overview_text = f"""
    This professional floor plan represents a modern residential house with optimal space utilization.
    Total Built-up Area: <b>{total_area:.1f} square meters</b>
    Number of Rooms: <b>{len(room_data)}</b>
    Designed for: <b>Family Living</b>
    """
    story.append(Paragraph(overview_text, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Room Specifications Table
    room_table_data = [['Room', 'Type', 'Dimensions', 'Area (sqm)', 'Doors', 'Windows']]
    for room_name, data in room_data.items():
        room_table_data.append([
            room_name,
            data['type'],
            f"{data['dimensions'][0]}m × {data['dimensions'][1]}m",
            f"{data['area']:.1f}",
            str(data['doors']),
            str(data['windows'])
        ])
    
    room_table = Table(room_table_data)
    room_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(room_table)
    story.append(Spacer(1, 20))
    
    # Features
    features = Paragraph("Key Features", styles['Heading2'])
    story.append(features)
    feature_text = """
    • Optimal room placement for natural light
    • Efficient circulation with central hallway
    • Master bedroom with ensuite bathroom proximity
    • Open living area concept
    • Modern kitchen layout with ample workspace
    • Proper ventilation and window placement
    • Furniture-optimized room dimensions
    """
    story.append(Paragraph(feature_text, styles['Normal']))
    
    # Additional Specifications
    specs = Paragraph("Technical Specifications", styles['Heading2'])
    story.append(specs)
    specs_text = f"""
    • Total Area: {total_area:.1f} sqm
    • Number of Bedrooms: {sum(1 for room in room_data.values() if room['type'] == 'Bedroom')}
    • Number of Bathrooms: {sum(1 for room in room_data.values() if room['type'] == 'Bathroom')}
    • Living Areas: {sum(1 for room in room_data.values() if room['type'] in ['Living Room', 'Kitchen'])}
    • Average Room Size: {total_area/len(room_data):.1f} sqm
    """
    story.append(Paragraph(specs_text, styles['Normal']))
    
    doc.build(story)
    print("Professional PDF report created: professional_floor_plan_report.pdf")

def main():
    """Main function to generate advanced floor plan"""
    print("🚀 Generating Advanced 2D Floor Plan...")
    
    # Create advanced floor plan
    generator = AdvancedFloorPlanGenerator()
    generator.create_advanced_floor_plan()
    
    # Get room data directly from the generator
    room_data = generator.get_room_data()
    
    # Generate room data JSON (this also returns the data)
    json_data = generator.generate_room_data_json()
    
    # Save outputs
    generator.save_as_pdf('advanced_floor_plan.pdf')
    plt.savefig('advanced_floor_plan.png', dpi=300, bbox_inches='tight')
    
    # Create professional report using the room data
    create_professional_pdf_report(room_data)
    
    # Show the plan
    generator.show_plan()
    
    print("\n" + "="*60)
    print("🎉 ENHANCED FILES GENERATED:")
    print("="*60)
    print("1. 📄 advanced_floor_plan.pdf - Enhanced floor plan with details")
    print("2. 🖼️  advanced_floor_plan.png - High-resolution image")
    print("3. 📊 professional_floor_plan_report.pdf - Professional report")
    print("4. 📋 room_specifications.json - Room data in JSON format")
    print("="*60)
    print("✨ Features included:")
    print("   • Detailed furniture with textures")
    print("   • Dimension arrows and labels")
    print("   • North arrow and scale bar")
    print("   • Professional legend")
    print("   • Room area calculations")
    print("   • JSON data export")
    print("="*60)

if __name__ == "__main__":
    main()