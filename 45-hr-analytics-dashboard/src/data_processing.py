import pandas as pd
import numpy as np
from datetime import datetime
import os

class HRDataProcessor:
    def __init__(self):
        self.df = None
        
    def generate_sample_data(self, n_employees=1000):
        """Generate synthetic HR data for demonstration"""
        np.random.seed(42)
        
        departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
        positions = ['Junior', 'Mid-Level', 'Senior', 'Manager', 'Director']
        performance_ratings = [1, 2, 3, 4, 5]
        
        data = {
            'employee_id': range(1, n_employees + 1),
            'department': np.random.choice(departments, n_employees),
            'position': np.random.choice(positions, n_employees),
            'salary': np.random.normal(75000, 25000, n_employees).astype(int),
            'tenure': np.random.exponential(5, n_employees).astype(int),
            'performance_rating': np.random.choice(performance_ratings, n_employees, p=[0.1, 0.2, 0.4, 0.2, 0.1]),
            'satisfaction_score': np.random.uniform(1, 5, n_employees),
            'overtime_hours': np.random.poisson(5, n_employees),
            'projects_completed': np.random.poisson(8, n_employees),
            'training_hours': np.random.normal(20, 5, n_employees).astype(int),
            'recruitment_source': np.random.choice(['LinkedIn', 'Referral', 'Campus', 'Agency', 'Website'], n_employees),
            'hire_date': pd.date_range('2015-01-01', periods=n_employees, freq='D').tolist(),
            'attrition': np.random.choice([0, 1], n_employees, p=[0.85, 0.15])
        }
        
        self.df = pd.DataFrame(data)
        self.df['hire_date'] = pd.to_datetime(self.df['hire_date'])
        self.df['current_date'] = datetime.now()
        self.df['tenure_months'] = ((self.df['current_date'] - self.df['hire_date']).dt.days / 30).astype(int)
        
        return self.df
    
    def calculate_recruitment_metrics(self):
        """Calculate key recruitment metrics"""
        recruitment_metrics = {
            'time_to_fill': self.df.groupby('department')['hire_date'].count().to_dict(),
            'source_effectiveness': self.df['recruitment_source'].value_counts().to_dict(),
            'department_hires': self.df['department'].value_counts().to_dict()
        }
        return recruitment_metrics
    
    def calculate_turnover_metrics(self):
        """Calculate turnover metrics"""
        turnover_by_dept = self.df.groupby('department')['attrition'].mean() * 100
        turnover_by_position = self.df.groupby('position')['attrition'].mean() * 100
        
        return {
            'overall_turnover_rate': self.df['attrition'].mean() * 100,
            'turnover_by_department': turnover_by_dept.to_dict(),
            'turnover_by_position': turnover_by_position.to_dict(),
            'avg_tenure_leavers': self.df[self.df['attrition'] == 1]['tenure_months'].mean()
        }