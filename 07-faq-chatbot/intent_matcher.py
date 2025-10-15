import numpy as np
import logging
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import os

logger = logging.getLogger(__name__)

class IntentMatcher:
    def __init__(self, nlp_processor, similarity_threshold=0.6):
        self.nlp_processor = nlp_processor
        self.similarity_threshold = similarity_threshold
        self.faqs = []
        self.faq_questions = []
        self.faq_vectors = None
        
    def load_faqs(self, faq_data):
        """Load FAQ data and prepare for matching"""
        self.faqs = faq_data
        self.faq_questions = [faq['question'] for faq in faq_data]
        
        # Fit vectorizer and transform FAQ questions
        self.nlp_processor.fit_vectorizer(self.faq_questions)
        
        # Precompute vectors for all FAQ questions
        self.faq_vectors = []
        for question in self.faq_questions:
            vector = self.nlp_processor.transform_text(question)
            self.faq_vectors.append(vector)
        
        logger.info(f"Loaded {len(self.faqs)} FAQs for intent matching")
    
    def find_best_match(self, user_question, top_k=3):
        """Find the best matching FAQ for user question"""
        if not self.faq_vectors:
            raise ValueError("FAQs not loaded. Call load_faqs first.")
        
        try:
            # Preprocess and vectorize user question
            user_vector = self.nlp_processor.transform_text(user_question)
            
            similarities = []
            
            # Calculate similarity with each FAQ
            for i, faq_vector in enumerate(self.faq_vectors):
                similarity = self.nlp_processor.calculate_similarity(user_vector, faq_vector)
                similarities.append((i, similarity))
            
            # Sort by similarity score (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Filter by threshold and get top matches
            filtered_matches = [
                (idx, score) for idx, score in similarities 
                if score >= self.similarity_threshold
            ][:top_k]
            
            results = []
            for idx, score in filtered_matches:
                results.append({
                    'question': self.faqs[idx]['question'],
                    'answer': self.faqs[idx]['answer'],
                    'category': self.faqs[idx].get('category', 'general'),
                    'similarity_score': round(score, 3),
                    'confidence': 'high' if score > 0.8 else 'medium' if score > 0.6 else 'low'
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error finding best match: {e}")
            return []
    
    def get_faq_categories(self):
        """Get unique FAQ categories"""
        categories = set()
        for faq in self.faqs:
            categories.add(faq.get('category', 'general'))
        return sorted(list(categories))
    
    def get_faqs_by_category(self, category):
        """Get FAQs by specific category"""
        return [faq for faq in self.faqs if faq.get('category') == category]
    
    def add_faq(self, question, answer, category='general', tags=None):
        """Add new FAQ to the system"""
        new_faq = {
            'question': question,
            'answer': answer,
            'category': category,
            'tags': tags or []
        }
        
        self.faqs.append(new_faq)
        self.faq_questions.append(question)
        
        # Update vectors
        new_vector = self.nlp_processor.transform_text(question)
        self.faq_vectors.append(new_vector)
        
        logger.info(f"Added new FAQ: {question}")