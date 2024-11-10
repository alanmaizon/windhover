from flask import Flask
from extensions import db
from config import Config

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
