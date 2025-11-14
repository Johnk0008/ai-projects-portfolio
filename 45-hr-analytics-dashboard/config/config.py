import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Data settings
    DATA_PATH = 'data/'
    MODEL_PATH = 'models/'
    
    # Analysis settings
    SAMPLE_SIZE = 1000
    FORECAST_MONTHS = 12
    GROWTH_RATE = 0.1
    
    # Dashboard settings
    DEBUG = True
    PORT = 8050
    HOST = 'localhost'