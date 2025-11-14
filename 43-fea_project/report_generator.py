import matplotlib.pyplot as plt
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, solver, post_processor):
        self.solver = solver
        self.post_processor = post_processor
        self.report_dir = "results/report"
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate_comprehensive_report(self, analysis_params):
        """Generate comprehensive FEA report"""
        print("Generating comprehensive FEA report...")
        
        # Create report figure
        fig = plt.figure(figsize=(20, 16))
        
        # Title and parameters
        ax_title = fig.add_axes([0.1, 0.95, 0.8, 0.05])
        ax_title.axis('off')
        ax_title.text(0.5, 0.5, 'FINITE ELEMENT ANALYSIS REPORT', 
                     ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Analysis parameters
        ax_params = fig.add_axes([0.1, 0.88, 0.8, 0.06])
        ax_params.axis('off')
        params_text = (
            f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Boundary Condition: {analysis_params['bc_type']} | "
            f"Load Type: {analysis_params['load_type']} | "
            f"Load Magnitude: {analysis_params['load_magnitude']} N | "
            f"Material: E={self.solver.E/1e9:.0f} GPa, ν={self.solver.nu}"
        )
        ax_params.text(0.02, 0.5, params_text, va='center', fontsize=10)
        
        # Results summary
        von_mises = self.solver.get_von_mises_stress()
        max_disp = self.solver.get_max_displacement()
        yield_strength = 250e6
        fos = yield_strength / np.max(von_mises) if np.max(von_mises) > 0 else float('inf')
        
        ax_results = fig.add_axes([0.1, 0.82, 0.8, 0.05])
        ax_results.axis('off')
        results_text = (
            f"RESULTS: Max Displacement: {max_disp*1000:.3f} mm | "
            f"Max Stress: {np.max(von_mises)/1e6:.2f} MPa | "
            f"Min Stress: {np.min(von_mises)/1e6:.2f} MPa | "
            f"Factor of Safety: {fos:.2f}"
        )
        ax_results.text(0.02, 0.5, results_text, va='center', fontsize=10, 
                       fontweight='bold', color='red' if fos < 2 else 'green')
        
        # Plot 1: Mesh
        ax1 = fig.add_subplot(3, 3, 1, projection='3d')
        ax1.scatter(self.solver.nodes[:,0], self.solver.nodes[:,1], self.solver.nodes[:,2], 
                   c='blue', alpha=0.6, s=10)
        ax1.set_title('Finite Element Mesh')
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        
        # Plot 2: Deformation
        ax2 = fig.add_subplot(3, 3, 2, projection='3d')
        scale_factor = 50
        deformed_nodes = self.solver.nodes + self.solver.displacements.reshape(-1, 3) * scale_factor
        ax2.scatter(deformed_nodes[:,0], deformed_nodes[:,1], deformed_nodes[:,2], 
                   c='red', alpha=0.6, s=10)
        ax2.set_title(f'Deformed Shape ({scale_factor}x scale)')
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        
        # Plot 3: Von Mises Stress
        ax3 = fig.add_subplot(3, 3, 3)
        sc3 = ax3.scatter(self.solver.nodes[:,0], self.solver.nodes[:,2], 
                         c=von_mises[self.solver.elements[:,0]], cmap='jet', s=50)
        ax3.set_title('Von Mises Stress Distribution')
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Z (m)')
        plt.colorbar(sc3, ax=ax3, label='Stress (Pa)')
        
        # Plot 4: Displacement contour
        ax4 = fig.add_subplot(3, 3, 4)
        displacement_magnitudes = np.sqrt(
            self.solver.displacements[0::3]**2 + 
            self.solver.displacements[1::3]**2 + 
            self.solver.displacements[2::3]**2
        )
        sc4 = ax4.scatter(self.solver.nodes[:,0], self.solver.nodes[:,2], 
                         c=displacement_magnitudes, cmap='coolwarm', s=50)
        ax4.set_title('Displacement Magnitude')
        ax4.set_xlabel('X (m)')
        ax4.set_ylabel('Z (m)')
        plt.colorbar(sc4, ax=ax4, label='Displacement (m)')
        
        # Plot 5: Stress histogram
        ax5 = fig.add_subplot(3, 3, 5)
        ax5.hist(von_mises, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax5.set_title('Stress Distribution Histogram')
        ax5.set_xlabel('Von Mises Stress (Pa)')
        ax5.set_ylabel('Frequency')
        ax5.axvline(np.mean(von_mises), color='red', linestyle='--', label=f'Mean: {np.mean(von_mises)/1e6:.1f} MPa')
        ax5.legend()
        
        # Plot 6: Displacement histogram
        ax6 = fig.add_subplot(3, 3, 6)
        ax6.hist(displacement_magnitudes, bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
        ax6.set_title('Displacement Distribution Histogram')
        ax6.set_xlabel('Displacement Magnitude (m)')
        ax6.set_ylabel('Frequency')
        ax6.axvline(np.mean(displacement_magnitudes), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(displacement_magnitudes)*1000:.3f} mm')
        ax6.legend()
        
        # Plot 7: Factor of safety visualization
        ax7 = fig.add_subplot(3, 3, 7)
        categories = ['Yield Strength', 'Max Stress']
        values = [yield_strength/1e6, np.max(von_mises)/1e6]
        colors = ['green' if fos >= 2 else 'orange', 'red']
        bars = ax7.bar(categories, values, color=colors, alpha=0.7)
        ax7.set_title('Stress vs Yield Strength')
        ax7.set_ylabel('Stress (MPa)')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            ax7.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    f'{value:.1f}', ha='center', va='bottom')
        
        # Plot 8: Observations
        ax8 = fig.add_subplot(3, 3, 8)
        ax8.axis('off')
        
        observations = [
            "OBSERVATIONS:",
            f"1. Maximum deformation occurs at free end",
            f"2. Stress concentration at fixed support",
            f"3. Maximum stress: {np.max(von_mises)/1e6:.2f} MPa",
            f"4. Maximum displacement: {max_disp*1000:.3f} mm",
            f"5. Factor of Safety: {fos:.2f}",
            f"6. Material utilization: {np.max(von_mises)/yield_strength*100:.1f}%"
        ]
        
        if fos < 1:
            observations.append("❌ CRITICAL: Structure will fail!")
            color = 'red'
        elif fos < 2:
            observations.append("⚠️ WARNING: Low safety margin!")
            color = 'orange'
        else:
            observations.append("✅ ACCEPTABLE: Structure is safe")
            color = 'green'
        
        ax8.text(0.02, 0.95, "\n".join(observations), va='top', fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.2))
        
        # Plot 9: Recommendations
        ax9 = fig.add_subplot(3, 3, 9)
        ax9.axis('off')
        
        recommendations = [
            "RECOMMENDATIONS:",
            f"1. {'Increase cross-section' if fos < 2 else 'Current design adequate'}",
            f"2. {'Use higher strength material' if fos < 1.5 else 'Material selection OK'}",
            f"3. {'Add reinforcement at stress concentration' if np.max(von_mises) > yield_strength*0.8 else 'Stress distribution acceptable'}",
            f"4. {'Consider dynamic loading effects' if max_disp > 0.01 else 'Stiffness adequate'}",
            f"5. {'Verify with experimental testing' if fos < 3 else 'Analytical results reliable'}"
        ]
        
        ax9.text(0.02, 0.95, "\n".join(recommendations), va='top', fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.3))
        
        plt.tight_layout(rect=[0, 0, 1, 0.9])
        
        # Save report
        report_filename = f"{self.report_dir}/fea_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(report_filename, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Comprehensive report saved as: {report_filename}")
        
        return report_filename