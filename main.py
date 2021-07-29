from flask import request, jsonify, make_response, render_template, send_from_directory
from flask_login import login_required, current_user

from app import create_app

app = create_app()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/uploads/<filename>')
@login_required
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
