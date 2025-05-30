from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config
from db import db
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
