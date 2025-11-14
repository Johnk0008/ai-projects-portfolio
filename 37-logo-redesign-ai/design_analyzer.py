import cv2
import numpy as np
from PIL import Image
import os
from typing import Dict, List

class DesignAnalyzer:
    def __init__(self):
        self.design_trends = {
            'modern': ['minimalism', 'geometric', 'negative_space'],
            'minimal': ['simplicity', 'monochrome', 'clean_typography'],
            'vibrant': ['gradients', 'bold_colors', 'organic_shapes'],
            'corporate': ['professional', 'conservative', 'established'],
            'tech': ['futuristic', 'innovative', 'digital_friendly']
        }

    def analyze_logo(self, image_path: str) -> Dict:
        """Comprehensive analysis of original logo"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return self._default_analysis()
            
            analysis = {
                'color_analysis': self._analyze_colors(img),
                'shape_analysis': self._analyze_shapes(img),
                'complexity_score': self._calculate_complexity(img),
                'modernity_score': self._assess_modernity(img),
                'recommendations': self._generate_recommendations(img)
            }
            
            return analysis
            
        except Exception as e:
            print(f"Analysis error: {e}")
            return self._default_analysis()

    def _analyze_colors(self, image: np.ndarray) -> Dict:
        """Analyze color usage in logo"""
        # Convert to RGB
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Calculate color statistics
        avg_color = np.mean(img_rgb, axis=(0, 1))
        std_color = np.std(img_rgb, axis=(0, 1))
        
        # Count distinct colors (simplified)
        unique_colors = len(np.unique(img_rgb.reshape(-1, img_rgb.shape[2]), axis=0))
        
        return {
            'color_count': unique_colors,
            'vibrancy': np.std(avg_color),
            'brightness': np.mean(avg_color),
            'recommendation': 'Reduce color palette' if unique_colors > 6 else 'Good color count'
        }

    def _analyze_shapes(self, image: np.ndarray) -> Dict:
        """Analyze shapes and composition"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Contour analysis
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        shape_complexity = len(contours)
        
        return {
            'contour_count': shape_complexity,
            'symmetry': self._assess_symmetry(gray),
            'balance': 'Balanced' if shape_complexity > 0 else 'Simple',
            'shape_type': 'Geometric' if shape_complexity < 10 else 'Organic'
        }

    def _assess_symmetry(self, gray_image: np.ndarray) -> str:
        """Basic symmetry assessment"""
        # Flip image and compare
        flipped = cv2.flip(gray_image, 1)
        difference = cv2.absdiff(gray_image, flipped)
        similarity = np.mean(difference)
        
        if similarity < 25:
            return 'Highly Symmetrical'
        elif similarity < 50:
            return 'Moderately Symmetrical'
        else:
            return 'Asymmetrical'

    def _calculate_complexity(self, image: np.ndarray) -> float:
        """Calculate visual complexity score"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use variance of Laplacian as focus measure
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Normalize to 0-1 scale
        complexity = min(fm / 1000, 1.0)
        
        return round(complexity, 2)

    def _assess_modernity(self, image: np.ndarray) -> float:
        """Assess how modern the design appears"""
        modernity_factors = 0
        total_factors = 4
        
        # Factor 1: Color count (fewer colors = more modern)
        color_analysis = self._analyze_colors(image)
        if color_analysis['color_count'] <= 4:
            modernity_factors += 1
        
        # Factor 2: Simplicity
        complexity = self._calculate_complexity(image)
        if complexity < 0.5:
            modernity_factors += 1
        
        # Factor 3: Geometric shapes
        shape_analysis = self._analyze_shapes(image)
        if shape_analysis['shape_type'] == 'Geometric':
            modernity_factors += 1
        
        # Factor 4: High contrast
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contrast = gray.std()
        if contrast > 60:
            modernity_factors += 1
        
        return round(modernity_factors / total_factors, 2)

    def _generate_recommendations(self, image: np.ndarray) -> List[str]:
        """Generate redesign recommendations"""
        recommendations = []
        
        color_info = self._analyze_colors(image)
        shape_info = self._analyze_shapes(image)
        modernity = self._assess_modernity(image)
        
        if color_info['color_count'] > 5:
            recommendations.append("Simplify color palette to 2-4 colors for modern appeal")
        
        if modernity < 0.6:
            recommendations.append("Consider geometric shapes and cleaner lines")
        
        if shape_info['contour_count'] > 15:
            recommendations.append("Reduce visual complexity for better scalability")
        
        if len(recommendations) == 0:
            recommendations.append("Logo has good modern characteristics. Focus on subtle refinements")
        
        return recommendations

    def _default_analysis(self) -> Dict:
        """Return default analysis when image processing fails"""
        return {
            'color_analysis': {'color_count': 0, 'vibrancy': 0, 'brightness': 0, 'recommendation': 'Unable to analyze'},
            'shape_analysis': {'contour_count': 0, 'symmetry': 'Unknown', 'balance': 'Unknown', 'shape_type': 'Unknown'},
            'complexity_score': 0,
            'modernity_score': 0,
            'recommendations': ['Upload a clearer image for analysis']
        }