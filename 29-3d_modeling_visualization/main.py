import os
import json
import shutil
from structure_generator import StructureGenerator
from material_applier import MaterialApplier
from render_engine import RenderEngine

class ModelingVisualizationApp:
    def __init__(self):
        self.structure_gen = StructureGenerator()
        self.material_applier = MaterialApplier()
        self.render_engine = RenderEngine()
        self.setup_directories()
    
    def setup_directories(self):
        """Create necessary directories with error handling"""
        directories = ['output/models', 'output/renders', 'output/textures']
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"Directory created/verified: {directory}")
            except OSError as e:
                print(f"Warning: Could not create directory {directory}: {e}")
    
    def create_house_design(self):
        """Generate and render a house design"""
        print("Generating house design...")
        
        try:
            # Generate house structure
            house_data = self.structure_gen.create_house()
            self.structure_gen.save_structure(house_data, 'house_design')
            
            # Render the house
            render_paths = self.render_engine.render_with_plotly(
                house_data, 
                house_data['materials'],
                'output/renders/house.png'
            )
            
            print(f"✓ House design saved: output/models/house_design.json")
            print(f"✓ Renders saved: {render_paths}")
            
            return house_data, render_paths
        except Exception as e:
            print(f"Error creating house design: {e}")
            return None, None
    
    def create_bridge_design(self):
        """Generate and render a bridge component"""
        print("Generating bridge component design...")
        
        try:
            # Generate bridge structure
            bridge_data = self.structure_gen.create_bridge_component()
            self.structure_gen.save_structure(bridge_data, 'bridge_component')
            
            # Render the bridge
            render_paths = self.render_engine.render_with_plotly(
                bridge_data, 
                bridge_data['materials'],
                'output/renders/bridge.png'
            )
            
            print(f"✓ Bridge design saved: output/models/bridge_component.json")
            print(f"✓ Renders saved: {render_paths}")
            
            return bridge_data, render_paths
        except Exception as e:
            print(f"Error creating bridge design: {e}")
            return None, None
    
    def create_commercial_design(self):
        """Generate and render a commercial block"""
        print("Generating commercial block design...")
        
        try:
            # Generate commercial structure
            commercial_data = self.structure_gen.create_commercial_block()
            self.structure_gen.save_structure(commercial_data, 'commercial_block')
            
            # Render the commercial block
            render_paths = self.render_engine.render_with_plotly(
                commercial_data, 
                commercial_data['materials'],
                'output/renders/commercial.png'
            )
            
            print(f"✓ Commercial design saved: output/models/commercial_block.json")
            print(f"✓ Renders saved: {render_paths}")
            
            return commercial_data, render_paths
        except Exception as e:
            print(f"Error creating commercial design: {e}")
            return None, None
    
    def run_all_designs(self):
        """Generate all three structure types"""
        print("=== 3D Modeling & Visualization System ===")
        print("Generating all structure designs...\n")
        
        results = {}
        
        # Generate all designs
        results['house'] = self.create_house_design()
        print("\n" + "="*50 + "\n")
        
        results['bridge'] = self.create_bridge_design()
        print("\n" + "="*50 + "\n")
        
        results['commercial'] = self.create_commercial_design()
        print("\n" + "="*50 + "\n")
        
        print("All designs completed successfully!")
        print("\nGenerated Files:")
        print("- Structure models: output/models/")
        print("- Rendered images: output/renders/")
        print("- Textures: output/textures/")
        
        return results

if __name__ == "__main__":
    app = ModelingVisualizationApp()
    app.run_all_designs()