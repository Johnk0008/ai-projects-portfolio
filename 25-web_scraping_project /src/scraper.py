import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from typing import List, Dict, Optional
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
import logging
import sys
import os

# Add the parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add compatibility fix for older numpy/pandas
try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None

try:
    from config import config
except ImportError:
    # Fallback if config module is not available
    class FallbackConfig:
        def get(self, key, default=None):
            return default
    config = FallbackConfig()

class AdvancedWebScraper:
    """
    Advanced web scraper with error handling, rate limiting, and respect for robots.txt
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.setup_logging()
        
        # Initialize UserAgent with fallback
        if UserAgent:
            self.ua = UserAgent()
        else:
            self.ua = None
            
        self.respect_robots_txt()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def respect_robots_txt(self):
        """Check robots.txt and respect crawling rules"""
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            self.robot_parser = RobotFileParser()
            self.robot_parser.set_url(robots_url)
            self.robot_parser.read()
            self.logger.info(f"Robots.txt loaded from {robots_url}")
        except Exception as e:
            self.logger.warning(f"Could not load robots.txt: {e}")
            self.robot_parser = None
    
    def can_fetch(self, url: str) -> bool:
        """Check if we're allowed to fetch the URL"""
        if self.robot_parser:
            return self.robot_parser.can_fetch("*", url)
        return True
    
    def get_random_delay(self) -> float:
        """Get random delay between requests to avoid being blocked"""
        base_delay = config.get('scraping.delay_between_requests', 1)
        return base_delay + random.uniform(0, 2)
    
    def get_headers(self):
        """Get request headers with fallback if UserAgent fails"""
        if self.ua:
            user_agent = self.ua.random
        else:
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            
        return {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def make_request(self, url: str, retry_count: int = 0) -> Optional[requests.Response]:
        """Make HTTP request with error handling and retry logic"""
        if not self.can_fetch(url):
            self.logger.warning(f"Not allowed to fetch {url} by robots.txt")
            return None
        
        max_retries = config.get('scraping.retry_attempts', 3)
        timeout = config.get('scraping.timeout', 30)
        
        headers = self.get_headers()
        
        try:
            time.sleep(self.get_random_delay())
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            self.logger.info(f"Successfully fetched {url}")
            return response
            
        except requests.exceptions.RequestException as e:
            if retry_count < max_retries:
                self.logger.warning(f"Request failed (attempt {retry_count + 1}/{max_retries}): {e}")
                time.sleep(2 ** retry_count)  # Exponential backoff
                return self.make_request(url, retry_count + 1)
            else:
                self.logger.error(f"Failed to fetch {url} after {max_retries} attempts: {e}")
                return None
    
    def scrape_books(self) -> List[Dict]:
        """Scrape book data from books.toscrape.com"""
        books_data = []
        page = 1
        has_next_page = True
        
        while has_next_page:
            if page == 1:
                url = f"{self.base_url}/index.html"
            else:
                url = f"{self.base_url}/catalogue/page-{page}.html"
            
            response = self.make_request(url)
            if not response:
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.select('article.product_pod')
            
            if not books:
                has_next_page = False
                break
            
            for book in books:
                book_info = self.extract_book_info(book)
                if book_info:
                    books_data.append(book_info)
            
            # Check for next page
            next_button = soup.select_one('li.next a')
            has_next_page = next_button is not None
            page += 1
            
            self.logger.info(f"Scraped page {page-1}, found {len(books)} books")
        
        return books_data
    
    def extract_book_info(self, book_element) -> Optional[Dict]:
        """Extract book information from HTML element"""
        try:
            title_element = book_element.select_one('h3 a')
            price_element = book_element.select_one('p.price_color')
            rating_element = book_element.select_one('p.star-rating')
            availability_element = book_element.select_one('p.availability')
            
            title = title_element['title'] if title_element and title_element.has_attr('title') else "N/A"
            price = price_element.text if price_element else "N/A"
            rating = rating_element['class'][1] if rating_element and len(rating_element.get('class', [])) > 1 else "N/A"
            availability = availability_element.text.strip() if availability_element else "N/A"
            
            return {
                'title': title,
                'price': price,
                'rating': rating,
                'availability': availability,
                'scraped_at': pd.Timestamp.now()
            }
        except Exception as e:
            self.logger.error(f"Error extracting book info: {e}")
            return None
    
    def scrape_quotes(self) -> List[Dict]:
        """Scrape quotes from quotes.toscrape.com"""
        quotes_data = []
        page = 1
        has_next_page = True
        
        while has_next_page:
            url = f"{self.base_url}/page/{page}/"
            response = self.make_request(url)
            
            if not response:
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            quotes = soup.select('div.quote')
            
            if not quotes:
                has_next_page = False
                break
            
            for quote in quotes:
                quote_info = self.extract_quote_info(quote)
                if quote_info:
                    quotes_data.append(quote_info)
            
            next_button = soup.select_one('li.next a')
            has_next_page = next_button is not None
            page += 1
            
            self.logger.info(f"Scraped page {page-1}, found {len(quotes)} quotes")
        
        return quotes_data
    
    def extract_quote_info(self, quote_element) -> Optional[Dict]:
        """Extract quote information from HTML element"""
        try:
            text_element = quote_element.select_one('span.text')
            author_element = quote_element.select_one('small.author')
            tags_elements = quote_element.select('div.tags a.tag')
            
            text = text_element.text if text_element else "N/A"
            author = author_element.text if author_element else "N/A"
            tags = [tag.text for tag in tags_elements] if tags_elements else []
            
            return {
                'text': text,
                'author': author,
                'tags': ', '.join(tags),
                'scraped_at': pd.Timestamp.now()
            }
        except Exception as e:
            self.logger.error(f"Error extracting quote info: {e}")
            return None