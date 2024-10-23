from flask import Blueprint, request, render_template, flash, redirect, url_for
from app import db
from models import Borrowing, Member, Book
from datetime import datetime, timedelta
import math

borrowing_bp = Blueprint('borrowing_bp', __name__)

@borrowing_bp.route('/borrowing', methods=['GET', 'POST'])
def manage_borrowing():
    if request.method == 'POST':
        member_id = request.form['memberid']
        book_id = request.form['bookid']

        # Check if the book is available
        book = Book.query.filter_by(bookid=book_id).first()
        if book and book.available:
            borrow_date = datetime.now().date()
            due_date = borrow_date + timedelta(days=30)

            borrowing = Borrowing(memberid=member_id, bookid=book_id, borrowdate=borrow_date, duedate=due_date)
            book.available = False
            db.session.add(borrowing)
            db.session.commit()

            flash('Book borrowed successfully!')
        else:
            flash('This book is not available for borrowing.', 'error')

    # Fetch borrowing records with pagination and sorting
    page = request.args.get('page', 1, type=int)
    per_page = 5
    sort_by = request.args.get('sortby', 'borrowdate')
    sort_order = request.args.get('order', 'desc')

    borrowing_records = Borrowing.query.order_by(db.text(f'{sort_by} {sort_order}')).paginate(page, per_page, False)

    # Fetch members and available books
    members = Member.query.all()
    books = Book.query.filter_by(available=True).all()

    return render_template('borrow.html', borrowing_records=borrowing_records.items, members=members, books=books, sort_by=sort_by, sort_order=sort_order, page=page)
