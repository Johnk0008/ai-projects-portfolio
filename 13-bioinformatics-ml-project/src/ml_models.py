import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class MLModels:
    def __init__(self):
        self.models = {}
    
    def train_random_forest(self, X, y):
        """Train Random Forest classifier"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        
        y_pred = rf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.models['random_forest'] = rf
        return rf, accuracy, classification_report(y_test, y_pred)
    
    def train_svm(self, X, y):
        """Train Support Vector Machine classifier"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        svm = SVC(kernel='rbf', probability=True, random_state=42)
        svm.fit(X_train, y_train)
        
        y_pred = svm.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.models['svm'] = svm
        return svm, accuracy, classification_report(y_test, y_pred)
    
    def train_neural_network(self, X, y):
        """Train Neural Network classifier"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        # Convert labels to numerical
        y_train_num = (y_train == 'Enzyme').astype(int)
        y_test_num = (y_test == 'Enzyme').astype(int)
        
        nn = MLPClassifier(hidden_layer_sizes=(64, 32), 
                          activation='relu',
                          random_state=42,
                          max_iter=1000)
        nn.fit(X_train, y_train_num)
        
        y_pred = nn.predict(X_test)
        accuracy = accuracy_score(y_test_num, y_pred)
        
        self.models['neural_network'] = nn
        return nn, accuracy, classification_report(y_test_num, y_pred)
    
    def demo_neural_network(self, X, y):
        """Demonstrate deep learning approach"""
        print("Building Neural Network Model...")
        
        # Convert to numerical labels
        y_num = (y == 'Enzyme').astype(int)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_num, test_size=0.3, random_state=42
        )
        
        # Build TensorFlow model
        model = keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Train model
        history = model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        # Evaluate model
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        print(f"Deep Neural Network Accuracy: {test_accuracy:.4f}")
        
        return model, history, test_accuracy
    
    def predict_sequence_function(self, model, sequence_features):
        """Predict function for new sequence features"""
        if hasattr(model, 'predict_proba'):
            prediction = model.predict_proba([sequence_features])[0]
            return prediction
        else:
            prediction = model.predict([sequence_features])[0]
            return prediction