import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression
import os

class DataLoader:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def generate_sample_data(self):
        """Generate sample datasets for demonstration"""
        # Sales data
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
        sales_data = pd.DataFrame({
            'date': dates,
            'sales': np.random.normal(1000, 200, len(dates)).cumsum() + 
                    np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 500,
            'customers': np.random.poisson(50, len(dates)),
            'revenue': np.random.normal(5000, 1000, len(dates)),
            'product_category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books'], len(dates)),
            'region': np.random.choice(['North', 'South', 'East', 'West'], len(dates))
        })
        
        # Customer behavior data
        X, y = make_classification(n_samples=1000, n_features=4, n_redundant=0, 
                                 n_informative=4, n_clusters_per_class=1, random_state=42)
        customer_data = pd.DataFrame(X, columns=['age', 'income', 'browsing_time', 'pages_visited'])
        customer_data['churn'] = y
        customer_data['satisfaction_score'] = np.random.randint(1, 6, 1000)
        customer_data['purchase_frequency'] = np.random.poisson(3, 1000)
        
        # Save to CSV
        sales_data.to_csv(os.path.join(self.data_dir, 'sample_sales_data.csv'), index=False)
        customer_data.to_csv(os.path.join(self.data_dir, 'customer_behavior.csv'), index=False)
        
        return sales_data, customer_data
    
    def load_data(self):
        """Load existing data or generate if not exists"""
        try:
            sales_data = pd.read_csv(os.path.join(self.data_dir, 'sample_sales_data.csv'))
            customer_data = pd.read_csv(os.path.join(self.data_dir, 'customer_behavior.csv'))
        except FileNotFoundError:
            print("Generating sample data...")
            sales_data, customer_data = self.generate_sample_data()
        
        return sales_data, customer_data