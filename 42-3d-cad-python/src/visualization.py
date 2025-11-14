import pyvista as pv
import trimesh
import matplotlib.pyplot as plt
from matplotlib import cm

class CADVisualizer:
    """3D Visualization for CAD models"""
    
    def __init__(self):
        self.theme = "default"
    
    def plot_mesh(self, mesh, title="3D Model"):
        """Plot 3D mesh using PyVista"""
        # Convert trimesh to PyVista
        vertices = mesh.vertices
        faces = mesh.faces
        
        # Create PyVista mesh
        pv_mesh = pv.PolyData(vertices, faces)
        
        # Create plotter
        plotter = pv.Plotter()
        plotter.add_mesh(pv_mesh, color='lightblue', 
                        show_edges=True, opacity=0.9)
        plotter.add_title(title, font_size=18)
        plotter.show_axes()
        plotter.show()
    
    def save_render(self, filename, mesh=None, resolution=(1920, 1080)):
        """Save high-quality render"""
        if mesh is not None:
            # Convert to PyVista for rendering
            pv_mesh = pv.PolyData(mesh.vertices, mesh.faces)
            
            plotter = pv.Plotter(off_screen=True)
            plotter.add_mesh(pv_mesh, color='lightgray', 
                           metallic=0.3, roughness=0.6,
                           show_edges=True)
            plotter.set_background("white")
            plotter.show_axes()
            
            plotter.screenshot(filename)
            plotter.close()
    
    def create_technical_drawing(self, mesh, dimensions, filename):
        """Create 2D technical drawing with dimensions"""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Front view
        self._plot_2d_view(mesh, ax1, view='front', title='Front View')
        
        # Top view
        self._plot_2d_view(mesh, ax2, view='top', title='Top View')
        
        # Side view
        self._plot_2d_view(mesh, ax3, view='side', title='Side View')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_2d_view(self, mesh, ax, view='front', title=''):
        """Plot 2D view of mesh"""
        vertices = mesh.vertices
        
        if view == 'front':
            x, y = vertices[:, 0], vertices[:, 1]
        elif view == 'top':
            x, y = vertices[:, 0], vertices[:, 2]
        elif view == 'side':
            x, y = vertices[:, 1], vertices[:, 2]
        
        ax.scatter(x, y, alpha=0.6)
        ax.set_title(title)
        ax.set_aspect('equal')
        ax.grid(True)