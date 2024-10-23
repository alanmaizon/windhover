from flask import Blueprint
from routes.books import books_bp
from routes.members import members_bp
from routes.borrowing import borrowing_bp

def init_routes(app):
    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(borrowing_bp)
