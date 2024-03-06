# app/__init__.py

from flask import Flask

app = Flask(__name__)

# Import routes or other components
from app.routes import api

# Additional initialization or configuration code