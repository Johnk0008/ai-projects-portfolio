import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///url_shortener_advanced.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Rate limiting
    RATE_LIMIT_STORAGE_URL = 'memory://'
    
    # Analytics
    ANALYTICS_RETENTION_DAYS = 30