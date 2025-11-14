import nltk
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class NLPProcessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(max_features=3000, lowercase=True, analyzer='word')
        self.is_fitted = False
        
    def preprocess_text(self, text):
        """Clean and preprocess input text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        # Tokenize
        tokens = nltk.word_tokenize(text)
        
        # Remove stopwords and stem
        processed_tokens = [
            self.stemmer.stem(token) 
            for token in tokens 
            if token not in self.stop_words and len(token) > 2
        ]
        
        return ' '.join(processed_tokens)
    
    def fit_vectorizer(self, texts):
        """Fit TF-IDF vectorizer on training data"""
        processed_texts = [self.preprocess_text(text) for text in texts]
        self.vectorizer.fit(processed_texts)
        self.is_fitted = True
    
    def transform_text(self, text):
        """Transform text to TF-IDF features"""
        if not self.is_fitted:
            raise ValueError("Vectorizer not fitted. Call fit_vectorizer first.")
        
        processed_text = self.preprocess_text(text)
        return self.vectorizer.transform([processed_text])