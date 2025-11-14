import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
from config import *

class ModelTrainer:
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_score = 0
        
    def initialize_models(self):
        """Initialize multiple classification models"""
        self.models = {
            'logistic_regression': {
                'model': LogisticRegression(random_state=RANDOM_STATE, max_iter=1000),
                'params': {
                    'C': [0.1, 1, 10],
                    'penalty': ['l1', 'l2'],
                    'solver': ['liblinear']
                }
            },
            'decision_tree': {
                'model': DecisionTreeClassifier(random_state=RANDOM_STATE),
                'params': {
                    'max_depth': [3, 5, 7, 10, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                }
            },
            'random_forest': {
                'model': RandomForestClassifier(random_state=RANDOM_STATE),
                'params': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [3, 5, 7, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                }
            },
            'gradient_boosting': {
                'model': GradientBoostingClassifier(random_state=RANDOM_STATE),
                'params': {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 4, 5]
                }
            }
        }
    
    def train_models(self, X_train, y_train, cv=5):
        """Train multiple models using GridSearchCV"""
        self.initialize_models()
        
        results = {}
        
        for name, model_info in self.models.items():
            print(f"Training {name}...")
            
            # Perform grid search
            grid_search = GridSearchCV(
                model_info['model'],
                model_info['params'],
                cv=cv,
                scoring='f1',
                n_jobs=-1,
                verbose=1
            )
            
            grid_search.fit(X_train, y_train)
            
            # Store results
            results[name] = {
                'model': grid_search.best_estimator_,
                'best_params': grid_search.best_params_,
                'best_score': grid_search.best_score_,
                'cv_results': grid_search.cv_results_
            }
            
            print(f"Best {name} score: {grid_search.best_score_:.4f}")
            print(f"Best parameters: {grid_search.best_params_}")
            
            # Update best model
            if grid_search.best_score_ > self.best_score:
                self.best_score = grid_search.best_score_
                self.best_model = grid_search.best_estimator_
        
        self.models = results
        return results
    
    def predict(self, model_name, X):
        """Make predictions using a specific model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        return self.models[model_name]['model'].predict(X)
    
    def predict_proba(self, model_name, X):
        """Get prediction probabilities using a specific model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        return self.models[model_name]['model'].predict_proba(X)
    
    def save_model(self, model_name, file_path):
        """Save a trained model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        joblib.dump(self.models[model_name]['model'], file_path)
    
    def save_best_model(self, file_path):
        """Save the best performing model"""
        if self.best_model is None:
            raise ValueError("No best model to save")
        
        joblib.dump(self.best_model, file_path)