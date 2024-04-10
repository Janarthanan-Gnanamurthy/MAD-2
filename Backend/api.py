from flask import request
from flask_restful import Resource, marshal_with, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from models import db, User, Book, Section, Request

book_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'content': fields.String,
    'author': fields.String,
    'section_id': fields.Integer,
    'image_filename': fields.String
}

section_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'date_created': fields.DateTime(dt_format='iso8601'),
    'books': fields.List(fields.Nested(book_fields)),
}

request_fields = {
    'id': fields.Integer,
    'user': fields.Nested({
        'id': fields.Integer,
        'username': fields.String
    }),
    'book': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'date_requested': fields.String(attribute=lambda x: x.date_requested.strftime('%Y-%m-%d')),
    'status': fields.String
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
    @jwt_required()
    def get(self, section_id=None):
        user_id = get_jwt_identity()['id']
        user = User.query.get_or_404(user_id)
        if section_id:
            section = Section.query.get(section_id)
            if section:
                # Fetch all books related to the section
                books = Book.query.filter_by(section_id=section_id).all()
                section.books = books
                serial_section = marshal(section, section_fields)

                return serial_section, 200
            else:
                return {"message": "Section not found"}, 404
        else:
            books = [book.id for book in user.books]
            sections = Section.query.all()
            serial_sections = marshal(sections, section_fields)
            return {'sections': serial_sections, 'userBooks': books}, 200

    @jwt_required()
    def put(self, section_id):
        data = request.json
        section = Section.query.get(section_id)
        if not section:
            return {"message": "Section not found"}, 404

        # Update section details
        section.name = data.get('name', section.name)
        section.description = data.get('description', section.description)

        # Remove existing books from the section
        section.books.clear()

        # Add books to the section
        book_ids = data.get('book_ids', [])
        for book_id in book_ids:
            book = Book.query.get(book_id)
            if book:
                section.books.append(book)

        db.session.commit()
        return {"message": "Section updated successfully"}, 200

    @marshal_with(section_fields)
    def post(self):
        data = request.json
        new_section = Section(
            name=data['name'], description=data['description'], date_created=datetime.now())
        db.session.add(new_section)
        db.session.commit()
        return {"message": "Section created successfully"}, 201


class BookResource(Resource):
    @marshal_with(book_fields)
    @jwt_required()
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
    @jwt_required()
    def put(self, book_id):
        book = Book.query.get(book_id)
        if book:
            data = request.json
            book.name = data['name']
            book.content = data['content']
            book.author = data['author']
            book.section_id = data['section_id']
            db.session.commit()
            return book, 200
        else:
            return {"message": "Book not found"}, 404

    @marshal_with(book_fields)
    def post(self):
        if request.headers.get('Content-Type') == 'application/json':
            # Handle JSON data
            data = request.json
            new_book = Book(
                name=data['name'],
                content=data['content'],
                author=data['author'],
                section_id=data['section_id']
            )
            db.session.add(new_book)
            db.session.commit()

            return new_book, 201
        elif request.headers.get('Content-Type').startswith('multipart/form-data'):
            # Handle file upload
            name = request.form.get('name')
            content = request.form.get('content')
            author = request.form.get('author')
            section_id = request.form.get('section_id')
            file = request.files.get('file')

            if not (name and content and author and section_id and file):
                return {'error': 'Missing required fields'}, 400

            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join('uploads/books', filename)
                file.save(filepath)

                new_book = Book(
                    name=name,
                    content=content,
                    author=author,
                    section_id=section_id,
                    image_filename=filename
                )
                db.session.add(new_book)
                db.session.commit()

                return new_book, 201
            else:
                return {'error': 'Invalid file type'}, 400
        else:
            return {'error': 'Unsupported Content-Type'}, 400

    def upload_book_image(self, book_id):
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400

        file = request.files['file']

        if file.filename == '':
            return {'error': 'No selected file'}, 400

        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            book = Book.query.get_or_404(book_id)
            book.image_filename = filename
            db.session.commit()

            return {'message': 'File successfully uploaded'}, 200
        else:
            return {'error': 'Invalid file type'}, 400

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book deleted successfully"}, 200
        else:
            return {"message": "Book not found"}, 404


class AdminRequestsResource(Resource):
    @marshal_with(request_fields)
    def get(self):
        try:
            requests = Request.query.all()
            return requests, 200
        except Exception as e:
            return {"message": str(e)}, 500
