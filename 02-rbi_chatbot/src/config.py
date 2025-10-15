# src/config.py - NO external dependencies
import os

class Config:
    # REPLACE WITH YOUR ACTUAL GOOGLE API KEY
    GOOGLE_API_KEY = GOOGLE_API_KEY  # ← PUT YOUR REAL KEY HERE
    
    # Data URLs
    PDF_URL = "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/106MDNBFCS1910202343073E3EF57A4916AA5042911CD8D562.PDF"
    
    # Model Configuration
    MODEL_NAME = "gemini-1.5-flash"  # This model works for everyone
    TEMPERATURE = 0.1