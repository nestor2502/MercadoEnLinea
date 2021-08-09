from math import prod
from flask import render_template, redirect, url_for, request, jsonify
from flask.helpers import flash
from flask_login import current_user, login_required

from . import products
from app.products import products_ctrl
from app.user import user_ctrl

@products.route('/home', methods = ['GET'])
@login_required
def home():
    role = user_ctrl.get_user_role()
    if role == 'Comprador': 
        products = products_ctrl.get_top_products()
        return render_template('home-buyer.html', products = products, role = role)
    elif role == 'Vendedor':
        products = products_ctrl.get_my_products()
        return render_template('homeSeller.html', products = products, role = role)


@products.route('/upload_product', methods = ['GET','POST'])
@login_required
def upload_product():
    role = user_ctrl.get_user_role()
    if role != "Vendedor":
        return render_template('404-error.html')
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_filepath = request.files['image']

        if products_ctrl.upload_product(name, price, description, image_filepath):
            return redirect(url_for('products.home'))
    return render_template('add-update-product.html', role=role)



@products.route('/update_product/<id_product>', methods = ['GET','POST'])
@login_required
def update_product(id_product):
    role = user_ctrl.get_user_role()
    if role != "Vendedor":
        return render_template('404-error.html')

    if not products_ctrl.verify_product(id_product):
        return render_template('404-error.html')

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        available = request.form.get('available')
        image_filepath = request.files['image']

        if products_ctrl.update_product(id_product, name, price, description, available, image_filepath):
            return redirect(url_for('products.home'))

    product = products_ctrl.get_product(id_product)
    image = product.photo
    name = product.name
    price = product.price
    description = product.description
    available = "on" if product.available else "off"

    return render_template('add-update-product.html', role=role, id_product=id_product,
            image=image, name=name, price=price, description=description, available=available)

@products.route('/delete_product/<id_product>', methods = ['GET'])
@login_required
def delete_product(id_product):
    if user_ctrl.get_user_role() != "Vendedor":
        return render_template('404-error.html')
    if not products_ctrl.verify_product(id_product):
        return render_template('404-error.html')
    products_ctrl.delete_product(id_product)
    return redirect(url_for('products.home'))   

@products.route('/search', methods = ['GET'])
@login_required
def search_product():
    role = user_ctrl.get_user_role()
    name = request.args.get("name")
    products = products_ctrl.search_product(name)
    return render_template('home.html', search_products=products, role=role)

@products.route('/buy_product/<product_id>', methods = ['GET'])
@login_required
def buy_product(product_id):
    if request.method == 'GET':
        if user_ctrl.get_user_role() != "Comprador":
            return render_template('404-error.html')
        products_ctrl.buy_product(product_id)
        return redirect(url_for('products.home'))   


@products.route('/getProduct', methods = ['GET'])
@login_required
def getProduct():
    if request.method == 'GET':
        if user_ctrl.get_user_role() != "Comprador":
            return render_template('404-error.html')
        product_id = request.args.get("product_id")
        product = products_ctrl.get_product(product_id)
        return render_template('product-detail.html', product=product)

@products.route('/rate_product/<id_product>', methods = ['POST'])
@login_required
def rate_product(id_product):
    if request.method == 'POST':
        if user_ctrl.get_user_role() != "Comprador":
            return render_template('404-error.html')
        rate_description = request.form['rate_description']
        products_ctrl.add_rate_product(product_id, rate_description)
        return render_template('home.html')

@products.route('/my-shopping', methods = ['GET'])
@login_required
def get_my_shopping():
    role = user_ctrl.get_user_role()
    return render_template('my-shopping.html', role = role)






