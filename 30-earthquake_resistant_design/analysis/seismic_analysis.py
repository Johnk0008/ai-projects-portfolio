import numpy as np
import pandas as pd
from typing import Dict, List  # Ensure these imports are present

class SeismicAnalyzer:
    def __init__(self):
        self.seismic_coefficients = {
            'Zone II': 0.10,
            'Zone III': 0.16,
            'Zone IV': 0.24,
            'Zone V': 0.36
        }
        
        self.soil_factors = {
            'Type I': 1.0,  # Hard soil
            'Type II': 1.2, # Medium soil
            'Type III': 1.5 # Soft soil
        }
    
    def calculate_base_shear(self, height: float, base_width: float, 
                           seismic_zone: str, soil_type: str) -> Dict:
        """Calculate base shear using equivalent lateral force method"""
        
        # Fundamental period (Empirical formula)
        T = 0.075 * (height ** 0.75)
        
        # Seismic coefficient
        Z = self.seismic_coefficients.get(seismic_zone, 0.24)
        S = self.soil_factors.get(soil_type, 1.2)
        
        # Response reduction factor (depends on structural system)
        R = 5.0  # For moment-resisting frame
        
        # Design horizontal acceleration coefficient
        Ah = (Z * S) / (2 * R)
        
        # Building weight estimation (simplified)
        floor_area = base_width * base_width
        weight_per_floor = floor_area * 12  # kN (assuming 12 kN/m²)
        total_weight = weight_per_floor * (height / 3)  # Assuming 3m per floor
        
        # Base shear
        base_shear = Ah * total_weight
        
        return {
            'base_shear': round(base_shear, 2),
            'seismic_coefficient': round(Ah, 4),
            'fundamental_period': round(T, 2),
            'total_weight': round(total_weight, 2)
        }
    
    def analyze_drift(self, height: float, base_shear: float) -> Dict:
        """Calculate inter-story drift"""
        
        # Simplified drift calculation
        stiffness = 50000  # kN/m (assumed)
        lateral_force = base_shear
        lateral_displacement = lateral_force / stiffness
        
        # Inter-story drift
        drift_ratio = lateral_displacement / height
        
        # Check against code limits (0.004 typically)
        drift_ok = drift_ratio <= 0.004
        
        return {
            'lateral_displacement': round(lateral_displacement * 1000, 2),  # mm
            'drift_ratio': round(drift_ratio, 4),
            'drift_acceptable': drift_ok
        }
    
    def analyze_building(self, height: float, base_width: float, 
                        seismic_zone: str, soil_type: str) -> Dict:
        """Complete building seismic analysis"""
        
        base_shear_results = self.calculate_base_shear(
            height, base_width, seismic_zone, soil_type
        )
        
        drift_results = self.analyze_drift(height, base_shear_results['base_shear'])
        
        # Combine results
        results = {**base_shear_results, **drift_results}
        
        # Performance rating
        performance_score = self.calculate_performance_score(results)
        results['performance_score'] = performance_score
        results['recommendations'] = self.generate_recommendations(results)
        
        return results
    
    def calculate_performance_score(self, results: Dict) -> float:
        """Calculate overall seismic performance score"""
        
        score = 100
        
        # Penalize high drift
        if not results['drift_acceptable']:
            score -= 20
        
        # Penalize high base shear
        if results['base_shear'] > 1000:
            score -= (results['base_shear'] - 1000) / 50
        
        return max(60, round(score, 1))
    
    def generate_recommendations(self, results: Dict) -> List[str]:
        """Generate design recommendations based on analysis"""
        
        recommendations = []
        
        if not results['drift_acceptable']:
            recommendations.extend([
                "Increase structural stiffness with shear walls",
                "Consider adding bracing systems",
                "Optimize column and beam sizes"
            ])
        
        if results['base_shear'] > 1500:
            recommendations.extend([
                "Implement base isolation system",
                "Use energy dissipation devices",
                "Consider structural damping systems"
            ])
        
        if results['performance_score'] < 80:
            recommendations.append("Review structural system and consider retrofit")
        
        if not recommendations:
            recommendations.append("Design meets seismic requirements")
        
        return recommendations