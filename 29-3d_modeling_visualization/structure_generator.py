import numpy as np
import open3d as o3d
import pyvista as pv
from typing import List, Tuple, Dict
import json

class StructureGenerator:
    def __init__(self):
        self.materials = {
            'brick': {'color': [0.7, 0.3, 0.1], 'roughness': 0.8},
            'concrete': {'color': [0.8, 0.8, 0.8], 'roughness': 0.9},
            'glass': {'color': [0.1, 0.1, 0.8, 0.3], 'roughness': 0.1},
            'wood': {'color': [0.5, 0.35, 0.05], 'roughness': 0.7},
            'metal': {'color': [0.8, 0.8, 0.9], 'roughness': 0.3}
        }
    
    def create_house(self, position=(0, 0, 0), size=10):
        """Generate a 3D house model"""
        vertices = []
        faces = []
        
        # Base dimensions
        width, depth, height = size, size, size * 0.7
        roof_height = size * 0.3
        
        # House base vertices
        base_vertices = [
            [position[0], position[1], position[2]],
            [position[0] + width, position[1], position[2]],
            [position[0] + width, position[1] + depth, position[2]],
            [position[0], position[1] + depth, position[2]],
            [position[0], position[1], position[2] + height],
            [position[0] + width, position[1], position[2] + height],
            [position[0] + width, position[1] + depth, position[2] + height],
            [position[0], position[1] + depth, position[2] + height]
        ]
        
        # Roof vertices (triangular)
        roof_vertices = [
            [position[0] - roof_height/2, position[1] - roof_height/2, position[2] + height],
            [position[0] + width + roof_height/2, position[1] - roof_height/2, position[2] + height],
            [position[0] + width + roof_height/2, position[1] + depth + roof_height/2, position[2] + height],
            [position[0] - roof_height/2, position[1] + depth + roof_height/2, position[2] + height],
            [position[0] + width/2, position[1] + depth/2, position[2] + height + roof_height]
        ]
        
        vertices = base_vertices + roof_vertices
        
        # Faces (cube + roof)
        faces = [
            [0, 1, 2, 3],  # bottom
            [4, 7, 6, 5],  # top
            [0, 4, 5, 1],  # front
            [1, 5, 6, 2],  # right
            [2, 6, 7, 3],  # back
            [3, 7, 4, 0],  # left
            # Roof faces
            [8, 9, 12],    # front roof
            [9, 10, 12],   # right roof
            [10, 11, 12],  # back roof
            [11, 8, 12]    # left roof
        ]
        
        house_data = {
            'vertices': vertices,
            'faces': faces,
            'materials': {
                'walls': 'brick',
                'roof': 'wood',
                'windows': 'glass'
            }
        }
        
        return house_data
    
    def create_bridge_component(self, position=(0, 0, 0), length=20):
        """Generate a bridge component"""
        vertices = []
        faces = []
        
        # Bridge deck
        deck_width = 8
        deck_height = 1
        
        # Support pillars
        pillar_width = 2
        pillar_height = 10
        
        # Create deck
        deck_vertices = [
            [position[0], position[1], position[2] + pillar_height],
            [position[0] + length, position[1], position[2] + pillar_height],
            [position[0] + length, position[1] + deck_width, position[2] + pillar_height],
            [position[0], position[1] + deck_width, position[2] + pillar_height],
            [position[0], position[1], position[2] + pillar_height + deck_height],
            [position[0] + length, position[1], position[2] + pillar_height + deck_height],
            [position[0] + length, position[1] + deck_width, position[2] + pillar_height + deck_height],
            [position[0], position[1] + deck_width, position[2] + pillar_height + deck_height]
        ]
        
        # Create pillars
        pillar_positions = [
            [position[0] + length/4, position[1] + deck_width/2 - pillar_width/2, position[2]],
            [position[0] + 3*length/4, position[1] + deck_width/2 - pillar_width/2, position[2]]
        ]
        
        vertices = deck_vertices
        faces = [
            [0, 1, 2, 3],  # bottom
            [4, 7, 6, 5],  # top
            [0, 4, 5, 1],  # front
            [1, 5, 6, 2],  # right
            [2, 6, 7, 3],  # back
            [3, 7, 4, 0]   # left
        ]
        
        # Add pillars to vertices and faces
        pillar_start_idx = len(vertices)
        for i, (px, py, pz) in enumerate(pillar_positions):
            pillar_verts = [
                [px, py, pz],
                [px + pillar_width, py, pz],
                [px + pillar_width, py + pillar_width, pz],
                [px, py + pillar_width, pz],
                [px, py, pz + pillar_height],
                [px + pillar_width, py, pz + pillar_height],
                [px + pillar_width, py + pillar_width, pz + pillar_height],
                [px, py + pillar_width, pz + pillar_height]
            ]
            vertices.extend(pillar_verts)
            
            pillar_face_offset = pillar_start_idx + i * 8
            faces.extend([
                [pillar_face_offset + 0, pillar_face_offset + 1, pillar_face_offset + 2, pillar_face_offset + 3],
                [pillar_face_offset + 4, pillar_face_offset + 7, pillar_face_offset + 6, pillar_face_offset + 5],
                [pillar_face_offset + 0, pillar_face_offset + 4, pillar_face_offset + 5, pillar_face_offset + 1],
                [pillar_face_offset + 1, pillar_face_offset + 5, pillar_face_offset + 6, pillar_face_offset + 2],
                [pillar_face_offset + 2, pillar_face_offset + 6, pillar_face_offset + 7, pillar_face_offset + 3],
                [pillar_face_offset + 3, pillar_face_offset + 7, pillar_face_offset + 4, pillar_face_offset + 0]
            ])
        
        bridge_data = {
            'vertices': vertices,
            'faces': faces,
            'materials': {
                'deck': 'concrete',
                'pillars': 'concrete',
                'railings': 'metal'
            }
        }
        
        return bridge_data
    
    def create_commercial_block(self, position=(0, 0, 0), size=15):
        """Generate a commercial building block"""
        vertices = []
        faces = []
        
        # Main building dimensions
        width, depth, height = size, size, size * 2
        floor_height = height / 5  # 5 floors
        
        # Create main building
        main_vertices = [
            [position[0], position[1], position[2]],
            [position[0] + width, position[1], position[2]],
            [position[0] + width, position[1] + depth, position[2]],
            [position[0], position[1] + depth, position[2]],
            [position[0], position[1], position[2] + height],
            [position[0] + width, position[1], position[2] + height],
            [position[0] + width, position[1] + depth, position[2] + height],
            [position[0], position[1] + depth, position[2] + height]
        ]
        
        vertices = main_vertices
        faces = [
            [0, 1, 2, 3],  # bottom
            [4, 7, 6, 5],  # top
            [0, 4, 5, 1],  # front
            [1, 5, 6, 2],  # right
            [2, 6, 7, 3],  # back
            [3, 7, 4, 0]   # left
        ]
        
        # Add window details (simplified)
        window_width = width / 8
        window_height = floor_height * 0.6
        
        commercial_data = {
            'vertices': vertices,
            'faces': faces,
            'materials': {
                'facade': 'concrete',
                'windows': 'glass',
                'entrance': 'metal'
            }
        }
        
        return commercial_data
    
    def save_structure(self, structure_data, filename):
        """Save structure to JSON file"""
        with open(f'output/models/{filename}.json', 'w') as f:
            json.dump(structure_data, f, indent=2)
        
        # Also save as OBJ format for compatibility
        self._save_as_obj(structure_data, f'output/models/{filename}.obj')
    
    def _save_as_obj(self, structure_data, filename):
        """Save structure as OBJ file"""
        with open(filename, 'w') as f:
            f.write("# 3D Structure Model\n")
            f.write("# Generated by AI/ML 3D Modeling System\n\n")
            
            # Write vertices
            for vertex in structure_data['vertices']:
                f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
            
            # Write faces (OBJ uses 1-based indexing)
            for face in structure_data['faces']:
                face_indices = [str(idx + 1) for idx in face]
                f.write(f"f {' '.join(face_indices)}\n")