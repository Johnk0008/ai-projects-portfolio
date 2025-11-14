import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split
import urllib.request
import os

class MedicalDataLoader:
    def __init__(self):
        self.data_path = "data/"
        os.makedirs(self.data_path, exist_ok=True)
    
    def load_heart_disease(self):
        """Load Heart Disease dataset"""
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
        column_names = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
        ]
        
        try:
            data = pd.read_csv(url, names=column_names, na_values='?')
            data['target'] = (data['target'] > 0).astype(int)  # Binary classification
            data = data.dropna()
            return data
        except:
            # Fallback: Create synthetic data
            return self._create_synthetic_heart_data()
    
    def load_diabetes(self):
        """Load Diabetes dataset"""
        diabetes = load_diabetes()
        df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
        # Create binary target (1 if disease progression > median)
        df['target'] = (diabetes.target > np.median(diabetes.target)).astype(int)
        return df
    
    def load_breast_cancer(self):
        """Load Breast Cancer dataset"""
        cancer = load_breast_cancer()
        df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
        df['target'] = cancer.target
        return df
    
    def _create_synthetic_heart_data(self):
        """Create synthetic heart disease data for demo"""
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'age': np.random.randint(29, 80, n_samples),
            'sex': np.random.randint(0, 2, n_samples),
            'cp': np.random.randint(0, 4, n_samples),
            'trestbps': np.random.randint(90, 200, n_samples),
            'chol': np.random.randint(120, 600, n_samples),
            'fbs': np.random.randint(0, 2, n_samples),
            'restecg': np.random.randint(0, 3, n_samples),
            'thalach': np.random.randint(70, 210, n_samples),
            'exang': np.random.randint(0, 2, n_samples),
            'oldpeak': np.round(np.random.uniform(0, 6.2, n_samples), 1),
            'slope': np.random.randint(0, 3, n_samples),
            'ca': np.random.randint(0, 4, n_samples),
            'thal': np.random.randint(0, 4, n_samples),
        }
        
        df = pd.DataFrame(data)
        # Synthetic target based on combinations of features
        risk_score = (
            (df['age'] > 55).astype(int) * 2 +
            (df['chol'] > 240).astype(int) * 2 +
            (df['trestbps'] > 140).astype(int) * 2 +
            (df['oldpeak'] > 2).astype(int) * 3
        )
        df['target'] = (risk_score > 4).astype(int)
        
        return df
    
    def get_dataset(self, dataset_name):
        """Get specific dataset by name"""
        datasets = {
            'heart': self.load_heart_disease,
            'diabetes': self.load_diabetes,
            'breast_cancer': self.load_breast_cancer
        }
        
        if dataset_name in datasets:
            return datasets[dataset_name]()
        else:
            raise ValueError(f"Dataset {dataset_name} not found. Available: {list(datasets.keys())}")
    
    def prepare_data(self, dataset_name, test_size=0.2, random_state=42):
        """Prepare data for training"""
        data = self.get_dataset(dataset_name)
        X = data.drop('target', axis=1)
        y = data['target']
        
        return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)