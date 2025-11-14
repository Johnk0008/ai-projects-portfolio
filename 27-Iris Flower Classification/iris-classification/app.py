from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os

app = Flask(__name__)

# Load the trained model
def load_model():
    try:
        model_data = joblib.load('model/iris_model.pkl')
        return model_data
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

model_data = load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model_data is None:
        return jsonify({'error': 'Model not loaded'})
    
    try:
        # Get data from form
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])
        
        # Prepare features
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        
        # Scale features
        features_scaled = model_data['scaler'].transform(features)
        
        # Make prediction
        model = model_data['model']
        prediction_encoded = model.predict(features_scaled)[0]
        
        # Convert back to species name
        predicted_species = model_data['label_encoder'].inverse_transform([prediction_encoded])[0]
        
        # Get probabilities if available
        try:
            probabilities = model.predict_proba(features_scaled)[0]
            prob_results = {
                species: f"{prob:.3f}"
                for species, prob in zip(model_data['label_encoder'].classes_, probabilities)
            }
        except AttributeError:
            # If model doesn't support predict_proba
            prob_results = {
                species: "N/A" 
                for species in model_data['label_encoder'].classes_
            }
        
        return jsonify({
            'prediction': predicted_species,
            'probabilities': prob_results,
            'accuracy': f"{model_data['accuracy']:.4f}",
            'model_name': model_data.get('model_name', 'Unknown')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for programmatic access"""
    if model_data is None:
        return jsonify({'error': 'Model not loaded'})
    
    try:
        data = request.get_json()
        
        sepal_length = float(data['sepal_length'])
        sepal_width = float(data['sepal_width'])
        petal_length = float(data['petal_length'])
        petal_width = float(data['petal_width'])
        
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        features_scaled = model_data['scaler'].transform(features)
        
        model = model_data['model']
        prediction_encoded = model.predict(features_scaled)[0]
        predicted_species = model_data['label_encoder'].inverse_transform([prediction_encoded])[0]
        
        # Get probabilities if available
        try:
            probabilities = model.predict_proba(features_scaled)[0]
            prob_dict = {
                species: float(prob)
                for species, prob in zip(model_data['label_encoder'].classes_, probabilities)
            }
        except AttributeError:
            prob_dict = {
                species: 0.0
                for species in model_data['label_encoder'].classes_
            }
        
        return jsonify({
            'prediction': predicted_species,
            'probabilities': prob_dict,
            'model_accuracy': float(model_data['accuracy']),
            'model_name': model_data.get('model_name', 'Unknown')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/model_info')
def model_info():
    """Endpoint to get model information"""
    if model_data is None:
        return jsonify({'error': 'Model not loaded'})
    
    return jsonify({
        'model_name': model_data.get('model_name', 'Unknown'),
        'accuracy': float(model_data['accuracy']),
        'classes': list(model_data['label_encoder'].classes_)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)