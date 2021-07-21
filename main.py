from flask import request, jsonify, make_response, render_template
from flask_login import login_required, current_user

from app import create_app

app = create_app()


@app.route('/')
def index():
    return "owo"