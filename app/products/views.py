from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from . import products

@products.route('/home', methods = ['GET'])
@login_required
def home():
    return render_template('home.html') 