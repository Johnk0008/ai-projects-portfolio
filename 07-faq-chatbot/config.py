import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'faq-chatbot-secret-key-2024'
    DEBUG = True
    
    # NLP Settings
    SIMILARITY_THRESHOLD = 0.6
    MAX_RESPONSES = 3
    
    # Model Settings
    USE_SPACY = True
    TFIDF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}