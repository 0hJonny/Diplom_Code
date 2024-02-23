import os
from flask import Flask
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Настройки для JWT
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


# Имспорт авторизации для api
from .client import client_bp
app.register_blueprint(client_bp)


# Импорт api для работы с новостными статьями
from .api.v1 import api_v1_bp
app.register_blueprint(api_v1_bp, url_prefix='/api/v1')