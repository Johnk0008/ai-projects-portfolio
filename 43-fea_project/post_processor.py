import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

class PostProcessor:
    def __init__(self, solver):
        self.solver = solver
        self.results_dir = "results/plots"
        os.makedirs(self.results_dir, exist_ok=True)
    
    def plot_deformation(self, scale_factor=50.0):
        """Plot deformed structure using matplotlib"""
        if self.solver.displacements is None:
            print("No displacement data available")
            return
        
        fig = plt.figure(figsize=(15, 5))
        
        # Original mesh
        ax1 = fig.add_subplot(131, projection='3d')
        self._plot_mesh_3d(ax1, self.solver.nodes, self.solver.elements, 'blue')
        ax1.set_title('Original Mesh')
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        
        # Deformed mesh
        ax2 = fig.add_subplot(132, projection='3d')
        deformed_nodes = self.solver.nodes + self.solver.displacements.reshape(-1, 3) * scale_factor
        self._plot_mesh_3d(ax2, deformed_nodes, self.solver.elements, 'red')
        ax2.set_title(f'Deformed Mesh (Scale: {scale_factor}x)')
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        
        # Both overlayed
        ax3 = fig.add_subplot(133, projection='3d')
        self._plot_mesh_3d(ax3, self.solver.nodes, self.solver.elements, 'blue', alpha=0.3)
        self._plot_mesh_3d(ax3, deformed_nodes, self.solver.elements, 'red', alpha=0.7)
        ax3.set_title('Original vs Deformed')
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Y (m)')
        ax3.set_zlabel('Z (m)')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/deformation.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_mesh_3d(self, ax, nodes, elements, color, alpha=1.0):
        """Helper function to plot 3D mesh"""
        # Plot nodes
        ax.scatter(nodes[:,0], nodes[:,1], nodes[:,2], c=color, alpha=alpha, s=20)
        
        # Plot element edges
        for element in elements:
            element_nodes = nodes[element]
            # Create edges for hexahedral element
            edges = [
                [0,1], [1,2], [2,3], [3,0],  # bottom face
                [4,5], [5,6], [6,7], [7,4],  # top face
                [0,4], [1,5], [2,6], [3,7]   # vertical edges
            ]
            for edge in edges:
                ax.plot([element_nodes[edge[0]][0], element_nodes[edge[1]][0]],
                       [element_nodes[edge[0]][1], element_nodes[edge[1]][1]],
                       [element_nodes[edge[0]][2], element_nodes[edge[1]][2]], 
                       color=color, alpha=alpha*0.7)
    
    def plot_stress_distribution(self):
        """Plot stress distribution using matplotlib"""
        von_mises = self.solver.get_von_mises_stress()
        if von_mises is None:
            print("No stress data available")
            return
        
        fig = plt.figure(figsize=(15, 5))
        
        # Von Mises stress
        ax1 = fig.add_subplot(131)
        # Map element stresses to nodes for better visualization
        node_stress = np.zeros(len(self.solver.nodes))
        node_count = np.zeros(len(self.solver.nodes))
        
        for i, element in enumerate(self.solver.elements):
            for node in element:
                node_stress[node] += von_mises[i]
                node_count[node] += 1
        
        node_stress /= np.maximum(node_count, 1)
        
        sc1 = ax1.scatter(self.solver.nodes[:,0], self.solver.nodes[:,2], 
                         c=node_stress, cmap='jet', s=50)
        ax1.set_title('Von Mises Stress Distribution (Pa)')
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Z (m)')
        plt.colorbar(sc1, ax=ax1)
        
        # Displacement magnitude
        displacement_magnitudes = np.sqrt(
            self.solver.displacements[0::3]**2 + 
            self.solver.displacements[1::3]**2 + 
            self.solver.displacements[2::3]**2
        )
        
        ax2 = fig.add_subplot(132)
        sc2 = ax2.scatter(self.solver.nodes[:,0], self.solver.nodes[:,2], 
                         c=displacement_magnitudes, cmap='coolwarm', s=50)
        ax2.set_title('Displacement Magnitude (m)')
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Z (m)')
        plt.colorbar(sc2, ax=ax2)
        
        # Principal stresses
        max_principal = np.max(np.abs(self.solver.stresses[:,:3]), axis=1)
        
        # Map to nodes
        node_principal = np.zeros(len(self.solver.nodes))
        node_count = np.zeros(len(self.solver.nodes))
        
        for i, element in enumerate(self.solver.elements):
            for node in element:
                node_principal[node] += max_principal[i]
                node_count[node] += 1
        
        node_principal /= np.maximum(node_count, 1)
        
        ax3 = fig.add_subplot(133)
        sc3 = ax3.scatter(self.solver.nodes[:,0], self.solver.nodes[:,2], 
                         c=node_principal, cmap='hot', s=50)
        ax3.set_title('Max Principal Stress (Pa)')
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Z (m)')
        plt.colorbar(sc3, ax=ax3)
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/stress_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_3d_visualization(self):
        """Create 3D visualization using matplotlib only"""
        print("Creating 3D visualization with matplotlib...")
        
        von_mises = self.solver.get_von_mises_stress()
        if von_mises is None:
            return
        
        # Map element stresses to nodes
        node_stress = np.zeros(len(self.solver.nodes))
        node_count = np.zeros(len(self.solver.nodes))
        
        for i, element in enumerate(self.solver.elements):
            for node in element:
                node_stress[node] += von_mises[i]
                node_count[node] += 1
        
        node_stress /= np.maximum(node_count, 1)
        
        fig = plt.figure(figsize=(15, 10))
        
        # Original mesh with stress
        ax1 = fig.add_subplot(221, projection='3d')
        sc1 = ax1.scatter(self.solver.nodes[:,0], self.solver.nodes[:,1], self.solver.nodes[:,2], 
                         c=node_stress, cmap='jet', s=30)
        self._plot_mesh_3d(ax1, self.solver.nodes, self.solver.elements, 'black', alpha=0.1)
        ax1.set_title('Von Mises Stress Distribution')
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        plt.colorbar(sc1, ax=ax1, shrink=0.6, label='Stress (Pa)')
        
        # Deformed mesh with stress
        ax2 = fig.add_subplot(222, projection='3d')
        scale_factor = 50
        deformed_nodes = self.solver.nodes + self.solver.displacements.reshape(-1, 3) * scale_factor
        sc2 = ax2.scatter(deformed_nodes[:,0], deformed_nodes[:,1], deformed_nodes[:,2], 
                         c=node_stress, cmap='jet', s=30)
        self._plot_mesh_3d(ax2, deformed_nodes, self.solver.elements, 'red', alpha=0.1)
        ax2.set_title(f'Deformed Shape with Stress ({scale_factor}x scale)')
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        plt.colorbar(sc2, ax=ax2, shrink=0.6, label='Stress (Pa)')
        
        # Displacement magnitude
        ax3 = fig.add_subplot(223, projection='3d')
        displacement_magnitudes = np.sqrt(
            np.sum(self.solver.displacements.reshape(-1, 3)**2, axis=1)
        )
        sc3 = ax3.scatter(self.solver.nodes[:,0], self.solver.nodes[:,1], self.solver.nodes[:,2], 
                         c=displacement_magnitudes, cmap='coolwarm', s=30)
        self._plot_mesh_3d(ax3, self.solver.nodes, self.solver.elements, 'blue', alpha=0.1)
        ax3.set_title('Displacement Magnitude')
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Y (m)')
        ax3.set_zlabel('Z (m)')
        plt.colorbar(sc3, ax=ax3, shrink=0.6, label='Displacement (m)')
        
        # Combined view
        ax4 = fig.add_subplot(224, projection='3d')
        # Plot original in light gray
        self._plot_mesh_3d(ax4, self.solver.nodes, self.solver.elements, 'lightgray', alpha=0.3)
        # Plot deformed with stress coloring
        sc4 = ax4.scatter(deformed_nodes[:,0], deformed_nodes[:,1], deformed_nodes[:,2], 
                         c=node_stress, cmap='jet', s=40, alpha=0.8)
        ax4.set_title('Original vs Deformed with Stress')
        ax4.set_xlabel('X (m)')
        ax4.set_ylabel('Y (m)')
        ax4.set_zlabel('Z (m)')
        plt.colorbar(sc4, ax=ax4, shrink=0.6, label='Stress (Pa)')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/3d_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_summary_report(self):
        """Generate summary of analysis results"""
        von_mises = self.solver.get_von_mises_stress()
        max_disp = self.solver.get_max_displacement()
        
        if von_mises is None:
            return
        
        print("\n" + "="*50)
        print("FEA ANALYSIS SUMMARY")
        print("="*50)
        print(f"Number of nodes: {len(self.solver.nodes)}")
        print(f"Number of elements: {len(self.solver.elements)}")
        print(f"Maximum displacement: {max_disp:.6f} m")
        print(f"Maximum von Mises stress: {np.max(von_mises):.2f} Pa")
        print(f"Minimum von Mises stress: {np.min(von_mises):.2f} Pa")
        print(f"Average von Mises stress: {np.mean(von_mises):.2f} Pa")
        
        # Factor of safety (assuming yield strength of steel = 250 MPa)
        yield_strength = 250e6
        max_stress = np.max(von_mises)
        if max_stress > 0:
            fos = yield_strength / max_stress
            print(f"Factor of Safety: {fos:.2f}")
            
            if fos < 1:
                print("WARNING: Factor of Safety < 1 - Structure may fail!")
            elif fos < 2:
                print("WARNING: Factor of Safety < 2 - Consider redesign!")
            else:
                print("Structure is safe.")
        
        print("="*50)