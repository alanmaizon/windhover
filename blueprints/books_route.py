import matplotlib
matplotlib.use('Agg')
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import func
import matplotlib.pyplot as plt
import io
import os
from extensions import db
from models import Book, Member, Borrowing
from config import Config
from icons import load_icons

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

books_bp = Blueprint('books_bp', __name__)

@books_bp.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        pub_year = request.form['publicationyear']

        # Handle the image file upload
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'book_covers', filename))
            img_path = os.path.join('images/book_covers', filename).replace("\\", "/")
        else:
            img_path = None

        # Create a new Book record
        new_book = Book(
            isbn=isbn,
            title=title,
            author=author,
            publisher=publisher,
            publicationyear=pub_year,
            imagepath=img_path
        )

        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')

    # Define default sort options
    sort_by = request.args.get('sortby', 'title')
    sort_order = request.args.get('order', 'asc')
    selected_publishers = request.args.getlist('publishers')

    allowed_sort_columns = ['title', 'author', 'publisher', 'publicationyear']
    if sort_by not in allowed_sort_columns:
        sort_by = 'title'
    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'

    # Build query with optional publisher filtering
    query = Book.query.filter(Book.deleted == False)
    if selected_publishers:
        query = query.filter(Book.publisher.in_(selected_publishers))

    books = query.order_by(db.text(f'{sort_by} {sort_order}')).all()
    current_year = datetime.now().year

    # Retrieve publishers from the database
    publishers = [g[0] for g in db.session.query(Book.publisher).filter(Book.deleted == False).distinct()]
    
    # Sort publishers alphabetically
    publishers.sort()

    return render_template(
        'books.html',
        books=books,
        current_year=current_year,
        sort_by=sort_by,
        sort_order=sort_order,
        publishers=publishers,
        selected_publishers=selected_publishers
    )

@books_bp.route('/books/edit_book/<int:bookid>', methods=['POST'])
def edit_book(bookid):
    book = Book.query.get_or_404(bookid)
    book.title = request.form['title']
    book.author = request.form['author']
    book.publisher = request.form['publisher']
    book.publicationyear = request.form['publicationyear']
    db.session.commit()
    flash("Book details updated successfully!", "success")
    return redirect(url_for('books_bp.books'))


@books_bp.route('/books/delete_book/<int:bookid>', methods=['POST'])
def delete_book(bookid):
    book = Book.query.get_or_404(bookid)
    book.deleted = True
    db.session.commit()
    flash("Book deleted successfully!", "success")
    return redirect(url_for('books_bp.books'))
