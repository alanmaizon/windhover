from flask import Flask
from extensions import db
from config import Config
from blueprints import register_blueprints
from filters import format_date


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    register_blueprints(app)

    # Load environmental filter for date format
    app.jinja_env.filters['format_date'] = format_date
    
    return app