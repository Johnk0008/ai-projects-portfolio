import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, mean_absolute_error, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

class HRPredictiveModels:
    def __init__(self, df):
        self.df = df
        self.models = {}
        self.encoders = {}
    
    def prepare_attrition_data(self):
        """Prepare data for attrition prediction"""
        df_encoded = self.df.copy()
        
        # Encode categorical variables
        categorical_cols = ['department', 'position', 'recruitment_source']
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[col + '_encoded'] = le.fit_transform(df_encoded[col])
            self.encoders[col] = le
        
        features = ['department_encoded', 'position_encoded', 'salary', 'tenure_months',
                   'satisfaction_score', 'performance_rating', 'overtime_hours',
                   'training_hours', 'projects_completed']
        
        X = df_encoded[features]
        y = df_encoded['attrition']
        
        return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    def train_attrition_model(self):
        """Train model to predict employee attrition"""
        X_train, X_test, y_train, y_test = self.prepare_attrition_data()
        
        # Random Forest for attrition prediction
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        # Logistic Regression for interpretability
        lr_model = LogisticRegression(random_state=42)
        lr_model.fit(X_train, y_train)
        
        # Evaluate models
        rf_predictions = rf_model.predict(X_test)
        lr_predictions = lr_model.predict(X_test)
        
        rf_accuracy = accuracy_score(y_test, rf_predictions)
        lr_accuracy = accuracy_score(y_test, lr_predictions)
        
        self.models['attrition_rf'] = rf_model
        self.models['attrition_lr'] = lr_model
        
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return {
            'random_forest_accuracy': rf_accuracy,
            'logistic_regression_accuracy': lr_accuracy,
            'feature_importance': feature_importance.to_dict('records'),
            'classification_report': classification_report(y_test, rf_predictions, output_dict=True)
        }
    
    def forecast_hiring_needs(self, growth_rate=0.1, forecast_months=12):
        """Forecast hiring needs based on growth and attrition"""
        current_headcount = len(self.df)
        monthly_attrition_rate = self.df['attrition'].mean() / 12
        
        # Calculate expected attrition
        expected_attrition = current_headcount * monthly_attrition_rate * forecast_months
        
        # Calculate growth needs
        growth_needs = current_headcount * growth_rate
        
        total_hiring_needs = expected_attrition + growth_needs
        
        # Department-wise breakdown
        dept_attrition = self.df.groupby('department')['attrition'].mean()
        dept_headcount = self.df['department'].value_counts()
        
        dept_hiring_needs = {}
        for dept in dept_attrition.index:
            dept_needs = (dept_headcount[dept] * dept_attrition[dept] * forecast_months + 
                         dept_headcount[dept] * growth_rate / len(dept_attrition))
            dept_hiring_needs[dept] = int(dept_needs)
        
        return {
            'total_hiring_needs': int(total_hiring_needs),
            'expected_attrition': int(expected_attrition),
            'growth_needs': int(growth_needs),
            'department_hiring_needs': dept_hiring_needs,
            'forecast_period': forecast_months
        }
    
    def save_models(self, path='models/'):
        """Save trained models"""
        import os
        os.makedirs(path, exist_ok=True)
        
        for name, model in self.models.items():
            joblib.dump(model, f'{path}/{name}.joblib')
        
        joblib.dump(self.encoders, f'{path}/encoders.joblib')