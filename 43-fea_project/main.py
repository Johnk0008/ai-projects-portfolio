import numpy as np
import matplotlib.pyplot as plt
from mesh_generator import MeshGenerator
from fea_solver import FEASolver
from post_processor import PostProcessor
from report_generator import ReportGenerator

def main():
    print("Finite Element Analysis for Structural Simulation")
    print("=" * 60)
    
    # Initialize components
    mesh_gen = MeshGenerator()
    solver = FEASolver()
    post_processor = None
    report_gen = None
    
    while True:
        print("\nMAIN MENU:")
        print("1. Generate Cantilever Beam Mesh")
        print("2. Generate Bracket Mesh")
        print("3. Run FEA Analysis")
        print("4. Visualize Results")
        print("5. Generate Comprehensive Report")
        print("6. Run Complete Demo")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\nGenerating Cantilever Beam Mesh...")
            nodes, elements = mesh_gen.create_cantilever_beam(
                length=5.0, height=0.5, width=0.3, num_elements=15
            )
            solver.set_mesh(nodes, elements)
            mesh_gen.visualize_mesh("Cantilever Beam Mesh")
            
        elif choice == '2':
            print("\nGenerating Bracket Mesh...")
            nodes, elements = mesh_gen.create_bracket_mesh()
            solver.set_mesh(nodes, elements)
            mesh_gen.visualize_mesh("Bracket Mesh")
            
        elif choice == '3':
            if solver.nodes is None:
                print("Please generate a mesh first!")
                continue
                
            print("\nFEA Analysis Configuration:")
            print("1. Cantilever with Point Load")
            print("2. Cantilever with Distributed Load")
            print("3. Simply Supported with Point Load")
            
            analysis_choice = input("Select analysis type (1-3): ").strip()
            
            if analysis_choice == '1':
                bc_type = 'cantilever'
                load_type = 'point'
                load_magnitude = 5000  # N
            elif analysis_choice == '2':
                bc_type = 'cantilever'
                load_type = 'distributed'
                load_magnitude = 1000  # N
            elif analysis_choice == '3':
                bc_type = 'simply_supported'
                load_type = 'point'
                load_magnitude = 5000  # N
            else:
                print("Invalid choice, using default (Cantilever with Point Load)")
                bc_type = 'cantilever'
                load_type = 'point'
                load_magnitude = 5000
            
            # Set material properties (Steel)
            solver.set_material_properties(E=200e9, nu=0.3)  # Steel
            
            print(f"\nRunning FEA with:")
            print(f"  - Boundary Condition: {bc_type}")
            print(f"  - Load Type: {load_type}")
            print(f"  - Load Magnitude: {load_magnitude} N")
            print(f"  - Material: E={solver.E/1e9:.0f} GPa, ν={solver.nu}")
            
            # Solve FEA
            displacements = solver.solve(bc_type, load_type, load_magnitude)
            
            # Initialize post-processor
            post_processor = PostProcessor(solver)
            report_gen = ReportGenerator(solver, post_processor)
            
            print("FEA Analysis Completed Successfully!")
            
        elif choice == '4':
            if post_processor is None:
                print("Please run FEA analysis first!")
                continue
                
            print("\nVisualization Options:")
            print("1. Plot Deformation")
            print("2. Plot Stress Distribution")
            print("3. 3D Visualization")
            print("4. All Visualizations")
            
            viz_choice = input("Select visualization (1-4): ").strip()
            
            if viz_choice == '1':
                post_processor.plot_deformation()
            elif viz_choice == '2':
                post_processor.plot_stress_distribution()
            elif viz_choice == '3':
                post_processor.create_3d_visualization()
            elif viz_choice == '4':
                post_processor.plot_deformation()
                post_processor.plot_stress_distribution()
                post_processor.create_3d_visualization()
            else:
                print("Invalid choice")
                
        elif choice == '5':
            if report_gen is None:
                print("Please run FEA analysis first!")
                continue
                
            analysis_params = {
                'bc_type': 'cantilever',
                'load_type': 'point', 
                'load_magnitude': 5000
            }
            
            report_gen.generate_comprehensive_report(analysis_params)
            post_processor.generate_summary_report()
            
        elif choice == '6':
            print("\nRunning Complete Demo...")
            
            # Generate mesh
            print("Step 1: Generating mesh...")
            nodes, elements = mesh_gen.create_cantilever_beam(
                length=4.0, height=0.4, width=0.2, num_elements=12
            )
            solver.set_mesh(nodes, elements)
            
            # Set material properties
            solver.set_material_properties(E=200e9, nu=0.3)
            
            # Run analysis
            print("Step 2: Running FEA analysis...")
            displacements = solver.solve('cantilever', 'point', 3000)
            
            # Initialize processors
            post_processor = PostProcessor(solver)
            report_gen = ReportGenerator(solver, post_processor)
            
            # Generate results
            print("Step 3: Generating visualizations...")
            post_processor.plot_deformation()
            post_processor.plot_stress_distribution()
            
            print("Step 4: Generating comprehensive report...")
            analysis_params = {
                'bc_type': 'cantilever',
                'load_type': 'point',
                'load_magnitude': 3000
            }
            report_gen.generate_comprehensive_report(analysis_params)
            
            print("Step 5: Generating summary...")
            post_processor.generate_summary_report()
            
            print("\nDemo Completed Successfully!")
            
        elif choice == '7':
            print("Exiting FEA Application. Goodbye!")
            break
            
        else:
            print("Invalid choice! Please enter a number between 1-7.")

if __name__ == "__main__":
    main()