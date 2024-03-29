from flask import request
from flask_restful import Resource, marshal_with, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import db, User, Book, Section

book_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'content': fields.String,
    'author': fields.String,
    'date_issued': fields.DateTime,
    'return_date': fields.DateTime,
    'section_id': fields.Integer
}


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return {'id': user.id, 'username': user.username, 'email': user.email}
        else:
            users = User.query.all()
            serialized_users = [
                {'id': user.id, 'username': user.username, 'email': user.email, 'password': user.password} for user in users]
            return serialized_users

    def post(self):
        data = request.get_json()
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User updated successfully'}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}


class SectionResource(Resource):
    def get(self, section_id=None):
        if section_id:
            section = Section.query.get(section_id)
            if section:
                return str(section.__dict__), 200
            else:
                return {"message": "Section not found"}, 404
        else:
            sections = Section.query.all()
            return [{'name': section.name, 'description': section.description, 'date_created': f'{section.date_created}'} for section in sections], 200

    def post(self):
        data = request.json
        new_section = Section(
            name=data['name'], description=data['description'], date_created=datetime.now())
        db.session.add(new_section)
        db.session.commit()
        return {"message": "Section created successfully"}, 201


class BookResource(Resource):
    @marshal_with(book_fields)
    def get(self, book_id=None):
        if book_id:
            book = Book.query.get(book_id)
            if book:
                return book, 200
            else:
                return {"message": "Book not found"}, 404
        else:
            books = Book.query.all()
            return books, 200

    @marshal_with(book_fields)
    def post(self):
        data = request.json
        new_book = Book(
            name=data['name'],
            content=data['content'],
            author=data['author'],
            date_issued=data['date_issued'],
            return_date=data['return_date'],
            section_id=data['section_id']
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book, 201

    @marshal_with(book_fields)
    def put(self, book_id):
        book = Book.query.get(book_id)
        if book:
            data = request.json
            book.name = data['name']
            book.content = data['content']
            book.author = data['author']
            book.date_issued = data['date_issued']
            book.return_date = data['return_date']
            book.section_id = data['section_id']
            db.session.commit()
            return book, 200
        else:
            return {"message": "Book not found"}, 404

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book deleted successfully"}, 200
        else:
            return {"message": "Book not found"}, 404
