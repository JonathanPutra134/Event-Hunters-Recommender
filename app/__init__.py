from flask import Flask
from app.db import init_db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)  # Call init_db to initialize the db instance

from app.routes import api  # Import routes after db is defined