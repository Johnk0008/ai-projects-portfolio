import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import os
from typing import List, Dict
import base64
from io import BytesIO

class LogoGenerator:
    def __init__(self):
        self.color_palettes = {
            'modern': ['#2D3047', '#419D78', '#E0A458', '#FFFFFF', '#1E1E24'],
            'minimal': ['#000000', '#FFFFFF', '#666666', '#F0F0F0'],
            'vibrant': ['#FF6B6B', '#4ECDC4', '#FFE66D', '#6A0572', '#1A535C'],
            'corporate': ['#2C3E50', '#34495E', '#E74C3C', '#ECF0F1'],
            'tech': ['#3498DB', '#2C3E50', '#E74C3C', '#27AE60', '#F39C12']
        }
        
        self.font_styles = {
            'modern': ['Arial', 'Helvetica', 'Montserrat'],
            'minimal': ['Roboto', 'Open Sans', 'Lato'],
            'vibrant': ['Poppins', 'Raleway', 'Nunito'],
            'corporate': ['Times New Roman', 'Georgia', 'Garamond'],
            'tech': ['Consolas', 'Courier New', 'Source Code Pro']
        }
        
        # Replace emojis with simple geometric icons
        self.industry_icons = {
            'technology': 'Tech',
            'food': 'ForkKnife',
            'fashion': 'Style',
            'health': 'Health',
            'education': 'Edu',
            'finance': 'Finance',
            'other': 'Logo'
        }

    def generate_redesigns(self, original_path: str, brand_name: str, 
                          industry: str, style: str, num_variations: int = 4) -> List[Dict]:
        """Generate multiple logo redesign variations"""
        variations = []
        
        # Analyze original logo for inspiration
        original_analysis = self._analyze_original(original_path)
        
        for i in range(num_variations):
            variation = self._create_variation(
                brand_name, industry, style, i, original_analysis
            )
            variations.append(variation)
        
        return variations

    def _analyze_original(self, image_path: str) -> Dict:
        """Analyze original logo for color and shape inspiration"""
        img = cv2.imread(image_path)
        if img is None:
            return {}
        
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Simple color analysis (you can enhance this with clustering)
        dominant_colors = self._extract_dominant_colors(img_rgb)
        
        return {
            'dominant_colors': dominant_colors,
            'dimensions': img.shape[:2]
        }

    def _extract_dominant_colors(self, image: np.ndarray, num_colors: int = 3) -> List[str]:
        """Extract dominant colors from image using k-means"""
        pixels = image.reshape(-1, 3)
        pixels = np.float32(pixels)
        
        # Use k-means to find dominant colors
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Convert to hex
        colors = []
        for color in centers:
            colors.append('#{:02x}{:02x}{:02x}'.format(
                int(color[0]), int(color[1]), int(color[2])
            ))
        
        return colors

    def _create_variation(self, brand_name: str, industry: str, 
                         style: str, variation_id: int, original_analysis: Dict) -> Dict:
        """Create a single logo variation"""
        
        # Choose design elements based on style
        colors = self.color_palettes.get(style, self.color_palettes['modern'])
        fonts = self.font_styles.get(style, self.font_styles['modern'])
        
        # Create different design concepts
        if variation_id == 0:
            design = self._create_minimal_logo(brand_name, colors, fonts)
            concept = "Minimal Modern Approach"
        elif variation_id == 1:
            design = self._create_geometric_logo(brand_name, colors, fonts)
            concept = "Geometric Abstract"
        elif variation_id == 2:
            design = self._create_typographic_logo(brand_name, colors, fonts)
            concept = "Typography Focused"
        else:
            design = self._create_iconic_logo(brand_name, industry, colors, fonts)
            concept = "Icon Integration"
        
        # Convert PIL Image to base64 for web display
        buffered = BytesIO()
        design.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            'image_data': f"data:image/png;base64,{img_str}",
            'concept': concept,
            'colors_used': colors[:3],
            'design_logic': self._generate_design_logic(concept, colors, industry, style)
        }

    def _create_minimal_logo(self, brand_name: str, colors: List[str], fonts: List[str]) -> Image.Image:
        """Create minimal logo design"""
        width, height = 400, 300
        img = Image.new('RGB', (width, height), color=colors[-1])  # Use background color
        draw = ImageDraw.Draw(img)
        
        # Draw simple geometric shape
        shape_color = colors[0]
        draw.rectangle([50, 50, 150, 150], fill=shape_color, outline=None)
        
        # Add text
        try:
            font = ImageFont.truetype(fonts[0], 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((180, 120), brand_name, fill=colors[0], font=font)
        
        return img

    def _create_geometric_logo(self, brand_name: str, colors: List[str], fonts: List[str]) -> Image.Image:
        """Create geometric abstract logo"""
        width, height = 400, 300
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw overlapping geometric shapes
        shapes = [
            ('circle', (100, 100, 180, 180), colors[0]),
            ('rectangle', (120, 80, 200, 160), colors[1]),
            ('polygon', [(220, 100), (280, 100), (250, 180)], colors[2])
        ]
        
        for shape_type, coords, color in shapes:
            if shape_type == 'circle':
                draw.ellipse(coords, fill=color)
            elif shape_type == 'rectangle':
                draw.rectangle(coords, fill=color)
            elif shape_type == 'polygon':
                draw.polygon(coords, fill=color)
        
        # Add text
        try:
            font = ImageFont.truetype(fonts[1], 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((150, 200), brand_name.upper(), fill=colors[0], font=font)
        
        return img

    def _create_typographic_logo(self, brand_name: str, colors: List[str], fonts: List[str]) -> Image.Image:
        """Create typography-focused logo"""
        width, height = 400, 200
        img = Image.new('RGB', (width, height), color=colors[-1])
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype(fonts[2], 32)
        except:
            font = ImageFont.load_default()
        
        # Center text
        bbox = draw.textbbox((0, 0), brand_name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), brand_name, fill=colors[0], font=font)
        
        # Add decorative element
        draw.line([(x-10, y+text_height+5), (x+text_width+10, y+text_height+5)], 
                 fill=colors[1], width=3)
        
        return img

    def _create_iconic_logo(self, brand_name: str, industry: str, colors: List[str], fonts: List[str]) -> Image.Image:
        """Create logo with industry-relevant icon using geometric shapes instead of emojis"""
        width, height = 400, 300
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw industry-specific geometric icon
        icon_text = self.industry_icons.get(industry.lower(), 'Logo')
        
        # Create a simple badge/circle with the icon text
        circle_center = (200, 100)
        circle_radius = 40
        
        # Draw circle background
        draw.ellipse([
            circle_center[0] - circle_radius, 
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius, 
            circle_center[1] + circle_radius
        ], fill=colors[0], outline=colors[1], width=2)
        
        # Add icon text
        try:
            icon_font = ImageFont.truetype(fonts[0], 16)
        except:
            icon_font = ImageFont.load_default()
        
        # Center the text in the circle
        bbox = draw.textbbox((0, 0), icon_text, font=icon_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = circle_center[0] - text_width // 2
        text_y = circle_center[1] - text_height // 2
        
        draw.text((text_x, text_y), icon_text, fill='white', font=icon_font)
        
        # Add brand name
        try:
            font = ImageFont.truetype(fonts[0], 24)
        except:
            font = ImageFont.load_default()
        
        # Center brand name below the icon
        bbox = draw.textbbox((0, 0), brand_name, font=font)
        text_width = bbox[2] - bbox[0]
        
        brand_x = (width - text_width) // 2
        brand_y = circle_center[1] + circle_radius + 20
        
        draw.text((brand_x, brand_y), brand_name, fill=colors[1], font=font)
        
        return img

    def _generate_design_logic(self, concept: str, colors: List[str], industry: str, style: str) -> str:
        """Generate design rationale for each variation"""
        design_logic = {
            "Minimal Modern Approach": f"""
            • Clean, uncluttered design for maximum impact
            • Limited color palette ({', '.join(colors[:2])}) for sophistication
            • Geometric shapes for modern aesthetic
            • Suitable for {industry} industry with contemporary appeal
            """,
            
            "Geometric Abstract": f"""
            • Dynamic overlapping shapes create visual interest
            • Color harmony using complementary tones
            • Abstract representation allows for brand interpretation
            • Modern {style} style with mathematical precision
            """,
            
            "Typography Focused": f"""
            • Brand name as the central visual element
            • Carefully selected typography reflects {industry} values
            • Subtle decorative elements enhance without distracting
            • Color scheme: {colors[0]} for prominence, {colors[1]} for accents
            """,
            
            "Icon Integration": f"""
            • Industry-relevant icon for immediate recognition
            • Balanced composition between symbol and typography
            • Color psychology applied for {industry} sector
            • Scalable design maintaining clarity at small sizes
            """
        }
        
        return design_logic.get(concept, "Modern redesign focusing on brand identity and visual appeal.")

    def generate_text_concepts(self, brand_name: str, industry: str, style: str) -> List[str]:
        """Generate textual design concepts"""
        concepts = [
            f"Modern minimalist logo for {brand_name} using clean lines and limited color palette",
            f"Geometric abstract design representing {industry} innovation",
            f"Typography-driven logo focusing on custom letterforms for {brand_name}",
            f"Icon-integrated logo combining symbolic imagery with {style} typography",
            f"Responsive logo system that adapts across digital platforms",
            f"Vibrant color gradient approach for {industry} sector appeal"
        ]
        
        return concepts