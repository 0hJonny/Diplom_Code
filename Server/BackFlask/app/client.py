import psycopg2
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
import datetime

from PostgreSQL import *
from models.user import User, User_model
from utils.database import users_connection

client_bp = Blueprint('client', __name__)


@client_bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return "Unsupported Media Type: Expecting JSON", 415

    requested_data = request.get_json()

    user = User(username=requested_data['username'], password=requested_data['password'])
    
    with psycopg2.connect(users_connection) as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(DB_INSERT_TABLE_USERS, (user.username, user.password))
                connection.commit()
        except psycopg2.Error as err:
            connection.rollback()
            return f"User already exists! {err}", 500

    return {"message": f"User {user.username} registered successfully!"}, 201


@client_bp.route('/login', methods=['GET'])
def login():
    if not request.is_json:
        return "Unsupported Media Type: Expecting JSON", 415

    requested_data = request.get_json()
    user = User(username=requested_data['username'], password=requested_data['password'])

    with psycopg2.connect(users_connection) as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(DB_SELECT_TABLE_USERS, (user.username,))
                user_data = cursor.fetchone()
                if user_data is None:
                    return jsonify({'message': 'No user data found'}), 404
                user_data = User_model(*user_data)
                if bcrypt.checkpw(user.password.encode('utf-8'), user_data.password.encode('utf-8')):
                    access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(days=1))
                    return jsonify(access_token=access_token), 200
                else:
                    return jsonify({'message': 'Invalid credentials'}), 401
        except psycopg2.Error as err:
            return f"Database error: {err}", 500

@client_bp.route('/verify', methods=['PUT'])
def verify():
    if not request.is_json:
        return "Unsupported Media Type: Expecting JSON", 415

    requested_data = request.get_json()
    verification_code = 534421
    user = User(username=requested_data['username'], password=requested_data['password'])

    with psycopg2.connect(users_connection) as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
                user_data = cursor.fetchone()
                if user_data is None:
                    return jsonify({'message': 'No user data found'}), 404
                user_data = User_model(*user_data)
                if user_data.confirmed:
                    return jsonify({'message': 'User already verified'}), 200
                if bcrypt.checkpw(user.password.encode('utf-8'), user_data.password.encode('utf-8')):
                    if verification_code == verification_code: # TODO Verification code from email
                        cursor.execute(DB_SELECT_TABLE_USERS_BY_ID_CONFIRMED, (user_data.user_id,))
                        connection.commit()
                        return jsonify({'message': 'User verified successfully!'}), 200
                    else:
                        return jsonify({'message': 'Invalid verification code'}), 401
                else:
                    return jsonify({'message': 'Invalid credentials'}), 401
        except psycopg2.Error as err:
            return f"Database error: {err}", 500