from app import db

class Book(db.Model):
    __tablename__ = 'books'
    bookid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    publicationyear = db.Column(db.Integer, nullable=False)
    imagepath = db.Column(db.String(255), nullable=True)
    available = db.Column(db.Boolean, default=True)

class Member(db.Model):
    __tablename__ = 'members'
    memberid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    joindate = db.Column(db.Date, nullable=False)
    profilepicture = db.Column(db.String(255), nullable=True)

class Borrowing(db.Model):
    __tablename__ = 'borrowing'
    borrowid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    memberid = db.Column(db.Integer, db.ForeignKey('members.memberid'), nullable=False)
    bookid = db.Column(db.String, db.ForeignKey('books.bookid'), nullable=False)
    borrowdate = db.Column(db.Date, nullable=False)
    duedate = db.Column(db.Date, nullable=False)
    returndate = db.Column(db.Date, nullable=True)

    member = db.relationship('Member', backref=db.backref('borrowings', lazy=True))
    book = db.relationship('Book', backref=db.backref('borrowings', lazy=True))
