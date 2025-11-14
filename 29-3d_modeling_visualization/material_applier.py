import numpy as np
import open3d as o3d
import pyvista as pv
from PIL import Image
import os

class MaterialApplier:
    def __init__(self):
        self.texture_cache = {}
        self.setup_default_materials()
    
    def setup_default_materials(self):
        """Create default material properties"""
        self.materials = {
            'brick': {
                'color': [0.7, 0.3, 0.1],
                'metallic': 0.1,
                'roughness': 0.8,
                'texture_scale': [2.0, 2.0]
            },
            'concrete': {
                'color': [0.8, 0.8, 0.8],
                'metallic': 0.05,
                'roughness': 0.9,
                'texture_scale': [3.0, 3.0]
            },
            'glass': {
                'color': [0.1, 0.1, 0.8, 0.3],
                'metallic': 0.0,
                'roughness': 0.1,
                'transmission': 0.9
            },
            'wood': {
                'color': [0.5, 0.35, 0.05],
                'metallic': 0.2,
                'roughness': 0.7,
                'texture_scale': [1.5, 1.5]
            },
            'metal': {
                'color': [0.8, 0.8, 0.9],
                'metallic': 0.9,
                'roughness': 0.3,
                'texture_scale': [4.0, 4.0]
            }
        }
    
    def create_texture(self, material_type, size=256):
        """Generate procedural textures for materials"""
        if material_type in self.texture_cache:
            return self.texture_cache[material_type]
        
        texture = Image.new('RGB', (size, size))
        pixels = texture.load()
        
        if material_type == 'brick':
            # Create brick pattern
            brick_color = (179, 89, 0)  # Brick red
            mortar_color = (150, 150, 150)  # Mortar gray
            brick_width = size // 8
            brick_height = size // 4
            
            for x in range(size):
                for y in range(size):
                    brick_x = (x + (y // brick_height) * brick_width // 2) % brick_width
                    brick_y = y % brick_height
                    
                    if brick_x < brick_width - 2 and brick_y < brick_height - 2:
                        pixels[x, y] = brick_color
                    else:
                        pixels[x, y] = mortar_color
        
        elif material_type == 'concrete':
            # Create concrete pattern
            base_color = (200, 200, 200)
            for x in range(size):
                for y in range(size):
                    noise = np.random.randint(-20, 20)
                    r = max(0, min(255, base_color[0] + noise))
                    g = max(0, min(255, base_color[1] + noise))
                    b = max(0, min(255, base_color[2] + noise))
                    pixels[x, y] = (r, g, b)
        
        elif material_type == 'wood':
            # Create wood grain pattern
            base_color = (140, 120, 83)
            for x in range(size):
                for y in range(size):
                    grain = int(20 * np.sin(x * 0.1) * np.cos(y * 0.05))
                    r = max(0, min(255, base_color[0] + grain))
                    g = max(0, min(255, base_color[1] + grain))
                    b = max(0, min(255, base_color[2] + grain))
                    pixels[x, y] = (r, g, b)
        
        else:
            # Default solid color
            color = tuple(int(c * 255) for c in self.materials[material_type]['color'][:3])
            for x in range(size):
                for y in range(size):
                    pixels[x, y] = color
        
        # Save texture
        os.makedirs('output/textures', exist_ok=True)
        texture_path = f'output/textures/{material_type}.png'
        texture.save(texture_path)
        self.texture_cache[material_type] = texture_path
        
        return texture_path
    
    def apply_material_to_mesh(self, mesh, material_type):
        """Apply material properties to a mesh"""
        if material_type not in self.materials:
            material_type = 'concrete'  # Default fallback
        
        material_props = self.materials[material_type]
        
        # Set base color
        if hasattr(mesh, 'paint_uniform_color'):
            mesh.paint_uniform_color(material_props['color'][:3])
        
        # For PyVista meshes
        if hasattr(mesh, 'active_t_coords'):
            texture_path = self.create_texture(material_type)
            try:
                texture = pv.read_texture(texture_path)
                mesh.textures['diffuse'] = texture
            except:
                pass
        
        return mesh, material_props