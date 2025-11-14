import unittest
from src.scraper import AdvancedWebScraper
from src.data_processor import DataProcessor

class TestWebScraper(unittest.TestCase):
    
    def setUp(self):
        self.scraper = AdvancedWebScraper('http://books.toscrape.com')
        self.processor = DataProcessor()
    
    def test_scraper_initialization(self):
        self.assertIsNotNone(self.scraper.session)
        self.assertIsNotNone(self.scraper.ua)
    
    def test_data_processor_initialization(self):
        self.assertEqual(self.processor.output_dir, "data")
    
    def test_make_request(self):
        response = self.scraper.make_request('http://httpbin.org/status/200')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()