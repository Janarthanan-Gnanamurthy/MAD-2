from flask import request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

from models import db, User, Book, Section


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
