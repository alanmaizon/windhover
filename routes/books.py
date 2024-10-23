from flask import Blueprint, request, render_template, flash
from app import db
from models import Book
from werkzeug.utils import secure_filename
from datetime import datetime
import os

books_bp = Blueprint('books_bp', __name__)

@books_bp.route('/books', methods=('GET', 'POST'))
def books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        pub_year = request.form['publicationyear']

        # Handle the image file upload
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/")
            img_path = img_path.replace("static/", "")
        else:
            img_path = None

        # Create a new Book record
        new_book = Book(title=title, author=author, genre=genre, publicationyear=pub_year, imagepath=img_path)
        db.session.add(new_book)
        db.session.commit()

    # Fetch sorting options safely
    sort_by = request.args.get('sortby', 'title')
    sort_order = request.args.get('order', 'asc')

    # Whitelist sort options
    allowed_sort_columns = ['title', 'author', 'genre', 'publicationyear']
    if sort_by not in allowed_sort_columns:
        sort_by = 'title'
    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'

    # Query books with sorting
    books = Book.query.order_by(db.text(f'{sort_by} {sort_order}')).all()

    current_year = datetime.now().year
    return render_template('books.html', books=books, current_year=current_year, sort_by=sort_by, sort_order=sort_order)
