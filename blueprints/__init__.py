from .base_route import base_bp
from .home_route import home_bp
from .books_route import books_bp
from .members_route import members_bp
from .borrow_route import borrow_bp


def register_blueprints(app):
    app.register_blueprint(base_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(borrow_bp)
