import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

def train_model():
    """Train a simple ML model for demonstration"""
    # Generate sample data
    X, y = make_classification(
        n_samples=1000, 
        n_features=4, 
        n_redundant=0, 
        n_informative=4,
        random_state=42
    )
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Print accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model trained with accuracy: {accuracy:.4f}")
    
    return model

def predict(model, features):
    """Make predictions using the trained model"""
    return model.predict(features)