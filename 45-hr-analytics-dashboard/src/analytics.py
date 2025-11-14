import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class HRAnalytics:
    def __init__(self, df):
        self.df = df
        self.scaler = StandardScaler()
    
    def satisfaction_analysis(self):
        """Analyze employee satisfaction factors"""
        satisfaction_corr = self.df[['satisfaction_score', 'salary', 'tenure_months', 
                                   'performance_rating', 'overtime_hours', 'training_hours']].corr()
        
        dept_satisfaction = self.df.groupby('department')['satisfaction_score'].mean().sort_values(ascending=False)
        position_satisfaction = self.df.groupby('position')['satisfaction_score'].mean().sort_values(ascending=False)
        
        return {
            'satisfaction_correlation': satisfaction_corr['satisfaction_score'].to_dict(),
            'department_satisfaction': dept_satisfaction.to_dict(),
            'position_satisfaction': position_satisfaction.to_dict()
        }
    
    def performance_analysis(self):
        """Analyze performance data"""
        performance_by_dept = self.df.groupby('department')['performance_rating'].mean()
        performance_by_position = self.df.groupby('position')['performance_rating'].mean()
        
        high_performers = self.df[self.df['performance_rating'] >= 4]
        low_performers = self.df[self.df['performance_rating'] <= 2]
        
        return {
            'performance_by_department': performance_by_dept.to_dict(),
            'performance_by_position': performance_by_position.to_dict(),
            'high_performer_count': len(high_performers),
            'low_performer_count': len(low_performers),
            'high_performer_characteristics': {
                'avg_salary': high_performers['salary'].mean(),
                'avg_satisfaction': high_performers['satisfaction_score'].mean(),
                'avg_training_hours': high_performers['training_hours'].mean()
            }
        }
    
    def employee_segmentation(self):
        """Segment employees using clustering"""
        features = ['salary', 'satisfaction_score', 'performance_rating', 'tenure_months']
        X = self.df[features].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=4, random_state=42)
        segments = kmeans.fit_predict(X_scaled)
        
        self.df['segment'] = segments
        segment_profiles = self.df.groupby('segment')[features].mean()
        
        return {
            'segments': segments.tolist(),
            'segment_profiles': segment_profiles.to_dict('index'),
            'segment_distribution': pd.Series(segments).value_counts().to_dict()
        }