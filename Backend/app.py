from flask import Flask, request, send_from_directory
from flask_restful import Api
from api import UserResource, SectionResource, BookResource

from models import db, User, Book, Section

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret'

api = Api(app)
CORS(app, origins=['http://localhost:5173/*'])

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        response = request.json
        user = User.query.filter_by(username=response['username']).first()
        if user and response['password'] == user.password:
            access_token = create_access_token(
                identity={'id': user.id, 'username': user.username, 'email': user.email})
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Wrong Username or Password'}, 404

    else:
        return {'message': 'this is login page'}


@app.route('/uploads/books/<filename>')
def uploaded_book_image(filename):
    return send_from_directory(os.path.join('uploads/books'), filename)


@app.route('/useridentity', methods=["GET"])
@jwt_required()
def userid():
    return get_jwt_identity()


api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(SectionResource, '/sections', '/sections/<int:section_id>')
api.add_resource(BookResource, '/books', '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True)
