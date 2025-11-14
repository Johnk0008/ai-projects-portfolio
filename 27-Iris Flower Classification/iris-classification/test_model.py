import pandas as pd
import numpy as np
import joblib
import os

def test_model_loading():
    """Test if the model loads correctly"""
    print("=== Testing Model Loading ===")
    
    if not os.path.exists('model/iris_model.pkl'):
        print("❌ Model file not found! Please run iris_classifier.py first.")
        return False
    
    try:
        model_data = joblib.load('model/iris_model.pkl')
        print("✅ Model loaded successfully!")
        print(f"Model type: {type(model_data['model'])}")
        print(f"Accuracy: {model_data['accuracy']}")
        print(f"Classes: {model_data['label_encoder'].classes_}")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def test_prediction():
    """Test making a prediction"""
    print("\n=== Testing Prediction ===")
    
    if not os.path.exists('model/iris_model.pkl'):
        print("❌ Model file not found!")
        return False
    
    try:
        model_data = joblib.load('model/iris_model.pkl')
        
        # Test samples for each species
        test_samples = {
            'Iris-setosa': [5.1, 3.5, 1.4, 0.2],
            'Iris-versicolor': [6.0, 2.7, 5.1, 1.6],
            'Iris-virginica': [6.3, 3.3, 6.0, 2.5]
        }
        
        for expected_species, features in test_samples.items():
            print(f"\nTesting {expected_species}: {features}")
            
            # Prepare features
            features_array = np.array([features])
            features_scaled = model_data['scaler'].transform(features_array)
            
            # Make prediction
            model = model_data['model']
            prediction_encoded = model.predict(features_scaled)[0]
            predicted_species = model_data['label_encoder'].inverse_transform([prediction_encoded])[0]
            
            # Get probabilities
            try:
                probabilities = model.predict_proba(features_scaled)[0]
                prob_dict = {
                    species: f"{prob:.3f}"
                    for species, prob in zip(model_data['label_encoder'].classes_, probabilities)
                }
            except AttributeError:
                prob_dict = {species: "N/A" for species in model_data['label_encoder'].classes_}
            
            print(f"✅ Predicted: {predicted_species}, Expected: {expected_species}")
            print(f"Probabilities: {prob_dict}")
            
            if predicted_species != expected_species:
                print(f"❌ Prediction mismatch!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in prediction test: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Running model tests...")
    
    # Test 1: Model loading
    load_success = test_model_loading()
    
    # Test 2: Prediction
    if load_success:
        test_prediction()
    
    print("\n=== Test Complete ===")