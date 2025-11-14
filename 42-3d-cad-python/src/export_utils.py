import trimesh
import json
import os

class ExportManager:
    """Handle export to various CAD formats"""
    
    def __init__(self):
        self.supported_formats = ['stl', 'step', 'obj', 'iges']
    
    def export_stl(self, mesh, filename):
        """Export mesh to STL format"""
        mesh.export(filename)
        print(f"Exported STL: {filename}")
    
    def export_step(self, mesh, filename):
        """Export mesh to STEP format"""
        # Note: trimesh has limited STEP support
        # In production, use dedicated CAD libraries
        try:
            mesh.export(filename)
            print(f"Exported STEP: {filename}")
        except Exception as e:
            print(f"STEP export failed: {e}")
            print("Consider using CADQuery for better STEP support")
    
    def export_obj(self, mesh, filename):
        """Export mesh to OBJ format"""
        mesh.export(filename)
        print(f"Exported OBJ: {filename}")
    
    def generate_bom(self, components, filename):
        """Generate Bill of Materials"""
        bom = {
            "project": "Mechanical Assembly",
            "components": [],
            "total_components": len(components)
        }
        
        for comp in components:
            bom["components"].append({
                "name": comp.__class__.__name__,
                "material": comp.material,
                "dimensions": comp.dimensions,
                "volume": comp.generate().volume,
                "mass": comp.calculate_mass(comp.generate().volume)
            })
        
        with open(filename, 'w') as f:
            json.dump(bom, f, indent=2)
        
        print(f"Generated BOM: {filename}")