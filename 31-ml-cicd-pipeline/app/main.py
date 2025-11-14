from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os
from .model import train_model, predict

app = Flask(__name__)

# Load or train model
try:
    model = joblib.load('model.pkl')
except:
    print("Training new model...")
    model = train_model()
    joblib.dump(model, 'model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        data = request.json
        features = np.array(data['features']).reshape(1, -1)
        prediction = predict(model, features)
        return jsonify({
            'prediction': prediction.tolist(),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)