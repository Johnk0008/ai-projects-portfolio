import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os
from config import *

class DataProcessor:
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        
    def generate_sample_data(self, n_samples=10000):
        """Generate synthetic credit scoring data for demonstration"""
        np.random.seed(RANDOM_STATE)
        
        data = {
            'age': np.random.randint(18, 70, n_samples),
            'income': np.random.normal(50000, 20000, n_samples).clip(10000, 150000),
            'employment_length': np.random.exponential(5, n_samples).clip(0, 40),
            'debt_to_income': np.random.beta(2, 5, n_samples) * 100,
            'credit_utilization': np.random.beta(3, 3, n_samples) * 100,
            'payment_history': np.random.randint(0, 13, n_samples),  # Months of late payments
            'number_of_accounts': np.random.poisson(8, n_samples).clip(1, 20),
            'loan_amount': np.random.normal(25000, 15000, n_samples).clip(1000, 100000),
            'loan_term': np.random.choice([12, 24, 36, 48, 60], n_samples),
            'home_ownership': np.random.choice(['RENT', 'MORTGAGE', 'OWN'], n_samples),
            'purpose': np.random.choice(['DEBT_CONSOLIDATION', 'HOME_IMPROVEMENT', 
                                       'BUSINESS', 'PERSONAL', 'EDUCATION'], n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create target variable based on features
        default_prob = (
            df['debt_to_income'] * 0.3 +
            df['payment_history'] * 0.4 +
            (100 - df['income']/1500) * 0.2 +
            np.random.normal(0, 10, n_samples)
        )
        df['credit_score'] = (default_prob > 50).astype(int)
        
        return df
    
    def load_data(self, file_path=None):
        """Load data from file or generate sample data"""
        if file_path and os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            print("Generating sample data...")
            df = self.generate_sample_data()
            # Save sample data for reference
            df.to_csv(RAW_DATA_DIR / "sample_credit_data.csv", index=False)
        
        return df
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        # Numerical columns - fill with median
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
        
        # Categorical columns - fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
        
        return df
    
    def split_data(self, df, target_col='credit_score'):
        """Split data into train, validation, and test sets"""
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # First split: separate test set
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )
        
        # Second split: separate validation set from temp
        val_size = VALIDATION_SIZE / (1 - TEST_SIZE)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size, random_state=RANDOM_STATE, stratify=y_temp
        )
        
        return X_train, X_val, X_test, y_train, y_val, y_test