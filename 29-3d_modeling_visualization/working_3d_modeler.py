import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json
import os
import sys

class Simple3DModeler:
    def __init__(self):
        self.setup_directories()
        self.colors = {
            'brick': 'red',
            'concrete': 'gray', 
            'glass': 'lightblue',
            'wood': 'brown',
            'metal': 'silver'
        }
    
    def setup_directories(self):
        """Create necessary directories"""
        os.makedirs('output/models', exist_ok=True)
        os.makedirs('output/renders', exist_ok=True)
        print("✓ Directories created successfully!")
    
    def create_cube(self, position, size):
        """Create a cube mesh at given position"""
        x, y, z = position
        vertices = np.array([
            [x, y, z],
            [x + size, y, z],
            [x + size, y + size, z],
            [x, y + size, z],
            [x, y, z + size],
            [x + size, y, z + size],
            [x + size, y + size, z + size],
            [x, y + size, z + size]
        ])
        
        faces = [
            [0, 1, 2, 3],  # bottom
            [4, 5, 6, 7],  # top
            [0, 1, 5, 4],  # front
            [1, 2, 6, 5],  # right
            [2, 3, 7, 6],  # back
            [3, 0, 4, 7]   # left
        ]
        
        return vertices, faces
    
    def create_house(self):
        """Create a house structure with walls and roof"""
        print("Creating house structure...")
        
        # Main house body
        base_vertices, base_faces = self.create_cube([0, 0, 0], 8)
        
        # Roof (pyramid style)
        roof_vertices = np.array([
            [-1, -1, 8],    # 8
            [9, -1, 8],     # 9  
            [9, 9, 8],      # 10
            [-1, 9, 8],     # 11
            [4, 4, 12]      # 12 - roof peak
        ])
        
        roof_faces = [
            [0, 1, 4],  # front roof triangle (indices 8,9,12)
            [1, 2, 4],  # right roof triangle
            [2, 3, 4],  # back roof triangle  
            [3, 0, 4]   # left roof triangle
        ]
        
        # Combine all vertices
        all_vertices = np.vstack([base_vertices, roof_vertices])
        
        # Adjust roof face indices (add 8 to account for base vertices)
        roof_faces_adjusted = [[idx + 8 for idx in face] for face in roof_faces]
        all_faces = base_faces + roof_faces_adjusted
        
        house_data = {
            'name': 'House',
            'type': 'residential',
            'vertices': all_vertices.tolist(),
            'faces': all_faces,
            'materials': {
                'walls': 'brick',
                'roof': 'wood',
                'windows': 'glass'
            },
            'metadata': {
                'width': 8,
                'depth': 8, 
                'height': 12,
                'created_with': 'Python 3D Modeler'
            }
        }
        
        return house_data
    
    def create_bridge(self):
        """Create a bridge structure with deck and pillars"""
        print("Creating bridge structure...")
        
        # Bridge deck
        deck_vertices, deck_faces = self.create_cube([0, 0, 6], 20)
        deck_vertices[:, 1] += 4  # Make it wider in y-direction
        
        # Pillars
        pillar1_vertices, pillar1_faces = self.create_cube([5, 2, 0], 2)
        pillar2_vertices, pillar2_faces = self.create_cube([15, 2, 0], 2)
        
        # Combine all vertices
        all_vertices = np.vstack([deck_vertices, pillar1_vertices, pillar2_vertices])
        
        # Adjust face indices
        pillar1_faces_adjusted = [[idx + 8 for idx in face] for face in pillar1_faces]
        pillar2_faces_adjusted = [[idx + 16 for idx in face] for face in pillar2_faces]
        
        all_faces = deck_faces + pillar1_faces_adjusted + pillar2_faces_adjusted
        
        bridge_data = {
            'name': 'Bridge Component',
            'type': 'infrastructure', 
            'vertices': all_vertices.tolist(),
            'faces': all_faces,
            'materials': {
                'deck': 'concrete',
                'pillars': 'concrete',
                'railings': 'metal'
            },
            'metadata': {
                'length': 20,
                'width': 8,
                'height': 8,
                'created_with': 'Python 3D Modeler'
            }
        }
        
        return bridge_data
    
    def create_commercial_building(self):
        """Create a commercial building"""
        print("Creating commercial building...")
        
        # Main building (taller)
        building_vertices, building_faces = self.create_cube([0, 0, 0], 12)
        
        # Make it taller
        building_vertices[4:, 2] += 8  # Increase height of top vertices
        
        commercial_data = {
            'name': 'Commercial Building',
            'type': 'commercial',
            'vertices': building_vertices.tolist(),
            'faces': building_faces,
            'materials': {
                'facade': 'concrete',
                'windows': 'glass',
                'entrance': 'metal'
            },
            'metadata': {
                'width': 12,
                'depth': 12,
                'height': 20,
                'floors': 5,
                'created_with': 'Python 3D Modeler'
            }
        }
        
        return commercial_data
    
    def plot_structure_3d(self, structure_data, filename):
        """Create a professional 3D plot of the structure"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        vertices = np.array(structure_data['vertices'])
        faces = structure_data['faces']
        materials = structure_data['materials']
        
        # Create collection of 3D polygons
        poly_collection = []
        colors = []
        
        for i, face in enumerate(faces):
            face_vertices = vertices[face]
            poly = [list(zip(face_vertices[:, 0], face_vertices[:, 1], face_vertices[:, 2]))]
            poly_collection.extend(poly)
            
            # Assign colors based on material (simplified)
            if i < 6:  # First 6 faces usually walls/base
                color = self.colors.get(materials.get('walls', 'brick'), 'red')
            elif 'roof' in materials and i >= len(faces) - 4:  # Last 4 faces might be roof
                color = self.colors.get(materials['roof'], 'brown')
            else:
                color = self.colors.get(materials.get('facade', 'concrete'), 'gray')
            
            colors.append(color)
        
        # Create 3D polygon collection
        mesh = Poly3DCollection(poly_collection, alpha=0.8, linewidth=1, edgecolor='black')
        mesh.set_facecolor(colors)
        ax.add_collection3d(mesh)
        
        # Set labels and title
        ax.set_xlabel('X Distance (m)')
        ax.set_ylabel('Y Distance (m)')
        ax.set_zlabel('Height (m)')
        ax.set_title(f"3D Model: {structure_data['name']}\n"
                    f"Materials: {', '.join(materials.values())}", 
                    fontsize=14, fontweight='bold')
        
        # Set equal aspect ratio
        max_range = np.array([
            vertices[:, 0].max() - vertices[:, 0].min(),
            vertices[:, 1].max() - vertices[:, 1].min(), 
            vertices[:, 2].max() - vertices[:, 2].min()
        ]).max()
        
        mid_x = (vertices[:, 0].max() + vertices[:, 0].min()) * 0.5
        mid_y = (vertices[:, 1].max() + vertices[:, 1].min()) * 0.5
        mid_z = (vertices[:, 2].max() + vertices[:, 2].min()) * 0.5
        
        ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
        ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
        ax.set_zlim(max(0, mid_z - max_range/2), mid_z + max_range/2)
        
        # Add grid and better viewing angle
        ax.grid(True, alpha=0.3)
        ax.view_init(elev=20, azim=45)
        
        # Add legend for materials
        from matplotlib.patches import Patch
        legend_elements = []
        for material, color in self.colors.items():
            if material in materials.values():
                legend_elements.append(Patch(facecolor=color, label=material, alpha=0.8))
        
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))
        
        # Save high-quality image
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✓ 3D render saved: {filename}")
        return filename
    
    def save_as_json(self, structure_data, filename):
        """Save structure as JSON file"""
        filepath = f"output/models/{filename}.json"
        with open(filepath, 'w') as f:
            json.dump(structure_data, f, indent=2)
        print(f"✓ Model saved: {filepath}")
        return filepath
    
    def save_as_obj(self, structure_data, filename):
        """Save structure as OBJ file (standard 3D format)"""
        filepath = f"output/models/{filename}.obj"
        vertices = np.array(structure_data['vertices'])
        
        with open(filepath, 'w') as f:
            f.write(f"# 3D Model: {structure_data['name']}\n")
            f.write(f"# Generated by Python 3D Modeler\n")
            f.write(f"# Materials: {structure_data['materials']}\n\n")
            
            # Write vertices
            for vertex in vertices:
                f.write(f"v {vertex[0]:.4f} {vertex[1]:.4f} {vertex[2]:.4f}\n")
            
            f.write("\n")
            
            # Write faces (OBJ uses 1-based indexing)
            for face in structure_data['faces']:
                face_indices = [str(idx + 1) for idx in face]
                f.write(f"f {' '.join(face_indices)}\n")
        
        print(f"✓ OBJ file saved: {filepath}")
        return filepath
    
    def generate_all_models(self):
        """Generate all three structure types"""
        print("=" * 60)
        print("3D MODELING & VISUALIZATION SYSTEM")
        print("=" * 60)
        
        models = {}
        
        try:
            # 1. Generate House
            print("\n" + "🏠" * 20)
            print("CREATING HOUSE MODEL")
            print("🏠" * 20)
            house_data = self.create_house()
            self.save_as_json(house_data, "house_design")
            self.save_as_obj(house_data, "house_design")
            self.plot_structure_3d(house_data, "output/renders/house_render.png")
            models['house'] = house_data
            
            # 2. Generate Bridge
            print("\n" + "🌉" * 20)
            print("CREATING BRIDGE MODEL")
            print("🌉" * 20)
            bridge_data = self.create_bridge()
            self.save_as_json(bridge_data, "bridge_component")
            self.save_as_obj(bridge_data, "bridge_component")
            self.plot_structure_3d(bridge_data, "output/renders/bridge_render.png")
            models['bridge'] = bridge_data
            
            # 3. Generate Commercial Building
            print("\n" + "🏢" * 20)
            print("CREATING COMMERCIAL BUILDING MODEL")
            print("🏢" * 20)
            commercial_data = self.create_commercial_building()
            self.save_as_json(commercial_data, "commercial_block")
            self.save_as_obj(commercial_data, "commercial_block")
            self.plot_structure_3d(commercial_data, "output/renders/commercial_render.png")
            models['commercial'] = commercial_data
            
            # Summary
            self.generate_summary(models)
            
        except Exception as e:
            print(f"❌ Error during model generation: {e}")
            import traceback
            traceback.print_exc()
    
    def generate_summary(self, models):
        """Generate a summary report"""
        print("\n" + "=" * 60)
        print("🎉 PROJECT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\n📁 GENERATED FILES:")
        print("├── 📂 output/")
        print("│   ├── 📂 models/")
        print("│   │   ├── 🏠 house_design.json")
        print("│   │   ├── 🏠 house_design.obj")
        print("│   │   ├── 🌉 bridge_component.json") 
        print("│   │   ├── 🌉 bridge_component.obj")
        print("│   │   ├── 🏢 commercial_block.json")
        print("│   │   └── 🏢 commercial_block.obj")
        print("│   └── 📂 renders/")
        print("│       ├── 🖼️  house_render.png")
        print("│       ├── 🖼️  bridge_render.png")
        print("│       └── 🖼️  commercial_render.png")
        
        print("\n📊 MODEL STATISTICS:")
        for name, data in models.items():
            vertices = len(data['vertices'])
            faces = len(data['faces'])
            materials = list(data['materials'].values())
            print(f"├── {data['name']}:")
            print(f"│   ├── Vertices: {vertices}")
            print(f"│   ├── Faces: {faces}")
            print(f"│   └── Materials: {', '.join(materials)}")
        
        print("\n🎯 NEXT STEPS:")
        print("1. View the rendered images in 'output/renders/'")
        print("2. Use the OBJ files in any 3D software (Blender, Maya, etc.)")
        print("3. The JSON files contain structured model data for further processing")


def check_dependencies():
    """Check if required packages are available"""
    required = ['numpy', 'matplotlib']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing required packages:")
        for package in missing:
            print(f"   - {package}")
        print("\n💡 Install them using:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True


if __name__ == "__main__":
    print("Initializing 3D Modeling System...")
    
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Create and run the modeler
        modeler = Simple3DModeler()
        modeler.generate_all_models()
        
        print("\n✅ All tasks completed! Your 3D models are ready.")
        
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)