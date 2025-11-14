import os
import sys
import argparse

# Add current directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import requests
        from bs4 import BeautifulSoup
        import pandas as pd
        import yaml
        print("✓ All dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main function to run the web scraping project"""
    
    # First check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Now import the project modules
    try:
        from src.scraper import AdvancedWebScraper
        from src.data_processor import DataProcessor
        from config import config
        print("✓ Project modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import project modules: {e}")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Advanced Web Scraping Tool')
    parser.add_argument('--website', type=str, choices=['books', 'quotes'], 
                       default='books', help='Website to scrape')
    parser.add_argument('--output', type=str, default='csv', 
                       choices=['csv', 'json', 'excel'], help='Output format')
    parser.add_argument('--pages', type=int, default=1, 
                       help='Number of pages to scrape (for testing)')
    args = parser.parse_args()
    
    # Initialize components
    processor = DataProcessor()
    
    try:
        if args.website == 'books':
            print("Starting books scraping from http://books.toscrape.com...")
            scraper = AdvancedWebScraper('http://books.toscrape.com')
            data = scraper.scrape_books()
            filename = 'books_data'
        else:
            print("Starting quotes scraping from http://quotes.toscrape.com...")
            scraper = AdvancedWebScraper('http://quotes.toscrape.com')
            data = scraper.scrape_quotes()
            filename = 'quotes_data'
        
        if data:
            # Clean and save data
            cleaned_data = processor.clean_data(data)
            filepath = processor.save_data(cleaned_data, filename, args.output)
            
            # Analyze data
            analysis = processor.analyze_data(cleaned_data)
            
            print(f"\n=== Scraping Completed ===")
            print(f"Total records scraped: {len(cleaned_data)}")
            print(f"Data saved to: {filepath}")
            print(f"\n=== Data Summary ===")
            print(f"Columns: {analysis['columns']}")
            print(f"Total records: {analysis['total_records']}")
            
        else:
            print("No data was scraped. This could be due to:")
            print("- Website being unavailable")
            print("- Network connectivity issues")
            print("- Changes in website structure")
            
    except Exception as e:
        print(f"Error during scraping: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()