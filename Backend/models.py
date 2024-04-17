from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

db = SQLAlchemy()


class UserBooks(db.Model):
    __tablename__ = 'user_books'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    feedback = db.Column(db.String)
    date_issued = db.Column(db.Date, nullable=False, default=date.today())
    return_date = db.Column(db.Date, nullable=False,
                            default=date.today() + timedelta(days=7))
    returned_on = db.Column(db.Date, nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(120))
    role = db.Column(db.String(50), nullable=False, default='User')
    books = db.relationship('Book', secondary='user_books', lazy='subquery',
                            backref=db.backref('users', lazy=True))
    last_visited = db.Column(db.Date)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    image_filename = db.Column(db.String(255))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    description = db.Column(db.String)
    date_created = db.Column(db.Date)
    books = db.relationship('Book', backref='section', lazy=True)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    date_requested = db.Column(
        db.Date, nullable=False, default=date.today)
    # Possible values: Pending, Approved, Completed, Revoked
    status = db.Column(db.String(50), nullable=False, default='Pending')

    user = db.relationship('User', backref='requests')
    book = db.relationship('Book', backref='requests')
