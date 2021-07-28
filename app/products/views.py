from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from . import products
from app.products import products_ctrl

@products.route('/home', methods = ['GET'])
@login_required
def home():
    return render_template('home.html') 


@products.route('/upload_product', methods = ['GET','POST'])
@login_required
def upload_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_filepath = request.files['image']
        products_ctrl.upload_product(name, price, description, image_filepath)

        return render_template('add-product.html', image = products_ctrl.get_product_image_filename(name))    
        
    return render_template('add-product.html')


    