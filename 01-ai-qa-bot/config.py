# config.py
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the AI Q&A Bot"""
    
    # API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
    HF_API_KEY = os.getenv('HF_API_KEY', 'your-huggingface-key-here')
    
    # Model Configuration
    DEFAULT_MODEL = "gpt-3.5-turbo"
    HF_MODEL = "microsoft/DialoGPT-large"
    
    # App Configuration
    MAX_HISTORY = 10
    TIMEOUT = 30
    
    @classmethod
    def validate_config(cls):
        """Validate that required environment variables are set"""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == 'your-api-key-here':
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return True

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)