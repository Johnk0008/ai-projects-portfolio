import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.model import train_model, predict
import numpy as np

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_prediction_endpoint(client):
    """Test prediction endpoint with valid data"""
    test_data = {
        'features': [1.2, -0.5, 0.3, 0.8]
    }
    response = client.post('/predict', json=test_data)
    assert response.status_code == 200
    assert 'prediction' in response.json

def test_model_training():
    """Test model training function"""
    model = train_model()
    assert model is not None
    
    # Test prediction
    test_features = np.array([[1.0, 2.0, 3.0, 4.0]])
    prediction = predict(model, test_features)
    assert prediction is not None