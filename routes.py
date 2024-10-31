import matplotlib
matplotlib.use('Agg')
from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import func
import matplotlib.pyplot as plt
import io
import os
from app import app, db
from models import Book, Member, Borrowing
from config import Config


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

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

    sort_by = request.args.get('sortby', 'title')
    sort_order = request.args.get('order', 'asc')

    allowed_sort_columns = ['title', 'author', 'genre', 'publicationyear']
    if sort_by not in allowed_sort_columns:
        sort_by = 'title'
    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'

    books = Book.query.order_by(db.text(f'{sort_by} {sort_order}')).all()
    current_year = datetime.now().year
    return render_template('books.html', books=books, current_year=current_year, sort_by=sort_by, sort_order=sort_order)

@app.route('/members', methods=['GET', 'POST'])
def members_page():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        joindate = datetime.now().date()

        file = request.files['profilepicture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics', filename))
            img_path = os.path.join('images/profile_pics', filename).replace("\\", "/")
        else:
            img_path = None

        new_member = Member(firstname=firstname, lastname=lastname, email=email, joindate=joindate, profilepicture=img_path)
        db.session.add(new_member)
        db.session.commit()

    sort_by = request.args.get('sortby', 'lastname')
    sort_order = request.args.get('order', 'asc')
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 6

    # Modify the members query with search, sort, and pagination
    members_query = Member.query.filter(
        (Member.firstname.ilike(f'%{search_query}%')) | 
        (Member.lastname.ilike(f'%{search_query}%'))
    ).order_by(db.text(f'{sort_by} {sort_order}'))

    members_pagination = members_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'members.html',
        members=members_pagination.items,
        sort_by=sort_by,
        sort_order=sort_order,
        search_query=search_query,
        page=page,
        total_pages=members_pagination.pages
    )

@app.route('/members/edit', methods=['POST'])
def edit_member():
    member_id = request.form['memberid']
    member = Member.query.get(member_id)
    if member:
        member.firstname = request.form['firstname']
        member.lastname = request.form['lastname']
        member.email = request.form['email']
        db.session.commit()
        flash('Member information updated successfully!', 'success')
    else:
        flash('Member not found.', 'error')
    return redirect(url_for('members_page'))


@app.route('/borrowing', methods=['GET', 'POST'])
def manage_borrowing():
    if request.method == 'POST':
        print("Form Data:", request.form)
        book_id = request.form.get('bookid', '').strip()
        member_id = request.form.get('memberid', '').strip()

        print(f"Book ID: {book_id}, Member ID: {member_id}")

        if not book_id or not member_id:
            flash('Please select both a book and a member.', 'error')
            return redirect(url_for('manage_borrowing'))

        try:
            book_id = int(book_id)
            member_id = int(member_id)
        except ValueError:
            flash('Invalid book or member ID.', 'error')
            return redirect(url_for('manage_borrowing'))
        
        book = Book.query.get(book_id)
        member = Member.query.get(member_id)

        if not book or not member:
            flash('Book or member not found.', 'error')
            return redirect(url_for('manage_borrowing'))

        if not book.available:
            flash('This book is not available for borrowing.', 'error')
            return redirect(url_for('manage_borrowing'))
        
        # Create a new borrowing record
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=30)
        borrowing = Borrowing(memberid=member_id, bookid=book_id, borrowdate=borrow_date, duedate=due_date)
        book.available = False  # Mark the book as unavailable
        db.session.add(borrowing)
        db.session.commit()
        flash('Book borrowed successfully!', 'success')
        return redirect(url_for('manage_borrowing'))

    # GET request handling
    page = request.args.get('page', 1, type=int)
    per_page = 5
    sort_by = request.args.get('sortby', 'borrowdate')
    sort_order = request.args.get('order', 'desc')
    search_query = request.args.get('search', '').strip()

    borrowing_records_query = Borrowing.query.join(Book).filter(
        (Book.title.ilike(f'%{search_query}%')) | (search_query == '')
    ).order_by(db.text(f'{sort_by} {sort_order}'))

    borrowing_records = borrowing_records_query.paginate(page=page, per_page=per_page, error_out=False)

    members = Member.query.all()
    books = Book.query.filter_by(available=True).all()

    today = datetime.now().date()
    for record in borrowing_records.items:
        record.can_extend = (record.duedate - today).days <= 7 and not record.returndate

    return render_template(
        'borrow.html',
        borrowing_records=borrowing_records.items,
        members=members,
        books=books,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        total_pages=borrowing_records.pages,
        datetime=datetime,
        search_query=search_query
    )

def get_borrowing_data():
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    results = db.session.query(
        func.date(Borrowing.borrowdate).label('date'),
        func.count().label('count')
    ).filter(
        Borrowing.borrowdate >= thirty_days_ago
    ).group_by(
        func.date(Borrowing.borrowdate)
    ).order_by(
        func.date(Borrowing.borrowdate)
    ).all()

    dates = [row.date for row in results]
    counts = [row.count for row in results]

    return dates, counts

@app.route('/borrowing_plot')
def borrowing_plot():
    dates, counts = get_borrowing_data()

    plt.figure(figsize=(10, 5))
    plt.plot(dates, counts, marker='o')
    plt.title('Borrowing Trends')
    plt.xlabel('Date')
    plt.ylabel('Number of Borrowings')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


@app.route('/return_book/<int:borrowid>', methods=['POST'])
def return_book(borrowid):
    borrowing = Borrowing.query.get(borrowid)
    book = Book.query.get(borrowing.bookid)

    borrowing.returndate = datetime.now().date()
    book.available = True

    db.session.commit()

    flash('Book returned successfully!')
    return redirect(url_for('manage_borrowing'))

@app.route('/extend_loan/<int:borrow_id>', methods=['POST'])
def extend_loan(borrow_id):
    borrowing_record = Borrowing.query.get(borrow_id)
    today = datetime.now().date()
    
    if borrowing_record and not borrowing_record.returndate:
        days_until_due = (borrowing_record.duedate - today).days
        
        if days_until_due <= 7:
            borrowing_record.duedate += timedelta(days=7)  # Extends the due date by 7 days
            db.session.commit()
            flash('Loan extended by one week!')
        else:
            flash('Cannot extend loan.', 'error')
    
    return redirect(url_for('manage_borrowing'))