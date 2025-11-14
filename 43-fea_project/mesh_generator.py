import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

class MeshGenerator:
    def __init__(self):
        self.nodes = None
        self.elements = None
        
    def create_cantilever_beam(self, length=10.0, height=1.0, width=1.0, num_elements=20):
        """Create a simple cantilever beam mesh"""
        print("Generating beam mesh...")
        
        # Create nodes
        num_nodes_x = num_elements + 1
        num_nodes_y = 2
        num_nodes_z = 2
        
        nodes = []
        node_id = 0
        
        for i in range(num_nodes_x):
            for j in range(num_nodes_y):
                for k in range(num_nodes_z):
                    x = i * (length / num_elements)
                    y = (j - 0.5) * width
                    z = (k - 0.5) * height
                    nodes.append([x, y, z])
                    node_id += 1
        
        self.nodes = np.array(nodes)
        
        # Create hexahedral elements
        elements = []
        for i in range(num_elements):
            for j in range(num_nodes_y - 1):
                for k in range(num_nodes_z - 1):
                    n1 = i * num_nodes_y * num_nodes_z + j * num_nodes_z + k
                    n2 = n1 + 1
                    n3 = n1 + num_nodes_z
                    n4 = n3 + 1
                    n5 = n1 + num_nodes_y * num_nodes_z
                    n6 = n5 + 1
                    n7 = n5 + num_nodes_z
                    n8 = n7 + 1
                    
                    elements.append([n1, n2, n4, n3, n5, n6, n8, n7])
        
        self.elements = np.array(elements)
        print(f"Mesh generated: {len(self.nodes)} nodes, {len(self.elements)} elements")
        return self.nodes, self.elements
    
    def create_bracket_mesh(self):
        """Create a simple L-bracket mesh"""
        print("Generating bracket mesh...")
        
        # Simple L-bracket geometry
        nodes = [
            [0, 0, 0], [1, 0, 0], [2, 0, 0],
            [0, 1, 0], [1, 1, 0], [2, 1, 0],
            [0, 0, 1], [1, 0, 1], [2, 0, 1],
            [0, 1, 1], [1, 1, 1], [2, 1, 1],
            [0, 2, 0], [1, 2, 0], [2, 2, 0],
            [0, 2, 1], [1, 2, 1], [2, 2, 1]
        ]
        
        # Hexahedral elements
        elements = [
            [0, 1, 4, 3, 6, 7, 10, 9],    # Vertical leg
            [1, 2, 5, 4, 7, 8, 11, 10],   # Horizontal leg
            [3, 4, 13, 12, 9, 10, 16, 15], # Upper vertical
            [4, 5, 14, 13, 10, 11, 17, 16]  # Upper horizontal
        ]
        
        self.nodes = np.array(nodes)
        self.elements = np.array(elements)
        print(f"Bracket mesh generated: {len(self.nodes)} nodes, {len(self.elements)} elements")
        return self.nodes, self.elements
    
    def visualize_mesh(self, title="Mesh Visualization"):
        """Visualize the generated mesh using matplotlib"""
        if self.nodes is None or self.elements is None:
            print("No mesh to visualize")
            return
        
        fig = plt.figure(figsize=(15, 5))
        
        # 3D view
        ax1 = fig.add_subplot(131, projection='3d')
        for element in self.elements:
            element_nodes = self.nodes[element]
            # Plot element edges
            for i in range(len(element_nodes)):
                for j in range(i+1, len(element_nodes)):
                    ax1.plot([element_nodes[i][0], element_nodes[j][0]],
                            [element_nodes[i][1], element_nodes[j][1]],
                            [element_nodes[i][2], element_nodes[j][2]], 'b-', alpha=0.6)
        
        ax1.scatter(self.nodes[:,0], self.nodes[:,1], self.nodes[:,2], c='red', s=30)
        ax1.set_title(f'{title} - 3D View')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        
        # XY view
        ax2 = fig.add_subplot(132)
        for element in self.elements:
            element_nodes = self.nodes[element]
            for i in range(len(element_nodes)):
                for j in range(i+1, len(element_nodes)):
                    ax2.plot([element_nodes[i][0], element_nodes[j][0]],
                            [element_nodes[i][1], element_nodes[j][1]], 'b-', alpha=0.6)
        
        ax2.scatter(self.nodes[:,0], self.nodes[:,1], c='red', s=30)
        ax2.set_title(f'{title} - XY View')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.grid(True)
        
        # XZ view
        ax3 = fig.add_subplot(133)
        for element in self.elements:
            element_nodes = self.nodes[element]
            for i in range(len(element_nodes)):
                for j in range(i+1, len(element_nodes)):
                    ax3.plot([element_nodes[i][0], element_nodes[j][0]],
                            [element_nodes[i][2], element_nodes[j][2]], 'b-', alpha=0.6)
        
        ax3.scatter(self.nodes[:,0], self.nodes[:,2], c='red', s=30)
        ax3.set_title(f'{title} - XZ View')
        ax3.set_xlabel('X')
        ax3.set_ylabel('Z')
        ax3.grid(True)
        
        plt.tight_layout()
        
        # Save the plot
        os.makedirs('results/plots', exist_ok=True)
        plt.savefig(f'results/plots/{title.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Mesh visualization saved as 'results/plots/{title.lower().replace(' ', '_')}.png'")