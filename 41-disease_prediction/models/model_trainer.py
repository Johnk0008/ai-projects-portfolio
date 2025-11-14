import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import os

class DiseasePredictor:
    def __init__(self):
        self.models = {
            'svm': SVC(probability=True, random_state=42),
            'logistic_regression': LogisticRegression(random_state=42),
            'random_forest': RandomForestClassifier(random_state=42),
            'xgboost': XGBClassifier(random_state=42, eval_metric='logloss')
        }
        self.scaler = StandardScaler()
        self.trained_models = {}
        self.model_dir = "saved_models"
        os.makedirs(self.model_dir, exist_ok=True)
    
    def preprocess_data(self, X_train, X_test):
        """Preprocess the data"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    
    def train_models(self, X_train, y_train, X_test, y_test, dataset_name):
        """Train all models and evaluate performance"""
        results = {}
        
        # Preprocess data
        X_train_scaled, X_test_scaled = self.preprocess_data(X_train, X_test)
        
        for name, model in self.models.items():
            print(f"Training {name}...")
            
            # Train model
            if name in ['svm', 'logistic_regression']:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                y_pred_proba = model.predict_proba(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'cv_mean': np.mean(cv_scores),
                'cv_std': np.std(cv_scores),
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
            
            self.trained_models[name] = model
            
            print(f"{name} - Accuracy: {accuracy:.4f}, CV Score: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
        
        # Save the best model
        best_model_name = max(results, key=lambda x: results[x]['accuracy'])
        self.save_model(best_model_name, dataset_name)
        
        return results
    
    def save_model(self, model_name, dataset_name):
        """Save trained model"""
        if model_name in self.trained_models:
            filename = f"{self.model_dir}/{dataset_name}_{model_name}.pkl"
            joblib.dump({
                'model': self.trained_models[model_name],
                'scaler': self.scaler
            }, filename)
            print(f"Model saved: {filename}")
    
    def load_model(self, model_path):
        """Load trained model"""
        return joblib.load(model_path)
    
    def predict(self, model_name, X_new, use_scaling=True):
        """Make predictions on new data"""
        if model_name not in self.trained_models:
            raise ValueError(f"Model {model_name} not trained")
        
        model = self.trained_models[model_name]
        
        if use_scaling and model_name in ['svm', 'logistic_regression']:
            X_new = self.scaler.transform(X_new)
        
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(X_new)
            predictions = model.predict(X_new)
            return predictions, probabilities
        else:
            predictions = model.predict(X_new)
            return predictions, None

    def hyperparameter_tuning(self, X_train, y_train, model_name):
        """Perform hyperparameter tuning for specific model"""
        param_grids = {
            'random_forest': {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5]
            },
            'xgboost': {
                'n_estimators': [100, 200],
                'max_depth': [3, 6],
                'learning_rate': [0.01, 0.1]
            },
            'svm': {
                'C': [0.1, 1, 10],
                'kernel': ['linear', 'rbf']
            }
        }
        
        if model_name in param_grids:
            grid_search = GridSearchCV(
                self.models[model_name],
                param_grids[model_name],
                cv=5,
                scoring='accuracy',
                n_jobs=-1
            )
            grid_search.fit(X_train, y_train)
            return grid_search.best_estimator_, grid_search.best_score_
        
        return None, None