import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""

    # eBay API Settings
    EBAY_APP_ID = os.getenv('EBAY_APP_ID')
    EBAY_CERT_ID = os.getenv('EBAY_CERT_ID')
    EBAY_DEV_ID = os.getenv('EBAY_DEV_ID')
    EBAY_ENVIRONMENT = os.getenv('EBAY_ENVIRONMENT', 'production')

    # Application Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = True

    # File Paths
    JUNKYARD_PRICES_CSV = 'Junkyard Pricing.csv'
    SAVED_PARTS_DB = 'saved_parts.json'

    @staticmethod
    def validate():
        """Check if required configuration is set"""
        if not Config.EBAY_APP_ID:
            print("[WARNING] eBay API credentials not configured!")
            print("          Please copy .env.template to .env and add your credentials")
            return False
        return True
