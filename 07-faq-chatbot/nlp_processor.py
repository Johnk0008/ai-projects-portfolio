import nltk
import spacy
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

logger = logging.getLogger(__name__)

class NLPProcessor:
    def __init__(self, use_spacy=True):
        self.use_spacy = use_spacy
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize spaCy if enabled
        if self.use_spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("spaCy model loaded successfully")
            except OSError:
                logger.warning("spaCy model not found. Please install it using: python -m spacy download en_core_web_sm")
                self.use_spacy = False
        
        # Initialize TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=1,
            max_df=0.8,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.is_fitted = False
    
    def preprocess_text(self, text):
        """Preprocess text by cleaning, tokenizing, and normalizing"""
        if not text or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        if self.use_spacy:
            return self._preprocess_with_spacy(text)
        else:
            return self._preprocess_with_nltk(text)
    
    def _preprocess_with_spacy(self, text):
        """Preprocess text using spaCy"""
        doc = self.nlp(text)
        
        # Extract tokens: lemmatize, remove stopwords and punctuation
        tokens = [
            token.lemma_.lower() for token in doc 
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        
        return ' '.join(tokens)
    
    def _preprocess_with_nltk(self, text):
        """Preprocess text using NLTK"""
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and punctuation, then stem
        processed_tokens = [
            self.stemmer.stem(token) for token in tokens 
            if token not in self.stop_words and token not in string.punctuation
        ]
        
        return ' '.join(processed_tokens)
    
    def fit_vectorizer(self, texts):
        """Fit TF-IDF vectorizer with preprocessed texts"""
        try:
            preprocessed_texts = [self.preprocess_text(text) for text in texts]
            self.vectorizer.fit(preprocessed_texts)
            self.is_fitted = True
            logger.info("TF-IDF vectorizer fitted successfully")
        except Exception as e:
            logger.error(f"Error fitting vectorizer: {e}")
    
    def transform_text(self, text):
        """Transform text to TF-IDF vector"""
        if not self.is_fitted:
            raise ValueError("Vectorizer not fitted. Call fit_vectorizer first.")
        
        preprocessed_text = self.preprocess_text(text)
        return self.vectorizer.transform([preprocessed_text])
    
    def calculate_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        if vec1.shape[1] != vec2.shape[1]:
            raise ValueError("Vectors must have the same dimensions")
        
        # Convert to arrays for cosine similarity calculation
        arr1 = vec1.toarray().flatten()
        arr2 = vec2.toarray().flatten()
        
        # Calculate cosine similarity
        dot_product = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def extract_keywords(self, text, top_n=5):
        """Extract top keywords from text"""
        preprocessed_text = self.preprocess_text(text)
        tokens = preprocessed_text.split()
        
        # Count frequency
        from collections import Counter
        word_freq = Counter(tokens)
        
        return word_freq.most_common(top_n)