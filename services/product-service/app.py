from flask import Flask
from dotenv import load_dotenv
import os

from app.config.db import db, DATABASE_URI
from app.models.product_model import Product
from app.routes.product_routes import product_bp
from flask_jwt_extended import JWTManager

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
jwt = JWTManager(app)
app.register_blueprint(product_bp, url_prefix='/api')

@app.route('/')
def home():
    return {
        "service": "product-service",
        "status": "running"
    }

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)