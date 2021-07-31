from flask import Flask
from flask_login import LoginManager

from .config import Config

import pathlib, os

UPLOAD_FOLDER = str(pathlib.Path(__file__).parent.resolve()).split("app")[0]+"/uploaded_images"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
MAXIMUM_FILE_SIZE = 16 * 1024 * 1024

login_manager = LoginManager()
login_manager.login_view = 'user.login'

from .user import user
from .products import products

from app.models import db

def create_app():
    create_dir(UPLOAD_FOLDER)
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAXIMUM_FILE_SIZE
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(user)
    app.register_blueprint(products)
    return app

def create_dir(path_dir):
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
