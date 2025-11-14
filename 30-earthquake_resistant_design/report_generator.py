# report_generator.py
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
    
    def generate_report(self, analysis_data, filename='earthquake_resistant_design_report.pdf'):
        self.pdf.add_page()
        
        # Title Page
        self.add_title_page()
        
        # Table of Contents
        self.add_table_of_contents()
        
        # Chapters
        self.add_introduction()
        self.add_seismic_principles()
        self.add_analysis_results(analysis_data)
        self.add_design_recommendations()
        self.add_conclusion()
        
        self.pdf.output(filename)
    
    def add_title_page(self):
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, 'Earthquake-Resistant Building Design Analysis', 0, 1, 'C')
        self.pdf.ln(20)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(0, 10, 
            'A Comprehensive Analysis of Seismic Design Principles\n'
            'with AI/ML Performance Prediction\n\n'
            'Generated on: ' + datetime.now().strftime('%Y-%m-%d')
        )
    
    def add_table_of_contents(self):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, 'Table of Contents', 0, 1)
        self.pdf.ln(10)
        
        contents = [
            '1. Introduction',
            '2. Seismic Design Principles',
            '3. Analysis Results',
            '4. Design Recommendations',
            '5. Conclusion'
        ]
        
        for item in contents:
            self.pdf.set_font('Arial', '', 12)
            self.pdf.cell(0, 10, item, 0, 1)
    
    def add_introduction(self):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, '1. Introduction', 0, 1)
        self.pdf.ln(5)
        
        intro_text = """
Earthquake-resistant design is a critical aspect of structural engineering that focuses 
on creating buildings capable of withstanding seismic events. This report presents a 
comprehensive analysis of seismic design principles integrated with machine learning 
for performance prediction.

Key objectives:
• Analyze structural response to seismic forces
• Predict building performance using AI/ML models
• Provide design recommendations for earthquake resistance
• Visualize force distribution and structural behavior

The integration of traditional engineering principles with modern AI techniques 
enables more accurate predictions and optimized design solutions.
"""
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(0, 8, intro_text)
    
    def add_seismic_principles(self):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, '2. Seismic Design Principles', 0, 1)
        self.pdf.ln(5)
        
        principles = """
Fundamental Principles of Earthquake-Resistant Design:

1. Strength and Stiffness
   - Adequate lateral load resistance
   - Controlled deformation under seismic forces
   - Balanced strength distribution

2. Ductility and Energy Dissipation
   - Ability to undergo large deformations without collapse
   - Energy absorption through plastic hinge formation
   - Controlled inelastic behavior

3. Regularity and Symmetry
   - Uniform mass and stiffness distribution
   - Avoidance of torsional irregularities
   - Symmetrical plan configuration

4. Redundancy and Continuous Load Path
   - Multiple load paths for force transmission
   - Robust connections between structural elements
   - Continuous reinforcement detailing

5. Foundation Design
   - Adequate soil-structure interaction
   - Prevention of differential settlement
   - Consideration of liquefaction potential
"""
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(0, 8, principles)
    
    def add_analysis_results(self, analysis_data):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, '3. Analysis Results', 0, 1)
        self.pdf.ln(5)
        
        results_text = f"""
Structural Analysis Summary:

Building Parameters:
• Height: {analysis_data.get('height', 'N/A')} m
• Base Width: {analysis_data.get('base_width', 'N/A')} m
• Seismic Zone: {analysis_data.get('seismic_zone', 'N/A')}
• Soil Type: {analysis_data.get('soil_type', 'N/A')}

Analysis Results:
• Base Shear: {analysis_data.get('base_shear', 'N/A')} kN
• Seismic Coefficient: {analysis_data.get('seismic_coefficient', 'N/A')}
• Fundamental Period: {analysis_data.get('fundamental_period', 'N/A')} sec
• Lateral Displacement: {analysis_data.get('lateral_displacement', 'N/A')} mm
• Drift Ratio: {analysis_data.get('drift_ratio', 'N/A')}
• Performance Score: {analysis_data.get('performance_score', 'N/A')}/100

The analysis indicates the structural system {'meets' if analysis_data.get('performance_score', 0) >= 80 else 'requires improvement for'} 
seismic design requirements.
"""
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(0, 8, results_text)
    
    def add_design_recommendations(self):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, '4. Design Recommendations', 0, 1)
        self.pdf.ln(5)
        
        recommendations = """
Recommended Design Strategies:

1. Structural System Selection
   • Moment-resisting frames for low to medium rise
   • Shear wall systems for high-rise buildings
   • Dual systems combining frames and walls
   • Braced frames for industrial structures

2. Material Considerations
   • High-strength concrete with proper confinement
   • Ductile steel reinforcement detailing
   • Energy dissipating devices
   • Base isolation systems for critical facilities

3. Detailing Requirements
   • Strong column-weak beam concept
   • Proper lap splices and anchorage
   • Confinement reinforcement in potential plastic zones
   • Avoidance of brittle failure modes

4. Advanced Technologies
   • Seismic base isolation
   • Energy dissipation devices
   • Active and passive control systems
   • Real-time structural health monitoring
"""
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(0, 8, recommendations)
    
    def add_conclusion(self):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.cell(0, 10, '5. Conclusion', 0, 1)
        self.pdf.ln(5)
        
        conclusion = """
Earthquake-resistant design requires a comprehensive approach combining 
traditional engineering principles with modern computational methods. The 
integration of AI/ML techniques enhances our ability to predict structural 
performance and optimize design solutions.

Key takeaways:
• Seismic design must consider multiple performance objectives
• Regular structural configuration significantly improves seismic response
• Advanced analysis methods provide more accurate performance predictions
• Continuous monitoring and assessment are essential for structural safety

Future developments in seismic design will likely incorporate more sophisticated 
AI models, real-time monitoring systems, and adaptive structural technologies 
to further enhance earthquake resilience.
"""
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(0, 8, conclusion)

# Usage example
if __name__ == '__main__':
    sample_data = {
        'height': 30,
        'base_width': 20,
        'seismic_zone': 'Zone IV',
        'soil_type': 'Type II',
        'base_shear': 845.32,
        'seismic_coefficient': 0.024,
        'fundamental_period': 1.23,
        'lateral_displacement': 45.6,
        'drift_ratio': 0.0032,
        'performance_score': 85.5
    }
    
    generator = ReportGenerator()
    generator.generate_report(sample_data)