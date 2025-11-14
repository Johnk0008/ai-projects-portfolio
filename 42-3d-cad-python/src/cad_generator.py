import numpy as np
import trimesh
from abc import ABC, abstractmethod

class CADGenerator:
    """Base CAD generator class"""
    
    def __init__(self):
        self.units = "mm"
    
    def create_cylinder(self, radius, height, sections=32):
        """Create a cylindrical mesh"""
        return trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    
    def create_box(self, width, depth, height):
        """Create a box mesh"""
        return trimesh.creation.box([width, depth, height])
    
    def create_gear_profile(self, module, teeth, pressure_angle=20):
        """Generate gear tooth profile"""
        # Simplified gear profile calculation
        pitch_diameter = module * teeth
        base_diameter = pitch_diameter * np.cos(np.radians(pressure_angle))
        
        # Generate points for gear profile
        angles = np.linspace(0, 2*np.pi, teeth*4, endpoint=False)
        radii = pitch_diameter/2 + (module/2) * np.sin(teeth * angles)
        
        points = []
        for angle, radius in zip(angles, radii):
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            points.append([x, y, 0])
        
        return np.array(points)

class MechanicalComponent(ABC):
    """Abstract base class for mechanical components"""
    
    def __init__(self, material):
        self.material = material
        self.dimensions = {}
    
    @abstractmethod
    def generate(self):
        """Generate the 3D mesh of the component"""
        pass
    
    def calculate_mass(self, volume):
        """Calculate mass based on material density"""
        densities = {
            "Steel AISI 4140": 7.85,  # g/cm³
            "Cast Iron": 7.2,
            "Aluminum 6061": 2.7,
            "Brass": 8.4
        }
        return volume * densities.get(self.material, 7.8)