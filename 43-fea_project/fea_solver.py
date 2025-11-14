import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

class FEASolver:
    def __init__(self, E=200e9, nu=0.3):  # Steel properties
        self.E = E  # Young's modulus (Pa)
        self.nu = nu  # Poisson's ratio
        self.nodes = None
        self.elements = None
        self.displacements = None
        self.stresses = None
        self.strains = None
        
    def set_material_properties(self, E, nu):
        """Set material properties"""
        self.E = E
        self.nu = nu
    
    def set_mesh(self, nodes, elements):
        """Set the mesh data"""
        self.nodes = nodes
        self.elements = elements
    
    def compute_d_matrix(self):
        """Compute the constitutive matrix for 3D elasticity"""
        E, nu = self.E, self.nu
        lam = E * nu / ((1 + nu) * (1 - 2 * nu))
        mu = E / (2 * (1 + nu))
        
        D = np.array([
            [lam + 2*mu, lam, lam, 0, 0, 0],
            [lam, lam + 2*mu, lam, 0, 0, 0],
            [lam, lam, lam + 2*mu, 0, 0, 0],
            [0, 0, 0, mu, 0, 0],
            [0, 0, 0, 0, mu, 0],
            [0, 0, 0, 0, 0, mu]
        ])
        return D
    
    def shape_functions_hex8(self, xi, eta, zeta):
        """Shape functions for 8-node hexahedral element"""
        N = np.array([
            0.125 * (1 - xi) * (1 - eta) * (1 - zeta),
            0.125 * (1 + xi) * (1 - eta) * (1 - zeta),
            0.125 * (1 + xi) * (1 + eta) * (1 - zeta),
            0.125 * (1 - xi) * (1 + eta) * (1 - zeta),
            0.125 * (1 - xi) * (1 - eta) * (1 + zeta),
            0.125 * (1 + xi) * (1 - eta) * (1 + zeta),
            0.125 * (1 + xi) * (1 + eta) * (1 + zeta),
            0.125 * (1 - xi) * (1 + eta) * (1 + zeta)
        ])
        return N
    
    def jacobian_hex8(self, nodes, xi, eta, zeta):
        """Compute Jacobian matrix for hexahedral element"""
        dN_dxi = np.array([
            [-0.125*(1-eta)*(1-zeta), 0.125*(1-eta)*(1-zeta), 0.125*(1+eta)*(1-zeta), -0.125*(1+eta)*(1-zeta),
             -0.125*(1-eta)*(1+zeta), 0.125*(1-eta)*(1+zeta), 0.125*(1+eta)*(1+zeta), -0.125*(1+eta)*(1+zeta)],
            [-0.125*(1-xi)*(1-zeta), -0.125*(1+xi)*(1-zeta), 0.125*(1+xi)*(1-zeta), 0.125*(1-xi)*(1-zeta),
             -0.125*(1-xi)*(1+zeta), -0.125*(1+xi)*(1+zeta), 0.125*(1+xi)*(1+zeta), 0.125*(1-xi)*(1+zeta)],
            [-0.125*(1-xi)*(1-eta), -0.125*(1+xi)*(1-eta), -0.125*(1+xi)*(1+eta), -0.125*(1-xi)*(1+eta),
             0.125*(1-xi)*(1-eta), 0.125*(1+xi)*(1-eta), 0.125*(1+xi)*(1+eta), 0.125*(1-xi)*(1+eta)]
        ])
        
        J = dN_dxi @ nodes
        return J, dN_dxi
    
    def compute_B_matrix(self, nodes, xi, eta, zeta):
        """Compute strain-displacement matrix"""
        J, dN_dxi = self.jacobian_hex8(nodes, xi, eta, zeta)
        invJ = np.linalg.inv(J)
        
        dN_dx = invJ @ dN_dxi
        
        B = np.zeros((6, 24))
        for i in range(8):
            B[0, i*3] = dN_dx[0, i]     # ε_xx
            B[1, i*3+1] = dN_dx[1, i]   # ε_yy
            B[2, i*3+2] = dN_dx[2, i]   # ε_zz
            B[3, i*3] = dN_dx[1, i]     # γ_xy
            B[3, i*3+1] = dN_dx[0, i]
            B[4, i*3+1] = dN_dx[2, i]   # γ_yz
            B[4, i*3+2] = dN_dx[1, i]
            B[5, i*3] = dN_dx[2, i]     # γ_zx
            B[5, i*3+2] = dN_dx[0, i]
        
        return B, J
    
    def element_stiffness_matrix(self, element_nodes):
        """Compute element stiffness matrix"""
        D = self.compute_d_matrix()
        K_e = np.zeros((24, 24))
        
        # Gaussian quadrature points (2x2x2)
        gauss_points = [-0.57735, 0.57735]
        weights = [1.0, 1.0]
        
        for i, xi in enumerate(gauss_points):
            for j, eta in enumerate(gauss_points):
                for k, zeta in enumerate(gauss_points):
                    B, J = self.compute_B_matrix(element_nodes, xi, eta, zeta)
                    detJ = np.linalg.det(J)
                    K_e += B.T @ D @ B * weights[i] * weights[j] * weights[k] * detJ
        
        return K_e
    
    def apply_boundary_conditions(self, K_global, f_global, bc_type='cantilever'):
        """Apply boundary conditions"""
        if bc_type == 'cantilever':
            # Fixed at x=0 (cantilever)
            fixed_nodes = [i for i, node in enumerate(self.nodes) if abs(node[0]) < 1e-6]
        elif bc_type == 'simply_supported':
            # Simply supported - fixed in z-direction at ends
            fixed_nodes = [i for i, node in enumerate(self.nodes) 
                          if (abs(node[0]) < 1e-6 or abs(node[0] - max(self.nodes[:,0])) < 1e-6)]
        
        # Apply fixed boundary conditions (all DOFs)
        dofs_to_fix = []
        for node in fixed_nodes:
            dofs_to_fix.extend([node*3, node*3+1, node*3+2])
        
        # Modify stiffness matrix and force vector
        for dof in dofs_to_fix:
            K_global[dof, :] = 0
            K_global[:, dof] = 0
            K_global[dof, dof] = 1
            f_global[dof] = 0
        
        return K_global, f_global, dofs_to_fix
    
    def apply_loads(self, f_global, load_type='point', magnitude=1000):
        """Apply loads to the structure"""
        if load_type == 'point':
            # Point load at free end
            free_end_nodes = [i for i, node in enumerate(self.nodes) 
                            if abs(node[0] - max(self.nodes[:,0])) < 1e-6]
            
            # Apply downward force in z-direction
            for node in free_end_nodes:
                f_global[node*3 + 2] = -magnitude / len(free_end_nodes)
                
        elif load_type == 'distributed':
            # Distributed load on top surface
            top_nodes = [i for i, node in enumerate(self.nodes) 
                        if abs(node[2] - max(self.nodes[:,2])) < 1e-6]
            
            for node in top_nodes:
                f_global[node*3 + 2] = -magnitude / len(top_nodes)
        
        return f_global
    
    def solve(self, bc_type='cantilever', load_type='point', load_magnitude=1000):
        """Solve the FEA problem"""
        print("Assembling global stiffness matrix...")
        
        n_nodes = len(self.nodes)
        n_dofs = n_nodes * 3
        
        # Initialize global stiffness matrix and force vector
        K_global = lil_matrix((n_dofs, n_dofs))
        f_global = np.zeros(n_dofs)
        
        # Assemble global stiffness matrix
        for element in self.elements:
            element_nodes = self.nodes[element]
            K_e = self.element_stiffness_matrix(element_nodes)
            
            for i, node_i in enumerate(element):
                for j, node_j in enumerate(element):
                    for dof_i in range(3):
                        for dof_j in range(3):
                            row = node_i * 3 + dof_i
                            col = node_j * 3 + dof_j
                            K_global[row, col] += K_e[i*3 + dof_i, j*3 + dof_j]
        
        # Convert to CSR format for efficient solving
        K_global = csr_matrix(K_global)
        
        print("Applying boundary conditions and loads...")
        # Apply boundary conditions and loads
        f_global = self.apply_loads(f_global, load_type, load_magnitude)
        K_global, f_global, fixed_dofs = self.apply_boundary_conditions(K_global, f_global, bc_type)
        
        print("Solving system of equations...")
        # Solve for displacements
        self.displacements = spsolve(K_global, f_global)
        
        print("Computing stresses and strains...")
        self.compute_stresses_strains()
        
        return self.displacements
    
    def compute_stresses_strains(self):
        """Compute element stresses and strains"""
        D = self.compute_d_matrix()
        self.stresses = []
        self.strains = []
        
        gauss_points = [-0.57735, 0.57735]
        
        for element in self.elements:
            element_nodes = self.nodes[element]
            element_displacements = np.concatenate([self.displacements[node*3:node*3+3] for node in element])
            
            element_stress = np.zeros(6)
            element_strain = np.zeros(6)
            count = 0
            
            for xi in gauss_points:
                for eta in gauss_points:
                    for zeta in gauss_points:
                        B, J = self.compute_B_matrix(element_nodes, xi, eta, zeta)
                        strain = B @ element_displacements
                        stress = D @ strain
                        
                        element_strain += strain
                        element_stress += stress
                        count += 1
            
            self.strains.append(element_strain / count)
            self.stresses.append(element_stress / count)
        
        self.strains = np.array(self.strains)
        self.stresses = np.array(self.stresses)
    
    def get_von_mises_stress(self):
        """Compute von Mises stress"""
        if self.stresses is None:
            return None
            
        von_mises = np.sqrt(0.5 * (
            (self.stresses[:,0] - self.stresses[:,1])**2 +
            (self.stresses[:,1] - self.stresses[:,2])**2 +
            (self.stresses[:,2] - self.stresses[:,0])**2 +
            6 * (self.stresses[:,3]**2 + self.stresses[:,4]**2 + self.stresses[:,5]**2)
        ))
        return von_mises
    
    def get_max_displacement(self):
        """Get maximum displacement magnitude"""
        if self.displacements is None:
            return 0
        displacement_magnitudes = np.sqrt(
            self.displacements[0::3]**2 + 
            self.displacements[1::3]**2 + 
            self.displacements[2::3]**2
        )
        return np.max(displacement_magnitudes)