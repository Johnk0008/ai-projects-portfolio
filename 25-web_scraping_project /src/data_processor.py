import pandas as pd
import json
import csv
import os
from typing import List, Dict, Union
import logging
from datetime import datetime
import sys

# Add the parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import config
except ImportError:
    # Fallback if config module is not available
    class FallbackConfig:
        def get(self, key, default=None):
            return default
    config = FallbackConfig()

class DataProcessor:
    """
    Process and save scraped data in various formats
    """
    
    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        self.setup_directories()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """Create necessary directories"""
        os.makedirs(os.path.join(self.output_dir, "raw"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "processed"), exist_ok=True)
    
    def save_data(self, data: List[Dict], filename: str, format_type: str = None) -> str:
        """
        Save data in specified format
        
        Args:
            data: List of dictionaries containing the data
            filename: Output filename (without extension)
            format_type: Output format ('csv', 'json', 'excel')
        
        Returns:
            Path to the saved file
        """
        if not format_type:
            format_type = config.get('data_processing.output_format', 'csv')
        
        # Use simple timestamp instead of pandas for compatibility
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in data:
            if 'scraped_at' in item:
                item['scraped_at'] = timestamp
        
        df = pd.DataFrame(data)
        
        if format_type.lower() == 'csv':
            filepath = os.path.join(self.output_dir, "processed", f"{filename}.csv")
            df.to_csv(filepath, index=False, encoding='utf-8')
        
        elif format_type.lower() == 'json':
            filepath = os.path.join(self.output_dir, "processed", f"{filename}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        elif format_type.lower() == 'excel':
            filepath = os.path.join(self.output_dir, "processed", f"{filename}.xlsx")
            df.to_excel(filepath, index=False)
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        
        self.logger.info(f"Data saved to {filepath} with {len(data)} records")
        return filepath
    
    def clean_data(self, data: List[Dict]) -> List[Dict]:
        """
        Clean and preprocess the data
        
        Args:
            data: List of dictionaries
        
        Returns:
            Cleaned list of dictionaries
        """
        if not data:
            return []
        
        # Remove duplicates based on all fields
        seen = set()
        cleaned_data = []
        
        for item in data:
            # Convert dict to tuple for hashing
            item_tuple = tuple(sorted(item.items()))
            if item_tuple not in seen:
                seen.add(item_tuple)
                cleaned_data.append(item)
        
        # Handle missing values
        for item in cleaned_data:
            for key in item:
                if item[key] is None:
                    item[key] = ''
                elif isinstance(item[key], str):
                    item[key] = item[key].strip()
        
        self.logger.info(f"Data cleaned: {len(data)} -> {len(cleaned_data)} records")
        return cleaned_data
    
    def analyze_data(self, data: List[Dict]) -> Dict:
        """
        Perform basic data analysis
        
        Args:
            data: List of dictionaries
        
        Returns:
            Dictionary with analysis results
        """
        if not data:
            return {'error': 'No data available for analysis'}
        
        df = pd.DataFrame(data)
        
        analysis = {
            'total_records': len(df),
            'columns': list(df.columns),
            'data_types': {col: str(type(df[col].iloc[0])) for col in df.columns},
            'missing_values': {col: df[col].isnull().sum() for col in df.columns},
        }
        
        return analysis