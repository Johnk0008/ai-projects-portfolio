from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from analysis.seismic_analysis import SeismicAnalyzer
from analysis.ml_model import SeismicPredictor
from analysis.visualization import VisualizationEngine
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_structure():
    try:
        data = request.json
        height = float(data['height'])
        base_width = float(data['base_width'])
        seismic_zone = data['seismic_zone']
        soil_type = data['soil_type']
        
        analyzer = SeismicAnalyzer()
        results = analyzer.analyze_building(height, base_width, seismic_zone, soil_type)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict', methods=['POST'])
def predict_performance():
    try:
        data = request.json
        predictor = SeismicPredictor()
        prediction = predictor.predict_performance(data)
        
        return jsonify(prediction)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)