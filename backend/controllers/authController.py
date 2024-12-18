from flask import Blueprint, request, jsonify
from models.user import create_user, find_user_by_email
import bcrypt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    create_user(email, hashed_password)
    
    return jsonify({'message': 'User registered successfully.'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body phải là JSON'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email và password là bắt buộc'}), 400

    user = find_user_by_email(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        token = jwt.encode({'email': email}, os.getenv('SECRET_KEY'), algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401
