import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import base64
from io import BytesIO
from typing import Dict, List  # Add this import

class VisualizationEngine:
    def __init__(self):
        plt.style.use('seaborn-v0_8')
    
    def create_seismic_force_distribution(self, height: float, base_shear: float) -> str:
        """Create visualization of seismic force distribution"""
        fig = go.Figure()
        
        # Calculate forces at different heights
        heights = np.linspace(0, height, 10)
        forces = base_shear * (heights / height) ** 2  # Triangular distribution
        
        fig.add_trace(go.Scatter(
            x=forces,
            y=heights,
            mode='lines+markers',
            name='Seismic Force',
            line=dict(width=4, color='red')
        ))
        
        fig.update_layout(
            title='Seismic Force Distribution Along Building Height',
            xaxis_title='Lateral Force (kN)',
            yaxis_title='Height (m)',
            showlegend=True,
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def create_performance_chart(self, analysis_results: Dict) -> str:
        """Create performance radar chart"""
        categories = ['Base Shear', 'Drift Control', 'Stiffness', 'Ductility', 'Safety Factor']
        
        values = [
            max(0, 100 - (analysis_results['base_shear'] / 20)),  # Base shear score
            100 if analysis_results['drift_acceptable'] else 60,   # Drift score
            max(60, 100 - analysis_results['lateral_displacement'] / 10),  # Stiffness score
            85,  # Assumed ductility
            analysis_results['performance_score']  # Overall safety
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(0,100,80,0.3)',
            line=dict(color='rgba(0,100,80,0.8)'),
            hoverinfo='text'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title='Structural Performance Radar Chart'
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def create_comparison_chart(self, buildings_data: List) -> str:
        """Create comparison chart for multiple building designs"""
        fig = go.Figure()
        
        for i, building in enumerate(buildings_data):
            fig.add_trace(go.Bar(
                name=f'Design {i+1}',
                x=['Performance Score', 'Base Shear', 'Drift Ratio'],
                y=[
                    building['performance_score'],
                    building['base_shear'] / 10,  # Scale for visualization
                    building['drift_ratio'] * 1000  # Scale for visualization
                ]
            ))
        
        fig.update_layout(
            title='Comparison of Different Building Designs',
            barmode='group',
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn')