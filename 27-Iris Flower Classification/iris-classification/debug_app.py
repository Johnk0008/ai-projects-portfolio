from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os
import traceback

app = Flask(__name__)

# Load the trained model
def load_model():
    try:
        print("Attempting to load model...")
        if not os.path.exists('model/iris_model.pkl'):
            print("ERROR: Model file not found!")
            return None
        
        model_data = joblib.load('model/iris_model.pkl')
        print("Model loaded successfully!")
        print(f"Model type: {type(model_data['model'])}")
        print(f"Model accuracy: {model_data['accuracy']}")
        print(f"Classes: {model_data['label_encoder'].classes_}")
        return model_data
    except Exception as e:
        print(f"Error loading model: {e}")
        print(traceback.format_exc())
        return None

model_data = load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model_data is None:
        return jsonify({'error': 'Model not loaded. Please train the model first.'})
    
    try:
        print("\n=== Prediction Request ===")
        # Get data from form
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])
        
        print(f"Input features: {[sepal_length, sepal_width, petal_length, petal_width]}")
        
        # Prepare features
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        print(f"Features shape: {features.shape}")
        
        # Scale features
        features_scaled = model_data['scaler'].transform(features)
        print(f"Scaled features: {features_scaled}")
        
        # Make prediction
        model = model_data['model']
        prediction_encoded = model.predict(features_scaled)[0]
        print(f"Encoded prediction: {prediction_encoded}")
        
        # Convert back to species name
        predicted_species = model_data['label_encoder'].inverse_transform([prediction_encoded])[0]
        print(f"Predicted species: {predicted_species}")
        
        # Get probabilities if available
        prob_results = {}
        try:
            probabilities = model.predict_proba(features_scaled)[0]
            print(f"Probabilities: {probabilities}")
            prob_results = {
                species: f"{prob:.3f}"
                for species, prob in zip(model_data['label_encoder'].classes_, probabilities)
            }
        except AttributeError as e:
            print(f"Probability not available: {e}")
            prob_results = {
                species: "N/A" 
                for species in model_data['label_encoder'].classes_
            }
        
        print("=== Prediction Successful ===")
        return jsonify({
            'prediction': predicted_species,
            'probabilities': prob_results,
            'accuracy': f"{model_data['accuracy']:.4f}",
            'model_name': model_data.get('model_name', 'Unknown')
        })
        
    except Exception as e:
        print(f"ERROR in prediction: {e}")
        print(traceback.format_exc())
        return jsonify({'error': f'Prediction failed: {str(e)}'})

@app.route('/check_model')
def check_model():
    """Endpoint to check model status"""
    if model_data is None:
        return jsonify({'status': 'error', 'message': 'Model not loaded'})
    
    return jsonify({
        'status': 'success',
        'model_name': model_data.get('model_name', 'Unknown'),
        'accuracy': float(model_data['accuracy']),
        'classes': list(model_data['label_encoder'].classes_),
        'model_type': str(type(model_data['model']))
    })

if __name__ == '__main__':
    print("Starting Flask app...")
    print(f"Model data: {model_data}")
    app.run(debug=True, host='0.0.0.0', port=5000)