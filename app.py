from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from db import db
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)

# ✅ Разрешаем CORS для всех доменов
CORS(app, resources={r"/*": {"origins": "*"}})

JWTManager(app)
db.init_app(app)
app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
