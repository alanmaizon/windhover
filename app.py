from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import init_routes  # Import the routes initialization function
from config import Config

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database and migration tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
