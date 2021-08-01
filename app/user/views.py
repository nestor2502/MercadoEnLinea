from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from flask_login.utils import login_user, logout_user

from . import user
from app.user import user_ctrl

@user.route('/signin', methods = ['POST', 'GET'])
def signin():

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        role = request.form['role']
        phone = request.form['phone']

        if user_ctrl.signin(email, name, phone, role):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('user.signin'))
    return render_template('signin.html')

@user.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('products.home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if user_ctrl.login(email,password):
            return redirect(url_for('products.home'))
        else:
            return redirect(url_for('user.login'))
    return render_template('login.html')

@user.route('/logout')
@login_required
def logout():
    user_ctrl.logout()
    return redirect(url_for('user.login'))
