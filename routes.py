from flask import Blueprint, request, jsonify
from db import db
from models import Brand, PromoCode
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

routes = Blueprint('routes', __name__)
bcrypt = Bcrypt()

@routes.route('/register', methods=['POST'])
def register():
    data = request.json
    if Brand.query.filter_by(login=data['login']).first():
        return jsonify({'msg': 'Login already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_brand = Brand(
        name=data['name'],
        channel=data['channel'],
        avatar=data['avatar'],
        topic=data['topic'],
        email=data['email'],
        login=data['login'],
        password=hashed_password
    )
    db.session.add(new_brand)
    db.session.commit()
    return jsonify({'msg': 'Brand registered successfully'}), 201

@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    brand = Brand.query.filter_by(login=data['login']).first()
    if brand and bcrypt.check_password_hash(brand.password, data['password']):
        token = create_access_token(identity=brand.id)
        return jsonify({'token': token}), 200
    return jsonify({'msg': 'Invalid credentials'}), 401

@routes.route('/promo/create', methods=['POST'])
@jwt_required()
def create_promo():
    data = request.json
    brand_id = get_jwt_identity()

    if not data.get('code') or not data.get('description'):
        return jsonify({'msg': 'Missing code or description'}), 400

    new_promo = PromoCode(
        code=data['code'],
        description=data['description'],
        brand_id=brand_id
    )

    db.session.add(new_promo)
    db.session.commit()

    return jsonify({'msg': 'Promo code created'}), 201

