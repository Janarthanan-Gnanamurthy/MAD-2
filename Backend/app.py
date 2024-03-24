from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from models import db, User, Book, Section
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
        data = request.json
        print(data)
        # user = User(**data)
        # db.session.add(user)
        # db.session.commit()
        return {'message': 'data'}, 201

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        db.session.commit()
        return {'message': 'User updated successfully'}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}


def get_users():
    return User.query.all()


api.add_resource(UserResource, '/users', '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
