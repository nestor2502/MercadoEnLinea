from flask import Flask
from flask_login import LoginManager

from .config import Config



login_manager = LoginManager()
login_manager.login_view = 'user.login'

from .user import user
from .products import products

from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(user)
    app.register_blueprint(products)
    return app