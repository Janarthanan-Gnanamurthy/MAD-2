from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

user_books = db.Table('user_books',
                      db.Column('user_id', db.Integer, db.ForeignKey(
                          'user.id'), primary_key=True),
                      db.Column('book_id', db.Integer, db.ForeignKey(
                          'book.id'), primary_key=True),
                      db.Column('date_issued', db.Date, nullable=False),
                      db.Column('return_date', db.Date, nullable=False)
                      )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='User')
    books = db.relationship('Book', secondary=user_books, backref='users')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    image_filename = db.Column(db.String(255))
    section_id = db.Column(db.Integer, db.ForeignKey(
        'section.id'), nullable=False)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    description = db.Column(db.String)
    date_created = db.Column(db.Date)
    books = db.relationship('Book', backref='section', lazy=True)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    date_requested = db.Column(
        db.Date, nullable=False, default=date.today)
    # Possible values: Pending, Approved, Rejected
    status = db.Column(db.String(50), nullable=False, default='Pending')

    user = db.relationship('User', backref='requests')
    book = db.relationship('Book', backref='requests')
