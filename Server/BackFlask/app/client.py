import psycopg2
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from PostgreSQL import DB_INSERT_TABLE_USERS, DB_SELECT_TABLE_USERS
from models.user import User
from utils.database import connection

client_bp = Blueprint('client', __name__)


@client_bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return "Unsupported Media Type: Expecting JSON", 415

    requested_data = request.get_json()
    user = User(username=requested_data['username'], password=requested_data['password'])

    with connection, connection.cursor() as cursor:
        try:
            cursor.execute(DB_INSERT_TABLE_USERS, (user.username, user.password))
            connection.commit()
        except psycopg2.Error as err:
            return f"User already exists! {err}", 500

    return {"message": f"User {user.username} registered successfully!"}, 201


@client_bp.route('/login', methods=['GET'])
def login():
    if not request.is_json:
        return "Unsupported Media Type: Expecting JSON", 415

    requested_data = request.get_json()
    username = requested_data['username']
    password = requested_data['password']

    with connection, connection.cursor() as cursor:
        cursor.execute(DB_SELECT_TABLE_USERS, (username, password))
        user = cursor.fetchone()

    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
