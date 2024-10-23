from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import math

app = Flask(__name__)

# Set secret key for session management and CSRF protection
app.config['SECRET_KEY'] = 'your_secret_key'

# SQLAlchemy Database URI using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('RDS_USERNAME')}:{os.getenv('RDS_PASSWORD')}@{os.getenv('RDS_HOST')}/{os.getenv('RDS_DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/images')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB limit by default

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Models
class Book(db.Model):
    __tablename__ = 'books'
    bookid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    publicationyear = db.Column(db.Integer, nullable=False)
    imagepath = db.Column(db.String(255), nullable=True)
    available = db.Column(db.Boolean, default=True)

class Member(db.Model):
    __tablename__ = 'members'
    memberid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    joindate = db.Column(db.Date, nullable=False)
    profilepicture = db.Column(db.String(255), nullable=True)

class Borrowing(db.Model):
    __tablename__ = 'borrowing'
    borrowid = db.Column(db.Integer, primary_key=True)
    memberid = db.Column(db.Integer, db.ForeignKey('members.memberid'), nullable=False)
    bookid = db.Column(db.Integer, db.ForeignKey('books.bookid'), nullable=False)
    borrowdate = db.Column(db.Date, nullable=False)
    duedate = db.Column(db.Date, nullable=False)
    returndate = db.Column(db.Date, nullable=True)

    member = db.relationship('Member', backref=db.backref('borrowings', lazy=True))
    book = db.relationship('Book', backref=db.backref('borrowings', lazy=True))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/books', methods=('GET', 'POST'))
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

    # Render the books page
    current_year = datetime.now().year
    return render_template('books.html', books=books, current_year=current_year, sort_by=sort_by, sort_order=sort_order)

@app.route('/members', methods=['GET', 'POST'])
def members_page():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        joindate = datetime.now().date()

        # Handle the image file upload
        file = request.files['profilepicture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics', filename))
            img_path = os.path.join('images/profile_pics', filename).replace("\\", "/")
        else:
            img_path = None

        # Create a new member
        new_member = Member(firstname=firstname, lastname=lastname, email=email, joindate=joindate, profilepicture=img_path)
        db.session.add(new_member)
        db.session.commit()

    # Handle sorting and searching
    sort_by = request.args.get('sortby', 'lastname')
    sort_order = request.args.get('order', 'asc')
    search_query = request.args.get('search', '')

    # Search members and sort results
    members = Member.query.filter(
        (Member.firstname.ilike(f'%{search_query}%')) | 
        (Member.lastname.ilike(f'%{search_query}%'))
    ).order_by(db.text(f'{sort_by} {sort_order}')).all()

    return render_template('members.html', members=members, sort_by=sort_by, sort_order=sort_order, search_query=search_query)

@app.route('/borrowing', methods=['GET', 'POST'])
def manage_borrowing():
    if request.method == 'POST':
        member_id = request.form['memberid']
        book_id = request.form['bookid']

        # Check if book is available
        book = Book.query.filter_by(bookid=book_id).first()
        if book and book.available:
            borrow_date = datetime.now().date()
            due_date = borrow_date + timedelta(days=30)

            # Create a new borrowing record
            borrowing = Borrowing(memberid=member_id, bookid=book_id, borrowdate=borrow_date, duedate=due_date)
            book.available = False  # Mark the book as unavailable
            db.session.add(borrowing)
            db.session.commit()
            flash('Book borrowed successfully!')
        else:
            flash('This book is not available for borrowing.', 'error')

    # Fetch borrowing records with sorting and pagination
    page = request.args.get('page', 1, type=int)
    per_page = 5
    sort_by = request.args.get('sortby', 'borrowdate')
    sort_order = request.args.get('order', 'desc')

    borrowing_records = Borrowing.query.order_by(db.text(f'{sort_by} {sort_order}')).paginate(page=page, per_page=per_page, error_out=False)

    # Fetch members and available books
    members = Member.query.all()
    books = Book.query.filter_by(available=True).all()

    return render_template(
        'borrow.html',
        borrowing_records=borrowing_records.items,  # Use .items for paginated results
        members=members,
        books=books,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        total_pages=borrowing_records.pages,  # Use pagination attribute for total pages
        datetime=datetime  # Pass the datetime object to the template context
    )

@app.route('/return_book/<int:borrowid>', methods=['POST'])
def return_book(borrowid):
    borrowing = Borrowing.query.get(borrowid)
    book = Book.query.get(borrowing.bookid)

    # Set the return date for the borrowing record
    borrowing.returndate = datetime.now().date()
    book.available = True  # Mark the book as available

    db.session.commit()

    flash('Book returned successfully!')
    return redirect(url_for('manage_borrowing'))

if __name__ == '__main__':
    app.run(debug=True)
