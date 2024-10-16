from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from urllib.parse import urlparse
import math 

app = Flask(__name__)

# Load configuration from environment variables
app.secret_key = os.getenv('SECRET_KEY', 'your_fallback_secret_key')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/images')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB limit by default

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fetch GitHub token from environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # This will pull the token set in Render.com
GITHUB_REPO = 'alanmaizon/windhover'
GITHUB_BRANCH = 'main'
UPLOAD_DIR = 'static/images/profile_pics'

# Function to upload file to GitHub
def upload_file_to_github(filepath, filename):
    with open(filepath, "rb") as file:
        content = file.read()
        base64_content = content.encode("base64")
    
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{UPLOAD_DIR}/{filename}'
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"Upload {filename}",
        "content": base64_content,
        "branch": GITHUB_BRANCH
    }
    
    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print(f"File {filename} uploaded successfully!")
    else:
        print(f"Failed to upload {filename}. Error: {response.json()}")

# Retrieve the Internal Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for the Flask application")

result = urlparse(DATABASE_URL)

# Function to connect to the database
def get_db_connection():
    return psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/books', methods=('GET', 'POST'))
def books():
    conn = get_db_connection()

    if request.method == 'POST':
        cursor = conn.cursor()

        # Fetch the highest bookid and increment it
        cursor.execute('SELECT MAX(bookid) FROM books')
        max_id = cursor.fetchone()[0]
        new_bookid = max_id + 1 if max_id else 1

        # Get form data
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
            # Remove the static/ part before storing
            img_path = img_path.replace("static/", "")
        else:
            img_path = None

        # Insert new book
        cursor.execute('''
            INSERT INTO books (bookid, title, author, genre, publicationyear, imagepath)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (new_bookid, title, author, genre, pub_year, img_path))

        conn.commit()
        cursor.close()
        

    # Fetch the sorting option from query parameters (default to 'title')
    sort_by = request.args.get('sortby', 'title')
    sort_order = request.args.get('order', 'asc')

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Construct the query to fetch books sorted by the chosen column
    cursor.execute(f'SELECT * FROM books ORDER BY {sort_by} {sort_order.upper()}')
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    # Pass the current year, books, sort option, and order to the template
    current_year = datetime.now().year
    return render_template('books.html', books=books, current_year=current_year, sort_by=sort_by, sort_order=sort_order)


@app.route('/members', methods=['GET', 'POST'])
def members_page():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Handle form submission for adding a new member
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        joindate = datetime.now().date()

        # Handle the image file upload
        file = request.files['profile_picture']
        if file:
            filename = secure_filename(file.filename)
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the file locally first
            file.save(temp_path)
            
            # Upload the file to GitHub
            upload_file_to_github(temp_path, filename)
            
            # Delete the temporary file after uploading
            os.remove(temp_path)
            
            flash(f"Profile picture {filename} uploaded to GitHub successfully!", "success")
        

        # Insert new member
        cursor.execute('''
            INSERT INTO members (firstname, lastname, email, joindate, profilepicture)
            VALUES (%s, %s, %s, %s, %s)
        ''', (firstname, lastname, email, joindate, img_path))
        conn.commit()

    # Handle sorting and searching
    sort_by = request.args.get('sortby', 'lastname')
    sort_order = request.args.get('order', 'asc')
    search_query = request.args.get('search', '')

    query = f"SELECT * FROM members WHERE firstname ILIKE %s OR lastname ILIKE %s ORDER BY {sort_by} {sort_order}"
    cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
    members = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('members.html', members=members, sort_by=sort_by, sort_order=sort_order, search_query=search_query)

@app.route('/borrowing', methods=['GET', 'POST'])
def manage_borrowing():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Handle Borrow Book form submission
    if request.method == 'POST':
        member_id = request.form['memberid']
        book_id = request.form['bookid']

        # Check if book is available
        cursor.execute('SELECT available FROM books WHERE bookid = %s', (book_id,))
        book = cursor.fetchone()
        
        if book['available']:  # If the book is available to borrow
            borrow_date = datetime.now().date()
            due_date = borrow_date + timedelta(days=30)
            
            cursor.execute('''
                INSERT INTO borrowing (memberid, bookid, borrowdate, duedate)
                VALUES (%s, %s, %s, %s)
            ''', (member_id, book_id, borrow_date, due_date))
            
            # Update the book's availability status to unavailable
            cursor.execute('UPDATE books SET available = FALSE WHERE bookid = %s', (book_id,))
            conn.commit()
            flash('Book borrowed successfully!')
        else:
            flash('This book is not available for borrowing.', 'error')
    
    # Pagination setup
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Adjust the number of records per page

    # Fetch borrowing records with pagination
    cursor.execute('SELECT COUNT(*) FROM borrowing')
    total_records = cursor.fetchone()[0]
    total_pages = math.ceil(total_records / per_page)

    offset = (page - 1) * per_page
    sort_by = request.args.get('sortby', 'borrowdate')
    sort_order = request.args.get('order', 'desc')

    cursor.execute(f'''
        SELECT b.borrowid, b.borrowdate, b.duedate, b.returndate, bk.title, m.firstname, m.lastname
        FROM borrowing b
        JOIN books bk ON b.bookid = bk.bookid
        JOIN members m ON b.memberid = m.memberid
        ORDER BY {sort_by} {sort_order}
        LIMIT %s OFFSET %s
    ''', (per_page, offset))
    borrowing_records = cursor.fetchall()

    # Fetch members and available books for the form dropdown
    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()
    
    cursor.execute('SELECT * FROM books WHERE available = TRUE')
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'borrow.html', 
        borrowing_records=borrowing_records,
        members=members,
        books=books,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        total_pages=total_pages,
        datetime=datetime
    )

@app.route('/return_book/<int:borrowid>', methods=['POST'])
def return_book(borrowid):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Get book id from the borrowing record
    cursor.execute('SELECT bookid FROM borrowing WHERE borrowid = %s', (borrowid,))
    book = cursor.fetchone()

    # Set the return date for the borrowing record
    return_date = datetime.now().date()
    cursor.execute('UPDATE borrowing SET returndate = %s WHERE borrowid = %s', (return_date, borrowid))
    
    # Update the book's availability to true
    cursor.execute('UPDATE books SET available = TRUE WHERE bookid = %s', (book['bookid'],))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash('Book returned successfully!')
    return redirect(url_for('manage_borrowing'))

if __name__ == '__main__':
    app.run(debug=True)
