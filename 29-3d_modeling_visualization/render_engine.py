import pyvista as pv
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
from PIL import Image

class RenderEngine:
    def __init__(self):
        self.setup_render_settings()
    
    def setup_render_settings(self):
        """Initialize rendering settings"""
        self.light_settings = {
            'position': [5, 5, 10],
            'intensity': 1.0,
            'color': 'white'
        }
        
        self.camera_settings = {
            'position': [15, -15, 10],
            'focal_point': [0, 0, 5],
            'view_up': [0, 0, 1]
        }
    
    def render_with_pyvista(self, structure_data, materials_config, output_path):
        """Render using PyVista for high-quality visualization"""
        plotter = pv.Plotter(off_screen=True, window_size=[1920, 1080])
        
        # Create mesh from structure data
        vertices = np.array(structure_data['vertices'])
        faces = []
        
        for face in structure_data['faces']:
            faces.append(len(face))
            faces.extend(face)
        
        faces = np.array(faces, dtype=np.int64)
        
        mesh = pv.PolyData(vertices, faces)
        
        # Apply materials
        material_applier = MaterialApplier()
        mesh, material_props = material_applier.apply_material_to_mesh(mesh, list(materials_config.values())[0])
        
        # Add mesh to plotter
        plotter.add_mesh(mesh, 
                        color=material_props['color'][:3],
                        smooth_shading=True,
                        metallic=material_props.get('metallic', 0.1),
                        roughness=material_props.get('roughness', 0.5))
        
        # Set lighting and camera
        plotter.set_background('lightblue')
        plotter.add_light(pv.Light(position=self.light_settings['position']))
        plotter.camera_position = [
            self.camera_settings['position'],
            self.camera_settings['focal_point'],
            self.camera_settings['view_up']
        ]
        
        # Render and save
        plotter.show(screenshot=output_path)
        plotter.close()
        
        return output_path
    
    def render_with_plotly(self, structure_data, materials_config, output_path):
        """Render interactive 3D visualization using Plotly"""
        vertices = np.array(structure_data['vertices'])
        faces = structure_data['faces']
        
        # Create mesh3d trace
        x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
        
        # Prepare face indices for Plotly
        i, j, k = [], [], []
        for face in faces:
            if len(face) == 3:  # Triangle
                i.append(face[0])
                j.append(face[1])
                k.append(face[2])
            elif len(face) == 4:  # Quad - triangulate
                i.extend([face[0], face[0]])
                j.extend([face[1], face[2]])
                k.extend([face[2], face[3]])
        
        # Get material color
        material_type = list(materials_config.values())[0]
        material_applier = MaterialApplier()
        color = material_applier.materials[material_type]['color']
        
        fig = go.Figure(data=[
            go.Mesh3d(
                x=x, y=y, z=z,
                i=i, j=j, k=k,
                color=f'rgb({int(color[0]*255)},{int(color[1]*255)},{int(color[2]*255)})',
                opacity=color[3] if len(color) > 3 else 1.0,
                lighting=dict(
                    ambient=0.3,
                    diffuse=0.8,
                    specular=0.1
                ),
                flatshading=False
            )
        ])
        
        fig.update_layout(
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                aspectmode='data',
                camera=dict(
                    eye=dict(x=2, y=2, z=2)
                )
            ),
            title="3D Structure Visualization",
            width=1200,
            height=800
        )
        
        # Save as HTML and PNG
        fig.write_html(output_path.replace('.png', '.html'))
        fig.write_image(output_path)
        
        return output_path
    
    def create_multiview_render(self, structure_data, materials_config, output_base):
        """Create multiple views of the structure"""
        views = [
            {'name': 'perspective', 'position': [15, -15, 10], 'focal_point': [0, 0, 5]},
            {'name': 'top', 'position': [0, 0, 20], 'focal_point': [0, 0, 0]},
            {'name': 'front', 'position': [0, -20, 5], 'focal_point': [0, 0, 5]},
            {'name': 'side', 'position': [20, 0, 5], 'focal_point': [0, 0, 5]}
        ]
        
        rendered_paths = []
        
        for view in views:
            self.camera_settings.update(view)
            output_path = f"{output_base}_{view['name']}.png"
            path = self.render_with_pyvista(structure_data, materials_config, output_path)
            rendered_paths.append(path)
        
        # Create composite image
        self.create_composite_image(rendered_paths, f"{output_base}_composite.png")
        
        return rendered_paths
    
    def create_composite_image(self, image_paths, output_path):
        """Create a composite image from multiple views"""
        images = [Image.open(path) for path in image_paths]
        
        # Resize images to same size
        min_width = min(img.width for img in images)
        min_height = min(img.height for img in images)
        images = [img.resize((min_width, min_height)) for img in images]
        
        # Create 2x2 grid
        composite = Image.new('RGB', (min_width * 2, min_height * 2))
        
        for i, img in enumerate(images):
            x = (i % 2) * min_width
            y = (i // 2) * min_height
            composite.paste(img, (x, y))
        
        composite.save(output_path)
        return output_path