from flask import Flask
from extensions import db
from config import Config
from blueprints.routes import route_bp
from filters import format_date


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(route_bp)

    # Load environmental filter for date format
    app.jinja_env.filters['format_date'] = format_date
    
    return app