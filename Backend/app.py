from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from models import db, User, Book, Section
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
CORS(app, origins=['http://localhost:5173/*'])

db.init_app(app)

with app.app_context():
    db.create_all()


# Resources for CRUD operations
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return {'id': user.id, 'username': user.username, 'email': user.email}
        else:
            users = User.query.all()
            serialized_users = [
                {'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return serialized_users

    # The rest of the CRUD operations remain unchanged...

    def post(self):
        data = request.get_json()
        db.session.commit()
        return {'message': 'User updated successfully'}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}


# Section resource
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


def get_users():
    return User.query.all()


api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(SectionResource, '/sections', '/sections/<int:section_id>')

if __name__ == '__main__':
    app.run(debug=True)
