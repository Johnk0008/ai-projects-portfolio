import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import Dict  # Add this import

class SeismicPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = 'models/seismic_model.pkl'
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load existing model or train new one"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.train_model()
    
    def generate_training_data(self) -> pd.DataFrame:
        """Generate synthetic training data for seismic performance"""
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'height': np.random.uniform(10, 200, n_samples),
            'base_width': np.random.uniform(10, 50, n_samples),
            'seismic_zone_encoded': np.random.randint(1, 5, n_samples),
            'soil_type_encoded': np.random.randint(1, 4, n_samples),
            'concrete_grade': np.random.uniform(25, 50, n_samples),
            'steel_yield_strength': np.random.uniform(415, 550, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Calculate target variable (performance score)
        df['performance_score'] = self.calculate_target_score(df)
        
        return df
    
    def calculate_target_score(self, df: pd.DataFrame) -> np.ndarray:
        """Calculate target performance score based on features"""
        score = (
            100 
            - 0.1 * df['height'] 
            + 0.5 * df['base_width'] 
            - 5 * df['seismic_zone_encoded']
            - 3 * df['soil_type_encoded']
            + 0.2 * df['concrete_grade']
            + 0.1 * df['steel_yield_strength']
            + np.random.normal(0, 5, len(df))
        )
        return np.clip(score, 60, 100)
    
    def train_model(self):
        """Train the ML model"""
        print("Training seismic performance prediction model...")
        
        # Generate training data
        df = self.generate_training_data()
        
        # Prepare features and target
        features = ['height', 'base_width', 'seismic_zone_encoded', 
                   'soil_type_encoded', 'concrete_grade', 'steel_yield_strength']
        X = df[features]
        y = df['performance_score']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Save model
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        
        # Calculate training score
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Model trained - Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
    
    def predict_performance(self, input_data: Dict) -> Dict:
        """Predict seismic performance for given input"""
        
        # Encode categorical variables
        zone_encoding = {'Zone II': 1, 'Zone III': 2, 'Zone IV': 3, 'Zone V': 4}
        soil_encoding = {'Type I': 1, 'Type II': 2, 'Type III': 3}
        
        features = np.array([[
            input_data['height'],
            input_data['base_width'],
            zone_encoding.get(input_data['seismic_zone'], 3),
            soil_encoding.get(input_data['soil_type'], 2),
            input_data.get('concrete_grade', 30),
            input_data.get('steel_yield_strength', 500)
        ]])
        
        # Scale features and predict
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        
        return {
            'predicted_performance_score': round(prediction, 1),
            'risk_level': self.assess_risk_level(prediction)
        }
    
    def assess_risk_level(self, score: float) -> str:
        """Assess risk level based on performance score"""
        if score >= 90:
            return "Low Risk"
        elif score >= 80:
            return "Moderate Risk"
        elif score >= 70:
            return "High Risk"
        else:
            return "Very High Risk"