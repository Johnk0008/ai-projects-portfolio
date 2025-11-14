import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
from config import *

class FeatureEngineer:
    def __init__(self):
        self.preprocessor = None
        self.feature_names = None
        
    def create_features(self, df):
        """Create new features from existing ones"""
        df = df.copy()
        
        # Financial ratios
        df['income_to_loan_ratio'] = df['income'] / df['loan_amount']
        df['monthly_debt_burden'] = df['debt_to_income'] * df['income'] / 100
        df['accounts_per_year'] = df['number_of_accounts'] / (df['age'] - 18).clip(1)
        
        # Payment behavior features
        df['has_late_payments'] = (df['payment_history'] > 0).astype(int)
        df['severe_late_payments'] = (df['payment_history'] > 3).astype(int)
        
        # Age groups
        df['age_group'] = pd.cut(df['age'], bins=BIN_RANGES['age'], 
                               labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
        
        # Income groups
        df['income_group'] = pd.cut(df['income'], bins=BIN_RANGES['income'],
                                  labels=['Low', 'Medium', 'High', 'Very High'])
        
        # Credit utilization categories
        df['utilization_category'] = pd.cut(df['credit_utilization'], 
                                          bins=[0, 30, 70, 100],
                                          labels=['Low', 'Medium', 'High'])
        
        return df
    
    def fit_preprocessor(self, X_train):
        """Fit the preprocessing pipeline"""
        # Separate numerical and categorical features
        numerical_features = X_train.select_dtypes(include=[np.number]).columns.tolist()
        categorical_features = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Preprocessing pipelines
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        # Combine preprocessing steps
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        
        # Fit the preprocessor
        self.preprocessor.fit(X_train)
        
        # Get feature names after one-hot encoding
        feature_names = numerical_features.copy()
        cat_encoder = self.preprocessor.named_transformers_['cat'].named_steps['onehot']
        cat_features = cat_encoder.get_feature_names_out(categorical_features)
        feature_names.extend(cat_features)
        
        self.feature_names = feature_names
        
        return self
    
    def transform_features(self, X):
        """Transform features using fitted preprocessor"""
        if self.preprocessor is None:
            raise ValueError("Preprocessor not fitted. Call fit_preprocessor first.")
        
        X_transformed = self.preprocessor.transform(X)
        return pd.DataFrame(X_transformed, columns=self.feature_names, index=X.index)
    
    def save_preprocessor(self, file_path):
        """Save the fitted preprocessor"""
        if self.preprocessor is None:
            raise ValueError("No preprocessor to save")
        joblib.dump(self.preprocessor, file_path)
    
    def load_preprocessor(self, file_path):
        """Load a fitted preprocessor"""
        self.preprocessor = joblib.load(file_path)
        return self