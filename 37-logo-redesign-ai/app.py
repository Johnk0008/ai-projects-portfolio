from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from logo_generator import LogoGenerator
from design_analyzer import DesignAnalyzer
import cv2
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize AI components
logo_gen = LogoGenerator()
design_analyzer = DesignAnalyzer()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    brand_name = request.form.get('brand_name', '')
    industry = request.form.get('industry', '')
    design_style = request.form.get('design_style', 'modern')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Analyze original logo
            analysis = design_analyzer.analyze_logo(filepath)
            
            # Generate redesign concepts
            redesigns = logo_gen.generate_redesigns(
                filepath, 
                brand_name, 
                industry, 
                design_style,
                num_variations=4
            )
            
            return render_template('results.html', 
                                 original_logo=filename,
                                 analysis=analysis,
                                 redesigns=redesigns,
                                 brand_name=brand_name,
                                 industry=industry,
                                 design_style=design_style)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/generate-concepts', methods=['POST'])
def generate_concepts():
    data = request.json
    brand_name = data.get('brand_name')
    industry = data.get('industry')
    style = data.get('style', 'modern')
    
    concepts = logo_gen.generate_text_concepts(brand_name, industry, style)
    return jsonify({'concepts': concepts})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)