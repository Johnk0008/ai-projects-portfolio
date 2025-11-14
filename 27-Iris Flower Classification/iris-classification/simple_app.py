from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os

app = Flask(__name__)

# Check if model exists
if not os.path.exists('model/iris_model.pkl'):
    print("❌ Please run iris_classifier.py first to train the model!")
    model_data = None
else:
    try:
        model_data = joblib.load('model/iris_model.pkl')
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model_data = None

@app.route('/')
def home():
    return '''
    <html>
    <body>
        <h1>Iris Classification</h1>
        <form action="/predict" method="post">
            Sepal Length: <input type="number" step="0.1" name="sepal_length" required><br>
            Sepal Width: <input type="number" step="0.1" name="sepal_width" required><br>
            Petal Length: <input type="number" step="0.1" name="petal_length" required><br>
            Petal Width: <input type="number" step="0.1" name="petal_width" required><br>
            <input type="submit" value="Predict">
        </form>
    </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    if model_data is None:
        return "Model not loaded. Please train the model first."
    
    try:
        # Get input values
        features = [
            float(request.form['sepal_length']),
            float(request.form['sepal_width']), 
            float(request.form['petal_length']),
            float(request.form['petal_width'])
        ]
        
        # Prepare and scale features
        features_scaled = model_data['scaler'].transform([features])
        
        # Make prediction
        prediction_encoded = model_data['model'].predict(features_scaled)[0]
        predicted_species = model_data['label_encoder'].inverse_transform([prediction_encoded])[0]
        
        # Get probabilities
        probabilities = model_data['model'].predict_proba(features_scaled)[0]
        
        result = f"""
        <h2>Prediction Result:</h2>
        <p><b>Predicted Species:</b> {predicted_species}</p>
        <p><b>Probabilities:</b></p>
        <ul>
        """
        for species, prob in zip(model_data['label_encoder'].classes_, probabilities):
            result += f"<li>{species}: {prob:.3f}</li>"
        
        result += f"</ul><p><b>Model Accuracy:</b> {model_data['accuracy']:.4f}</p>"
        result += '<p><a href="/">Make another prediction</a></p>'
        
        return result
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)