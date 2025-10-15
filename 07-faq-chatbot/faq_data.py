import json
import os
import logging

logger = logging.getLogger(__name__)

class FAQData:
    def __init__(self, data_file='data/faqs.json'):
        self.data_file = data_file
        self.faqs = []
        self.load_data()
    
    def load_data(self):
        """Load FAQ data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.faqs = data.get('faqs', [])
                logger.info(f"Loaded {len(self.faqs)} FAQs from {self.data_file}")
            else:
                logger.warning(f"FAQ data file {self.data_file} not found. Using empty dataset.")
                self.faqs = []
        except Exception as e:
            logger.error(f"Error loading FAQ data: {e}")
            self.faqs = []
    
    def save_data(self):
        """Save FAQ data to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({'faqs': self.faqs}, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.faqs)} FAQs to {self.data_file}")
        except Exception as e:
            logger.error(f"Error saving FAQ data: {e}")
    
    def get_all_faqs(self):
        """Get all FAQs"""
        return self.faqs
    
    def get_faq_by_index(self, index):
        """Get FAQ by index"""
        if 0 <= index < len(self.faqs):
            return self.faqs[index]
        return None
    
    def add_faq(self, question, answer, category='general', tags=None):
        """Add new FAQ"""
        new_faq = {
            'question': question,
            'answer': answer,
            'category': category,
            'tags': tags or []
        }
        self.faqs.append(new_faq)
        self.save_data()
        return new_faq
    
    def search_faqs(self, query, search_in='both'):
        """Search FAQs by query"""
        query = query.lower()
        results = []
        
        for faq in self.faqs:
            match = False
            
            if search_in in ['question', 'both']:
                if query in faq['question'].lower():
                    match = True
            
            if search_in in ['answer', 'both'] and not match:
                if query in faq['answer'].lower():
                    match = True
            
            if search_in in ['tags', 'both'] and not match:
                for tag in faq.get('tags', []):
                    if query in tag.lower():
                        match = True
                        break
            
            if match:
                results.append(faq)
        
        return results