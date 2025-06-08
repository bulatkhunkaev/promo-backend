from flask import Blueprint, request, jsonify
from db import db
from models import Brand, PromoCode
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

routes = Blueprint('routes', __name__)
bcrypt = Bcrypt()

@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if Brand.query.filter_by(login=data['login']).first():
        return jsonify({'error': 'Login already exists'}), 400
    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    brand = Brand(
        name=data['name'],
        channel=data['channel'],
        avatar=data.get('avatar'),
        topic=data.get('topic'),
        email=data['email'],
        login=data['login'],
        password_hash=hashed
    )
    db.session.add(brand)
    db.session.commit()
    return jsonify({'message': 'Brand registered successfully'}), 201

@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    brand = Brand.query.filter_by(login=data['login']).first()
    if brand and bcrypt.check_password_hash(brand.password_hash, data['password']):
        token = create_access_token(identity=str(brand.id), expires_delta=datetime.timedelta(days=1))
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@routes.route('/promo/create', methods=['POST'])
@jwt_required()
def create_promo():
    brand_id = int(get_jwt_identity())  # ✅ строка → число
    data = request.get_json()
    promo = PromoCode(
        code=data['code'],
        description=data.get('description'),
        brand_id=brand_id
    )
    db.session.add(promo)
    db.session.commit()
    return jsonify({'message': 'Promo created'}), 201

