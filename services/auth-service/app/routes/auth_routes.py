from flask import Blueprint, request, jsonify

from app.config.db import db
from app.models.user_model import User
from app.utils.security import hash_password

from flask_jwt_extended import create_access_token
from app.utils.security import (
    hash_password,
    verify_password
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    existing_user = User.query.filter(
        (User.email == email) |
        (User.username == username)
    ).first()

    if existing_user:
        return jsonify({
            "error": "User already exists"
        }), 409

    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password.decode('utf-8')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    password_valid = verify_password(
        password,
        user.password.encode('utf-8')
    )

    if not password_valid:
        return jsonify({
            "error": "Invalid credentials"
        }), 401

    access_token = create_access_token(
    identity=str(user.id),
    additional_claims={
        "email": user.email,
        "role": user.role
    }
)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200