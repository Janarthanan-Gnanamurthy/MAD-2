from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api
from api import UserResource, SectionResource, BookResource, AdminRequestsResource

from models import db, User, Request, Book, UserBooks

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from functools import wraps
import os
from datetime import date, timedelta, datetime

from celery import Celery
from celery.schedules import crontab
import tasks

celery = Celery(__name__, broker='redis://localhost:6379/0',
                result_backend='redis://localhost:6379/1')
celery.conf.imports = ('tasks',)
# celery.autodiscover_tasks(['tasks'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret'

api = Api(app)
CORS(app, origins=['http://localhost:5173/*'])

app.config.update(
    CELERYBEAT_SCHEDULE={
        'send_daily_reminder': {
            'task': 'tasks.send_daily_reminder',
            'schedule': crontab(hour=20, minute=10)
        }
    }
)


db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()


@app.route('/trigger-reminder', methods=['GET'])
def trigger_reminder():
    tasks.send_daily_reminder.delay()
    return jsonify({"message": "Daily reminder task triggered successfully!"}), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        response = request.json
        user = User.query.filter_by(username=response['username']).first()
        if user and response['password'] == user.password:
            user.last_visited = datetime.now()
            db.session.commit()
            access_token = create_access_token(
                identity={'id': user.id, 'username': user.username, 'email': user.email})

            user.last_visited = datetime.now()
            db.session.commit()
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Wrong Username or Password'}, 404

    else:
        return {'message': 'this is login page'}


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    response = request.json
    user = User.query.filter_by(username=response['username']).first()
    if user.role == 'admin':
        if user and response['password'] == user.password:
            access_token = create_access_token(
                identity={'id': user.id, 'username': user.username, 'email': user.email})
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Wrong Username or Password'}, 404
    else:
        return {'message': 'No Admin Priveledges'}, 401


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
    request_payload = request.get_json()

    if 'book_id' not in request_payload or 'request_id' not in request_payload:
        return jsonify({'error': 'Missing book_id or request_id in request'}), 400

    book_id = request_payload['book_id']
    request_id = request_payload['request_id']

    user = User.query.get(user_id)
    book = Book.query.get(book_id)

    if not user or not book:
        return jsonify({'error': 'User or book not found'}), 404

    user.books.append(book)

    book_request = Request.query.get(request_id)

    if not book_request:
        return jsonify({'message': 'Request not found'}), 404

    book_request.status = 'Approved'
    db.session.commit()

    return jsonify({'message': 'Request approved successfully'}), 200


@app.route('/admin/revoke', methods=['POST'])
@jwt_required()
def reject_book_request():
    user_id = get_jwt_identity()['id']
    response = request.get_json()
    db_request = Request.query.get(response['request_id'])
    if not db_request:
        return jsonify({'message': 'Request not found'}), 404
    db_request.status = 'Revoked'

    user_book = db.session.query(UserBooks).filter_by(
        user_id=user_id, book_id=response['book_id']
    ).first()

    if user_book:
        db.session.delete(user_book)
        db.session.commit()
        return jsonify({'message': 'Access Revoked successfully'}), 200
    else:
        return jsonify({'message': 'User book not found'}), 404


@app.route('/user/books', methods=['GET'])
@jwt_required()
def get_UserBooks():
    user_id = get_jwt_identity()['id']
    user = User.query.get(user_id)

    acquired_books = []
    returned_books = []

    for book in user.books:
        book_data = {
            'id': book.id,
            'name': book.name
        }

        user_book = db.session.query(UserBooks).filter_by(
            user_id=user_id, book_id=book.id).first()

        if user_book.returned_on:
            book_data['returned_on'] = user_book.returned_on

            returned_books.append(book_data)
        else:
            book_data['return_date'] = str(user_book.return_date)

            # Check if return_date is passed
            if user_book.return_date < date.today():
                returned_books.append(book_data)
            else:
                acquired_books.append(book_data)

    return jsonify({
        'acquired_books': acquired_books,
        'returned_books': returned_books
    })


def has_book_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        book_id = request.view_args.get('book_id')  # Get book_id from URL rule

        current_user_id = get_jwt_identity()['id']
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'Invalid user'}), 401

        book = Book.query.get(book_id)
        user_book = db.session.query(UserBooks).filter_by(
            user_id=current_user_id, book_id=book_id).first()

        if book and user_book and user_book.returned_on is None:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Book not found or you do not have access'}), 404

    return wrapper


@app.route('/get-book/<int:book_id>', methods=['GET'])
@jwt_required()
@has_book_access
def get_book_content(book_id):
    book = Book.query.get(book_id)
    content_path = book.content
    try:
        return {'pdfurl': content_path}
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/user/return/<int:book_id>', methods=['PUT'])
@jwt_required()
def return_book(book_id):
    user_id = get_jwt_identity()['id']
    db.session.query(UserBooks).filter_by(
        user_id=user_id, book_id=book_id).update({'returned_on': date.today()})
    Request.query.filter_by(user_id=user_id, book_id=book_id).update(
        {'status': 'Completed'})
    db.session.commit()
    return jsonify({'message': 'Successfully returned book'}), 200


@app.route('/user/feedback/<int:book_id>', methods=["PUT"])
@jwt_required()
def feedback(book_id):
    response = request.get_json()
    print(response)
    user_id = get_jwt_identity()['id']

    result = db.session.query(UserBooks).filter_by(
        user_id=user_id, book_id=book_id
    ).update(
        {'feedback': response['feedback']}, synchronize_session=False
    )
    if result == 0:
        return {'message': 'user_book not found'}

    db.session.commit()

    return {'message': 'Successfully updated'}


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
