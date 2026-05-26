from flask import Blueprint, request, jsonify

from app.config.db import db
from app.models.user_model import User
from app.utils.security import hash_password

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