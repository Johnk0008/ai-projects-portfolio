import yaml
import os
from typing import Dict, Any

class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                self.data = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Config file {self.config_path} not found. Using default settings.")
            self.data = {
                'scraping': {
                    'timeout': 30,
                    'retry_attempts': 3,
                    'delay_between_requests': 1,
                    'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                'websites': {
                    'example_books': {
                        'url': "http://books.toscrape.com",
                        'selectors': {
                            'product_container': "article.product_pod",
                            'title': "h3 a",
                            'price': "p.price_color",
                            'rating': "p.star-rating",
                            'availability': "p.availability"
                        }
                    },
                    'example_quotes': {
                        'url': "http://quotes.toscrape.com",
                        'selectors': {
                            'quote_container': "div.quote",
                            'text': "span.text",
                            'author': "small.author",
                            'tags': "div.tags a.tag"
                        }
                    }
                },
                'data_processing': {
                    'output_format': "csv",
                    'encoding': "utf-8",
                    'save_raw_html': False
                }
            }
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

# Global configuration instance
config = Config()