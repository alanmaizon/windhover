from flask import Blueprint, render_template
from datetime import datetime
from extensions import db
from models import Book, Member, Borrowing
from config import Config

home_bp = Blueprint('home_bp', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@home_bp.route('/')
def home():
    # Query the totals from the database
    total_books = db.session.query(Book).count()
    total_members = db.session.query(Member).count()
    total_borrowed = db.session.query(Borrowing).count()

    # Fetch recommended books (published from 2020 to the current year)
    current_year = datetime.now().year
    recommended_books = Book.query.filter(Book.deleted == False).filter(Book.publicationyear >= 2020).order_by(Book.publicationyear.desc()).all()
    
    # Pass the totals to the template
    return render_template(
        'home.html', 
        total_books=total_books, 
        total_members=total_members, 
        total_borrowed=total_borrowed,
        books=recommended_books,
        current_year=current_year,
    )