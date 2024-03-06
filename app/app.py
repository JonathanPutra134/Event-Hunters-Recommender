# app/app.py

from flask import Flask
from app.extensions import db
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

if __name__ == '__main__':
    app.run()
