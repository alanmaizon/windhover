from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
