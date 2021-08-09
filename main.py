from flask import request, jsonify, make_response, render_template, send_from_directory, redirect, url_for
from flask_login import login_required, current_user

from app import create_app

app = create_app()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('products.home'))
    return render_template("index.html")

@app.route('/uploads/<filename>')
@login_required
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404-error.html')