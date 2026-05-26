from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import json
from app.config.redis_client import redis_client
from app.config.db import db
from app.models.product_model import Product

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():

    data = request.get_json()

    product = Product(
        name=data.get('name'),
        description=data.get('description'),
        price=data.get('price'),
        stock=data.get('stock'),
        category=data.get('category')
    )

    db.session.add(product)
    db.session.commit()

    redis_client.delete('all_products')

    return jsonify({
        "message": "Product created successfully",
        "product": product.to_dict()
    }), 201


@product_bp.route('/products', methods=['GET'])
def get_products():

    cached_products = redis_client.get('all_products')

    if cached_products:
        return jsonify(json.loads(cached_products))

    products = Product.query.all()

    product_list = [
        product.to_dict()
        for product in products
    ]

    redis_client.set(
        'all_products',
        json.dumps(product_list),
        ex=60
    )

    return jsonify(product_list)


@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product.to_dict())