from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api
from api import UserResource, SectionResource, BookResource, AdminRequestsResource

from models import db, User, Request, Book, user_books

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import os
from datetime import date, timedelta

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


@app.route('/request-book', methods=['POST'])
@jwt_required()
def request_book():
    data = request.json
    user = get_jwt_identity()
    user_id = user['id']
    book_id = data.get('book_id')

    new_request = Request(
        user_id=user_id, book_id=book_id)
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Book request submitted successfully'}), 200


@app.route('/admin/approve', methods=['POST'])
@jwt_required()
def approve_book_request():
    user_id = get_jwt_identity()['id']
    print(user_id)
    print(request.get_json())
    # Rename 'request_payload' to avoid conflict with Flask 'request' object
    request_payload = request.get_json()

    if 'book_id' not in request_payload or 'request_id' not in request_payload:
        return jsonify({'error': 'Missing book_id or request_id in request'}), 400

    book_id = request_payload['book_id']
    request_id = request_payload['request_id']

    user = User.query.get(user_id)
    book = Book.query.get(book_id)

    if not user or not book:
        return jsonify({'error': 'User or book not found'}), 404

    date_issued = date.today()
    return_date = date_issued + timedelta(days=7)

    new_user_book = user_books.insert().values(user_id=user_id, book_id=book_id,
                                               date_issued=date_issued, return_date=return_date)

    book_request = Request.query.get(request_id)

    if not book_request:
        return jsonify({'message': 'Request not found'}), 404

    book_request.status = 'Approved'
    db.session.execute(new_user_book)
    db.session.commit()

    return jsonify({'message': 'Request approved successfully'}), 200


@app.route('/reject_book_request/<int:request_id>', methods=['PUT'])
def reject_book_request(request_id):
    request = Request.query.get(request_id)
    if not request:
        return jsonify({'message': 'Request not found'}), 404

    request.status = 'Rejected'
    db.session.commit()

    return jsonify({'message': 'Request rejected successfully'}), 200


@app.route('/user/books', methods=['GET'])
@jwt_required()
def get_user_books():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)

    acquired_books = []
    returned_books = []

    for book in user.books:
        book_data = {
            'id': book.id,
            'name': book.name
        }

        user_book = next(
            (ub for ub in book.users if ub.user_id == user_id), None)
        if user_book:
            book_data['return_date'] = str(user_book.return_date)
            acquired_books.append(book_data)
        else:
            returned_books.append(book_data)

    return jsonify({
        'acquired_books': acquired_books,
        'returned_books': returned_books
    })


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
api.add_resource(AdminRequestsResource, '/admin/requests')

if __name__ == '__main__':
    app.run(debug=True)
