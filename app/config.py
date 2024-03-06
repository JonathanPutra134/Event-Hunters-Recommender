# app/config.py

import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add other configuration settings as needed