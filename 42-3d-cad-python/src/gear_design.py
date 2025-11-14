import numpy as np
import trimesh
from .cad_generator import MechanicalComponent

class SpurGear(MechanicalComponent):
    """Spur Gear Design Implementation"""
    
    def __init__(self, module, teeth, pressure_angle=20, thickness=10, 
                 bore_diameter=10, material="Steel AISI 4140"):
        super().__init__(material)
        self.module = module
        self.teeth = teeth
        self.pressure_angle = pressure_angle
        self.thickness = thickness
        self.bore_diameter = bore_diameter
        
        # Calculate gear dimensions
        self.pitch_diameter = module * teeth
        self.addendum = module
        self.dedendum = 1.25 * module
        self.outer_diameter = self.pitch_diameter + 2 * self.addendum
        
        self.dimensions = {
            "module": module,
            "teeth": teeth,
            "pitch_diameter": self.pitch_diameter,
            "outer_diameter": self.outer_diameter,
            "thickness": thickness,
            "bore_diameter": bore_diameter
        }
    
    def generate(self):
        """Generate spur gear mesh"""
        # Create gear profile
        angles = np.linspace(0, 2*np.pi, 360)
        profile_points = []
        
        for angle in angles:
            # Simplified involute-like profile
            radius = self.outer_diameter/2 * (1 + 0.1 * np.sin(self.teeth * angle))
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            profile_points.append([x, y])
        
        # Extrude to create 3D gear
        gear_mesh = trimesh.creation.sweep_polygon(
            trimesh.path.polygons.Polygon(profile_points),
            [[0, 0, 0], [0, 0, self.thickness]]
        )
        
        # Create bore hole
        if self.bore_diameter > 0:
            bore = trimesh.creation.cylinder(
                radius=self.bore_diameter/2, 
                height=self.thickness
            )
            gear_mesh = gear_mesh.difference(bore)
        
        return gear_mesh

class BearingHousing(MechanicalComponent):
    """Bearing Housing Design"""
    
    def __init__(self, inner_diameter, outer_diameter, width, 
                 bolt_hole_diameter=6, material="Cast Iron"):
        super().__init__(material)
        self.inner_diameter = inner_diameter
        self.outer_diameter = outer_diameter
        self.width = width
        self.bolt_hole_diameter = bolt_hole_diameter
        
        self.dimensions = {
            "inner_diameter": inner_diameter,
            "outer_diameter": outer_diameter,
            "width": width,
            "bolt_hole_diameter": bolt_hole_diameter
        }
    
    def generate(self):
        """Generate bearing housing mesh"""
        # Create main housing cylinder
        housing = trimesh.creation.cylinder(
            radius=self.outer_diameter/2,
            height=self.width
        )
        
        # Create inner bore
        bore = trimesh.creation.cylinder(
            radius=self.inner_diameter/2,
            height=self.width
        )
        
        housing = housing.difference(bore)
        
        # Create bolt holes (simplified)
        bolt_positions = [
            [self.outer_diameter/2 * 0.7, 0, self.width/2],
            [-self.outer_diameter/2 * 0.7, 0, self.width/2],
            [0, self.outer_diameter/2 * 0.7, self.width/2],
            [0, -self.outer_diameter/2 * 0.7, self.width/2]
        ]
        
        for position in bolt_positions:
            bolt_hole = trimesh.creation.cylinder(
                radius=self.bolt_hole_diameter/2,
                height=self.width
            )
            bolt_hole.apply_translation(position)
            housing = housing.difference(bolt_hole)
        
        return housing