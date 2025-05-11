import os
from datetime import timedelta

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost/irrigation_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API settings
    API_TITLE = 'Irrigation System API'
    API_VERSION = 'v1'
    
    # Device settings
    DEVICE_HEARTBEAT_TIMEOUT = timedelta(minutes=5)  # Consider device offline after 5 minutes of no updates
