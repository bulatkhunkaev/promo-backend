from db import db

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    channel = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=False)
    topic = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class PromoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
