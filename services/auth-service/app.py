from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

import os

from app.config.db import db, DATABASE_URI
from app.models.user_model import User
from app.routes.auth_routes import auth_bp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
jwt = JWTManager(app)
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def home():
    return {
        "service": "auth-service",
        "status": "running"
    }

@app.route('/protected')
@jwt_required()
def protected():

    current_user_id = get_jwt_identity()
    claims = get_jwt()

    return {
        "message": "Protected route accessed",
        "user": {
            "id": current_user_id,
            "email": claims.get("email"),
            "role": claims.get("role")
        }
    }

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)