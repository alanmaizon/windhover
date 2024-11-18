import matplotlib
matplotlib.use('Agg')
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from datetime import datetime, timedelta
from sqlalchemy import func
import matplotlib.pyplot as plt
import io
from extensions import db
from models import Book, Member, Borrowing

borrow_bp = Blueprint('borrow_bp', __name__)

@borrow_bp.route('/borrowing', methods=['GET', 'POST'])
def manage_borrowing():
    thirty_days_loan = 30
    seven_days_deadline = 7
    
    if request.method == 'POST':
        print("Form Data:", request.form)
        book_id = request.form.get('bookid', '').strip()
        member_id = request.form.get('memberid', '').strip()

        print(f"Book ID: {book_id}, Member ID: {member_id}")

        if not book_id or not member_id:
            flash('Please select both a book and a member.', 'error')
            return redirect(url_for('borrow_bp.manage_borrowing'))

        try:
            book_id = int(book_id)
            member_id = int(member_id)
        except ValueError:
            flash('Invalid book or member ID.', 'error')
            return redirect(url_for('borrow_bp.manage_borrowing'))
        
        book = Book.query.get(book_id)
        member = Member.query.get(member_id)

        if not book or not member:
            flash('Book or member not found.', 'error')
            return redirect(url_for('borrow_bp.manage_borrowing'))

        if not book.available:
            flash('This book is not available for borrowing.', 'error')
            return redirect(url_for('borrow_bp.manage_borrowing'))
        
        # Create a new borrowing record
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=thirty_days_loan)
        borrowing = Borrowing(memberid=member_id, bookid=book_id, borrowdate=borrow_date, duedate=due_date)
        book.available = False  # Mark the book as unavailable
        db.session.add(borrowing)
        db.session.commit()
        flash('Book borrowed successfully!', 'success')
        return redirect(url_for('borrow_bp.manage_borrowing'))

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
        record.can_extend = (record.duedate - today).days <= seven_days_deadline and not record.returndate

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
    one_month_ago = datetime.now() - timedelta(days=30)
    
    results = db.session.query(
        func.date(Borrowing.borrowdate).label('date'),
        func.count().label('count')
    ).filter(
        Borrowing.borrowdate >= one_month_ago
    ).group_by(
        func.date(Borrowing.borrowdate)
    ).order_by(
        func.date(Borrowing.borrowdate)
    ).all()

    dates = [row.date for row in results]
    counts = [row.count for row in results]

    return dates, counts

@borrow_bp.route('/borrowing_plot')
def borrowing_plot():
    dates, counts = get_borrowing_data()

    plt.figure(figsize=(9, 5))
    plt.plot(dates, counts, marker='o')
    plt.title('Monthly Stats')
    plt.xlabel('Date')
    plt.ylabel('Checkouts')
    plt.xticks(rotation=0)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

@borrow_bp.route('/return_book/<int:borrowid>', methods=['POST'])
def return_book(borrowid):

    borrowing = Borrowing.query.get(borrowid)
    book = Book.query.get(borrowing.bookid)

    borrowing.returndate = datetime.now().date()
    book.available = True

    db.session.commit()

    flash('Book returned successfully!')
    return redirect(url_for('borrow_bp.manage_borrowing'))

@borrow_bp.route('/extend_loan/<int:borrow_id>', methods=['POST'])
def extend_loan(borrow_id):
    extend_one_week = 7
    borrowing_record = Borrowing.query.get(borrow_id)
    today = datetime.now().date()
    
    if borrowing_record and not borrowing_record.returndate:
        days_until_due = (borrowing_record.duedate - today).days
        
        if days_until_due <= extend_one_week:
            borrowing_record.duedate += timedelta(days=extend_one_week)
            db.session.commit()
            flash('Loan extended by one week!')
        else:
            flash('Cannot extend loan.', 'error')
    
    return redirect(url_for('borrow_bp.manage_borrowing'))