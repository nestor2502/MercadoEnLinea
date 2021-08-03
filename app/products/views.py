from flask import render_template, redirect, url_for, request, jsonify
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
    elif role == 'Vendedor':
        products = products_ctrl.get_my_products()
    return render_template('home.html', products = products, role = role)
    #return render_template('home.html', role = role) 


@products.route('/upload_product', methods = ['GET','POST'])
@login_required
def upload_product():
    if user_ctrl.get_user_role() != "Vendedor":
        return render_template('404-error.html')
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_filepath = request.files['image']

        if products_ctrl.upload_product(name, price, description, image_filepath):
            return redirect(url_for('products.home'))
    return render_template('add-update-product.html')



@products.route('/update_product/<id_product>', methods = ['GET','POST'])
@login_required
def update_product(id_product):
    if user_ctrl.get_user_role() != "Vendedor":
        return render_template('404-error.html')
    id_product = id_product #request.args.get('id')
    if not products_ctrl.verify_product(id_product):
        return render_template('404-error.html')
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_filepath = request.files['image']

        if products_ctrl.update_product(id_product, name, price, description, image_filepath):
            return redirect(url_for('products.home'))

    product = products_ctrl.get_product(id_product)
    image = product.photo
    name = product.name
    price = product.price
    description = product.description
    return render_template('add-update-product.html', id_product=id_product, image=image, name=name, price=price, description=description)    

@products.route('/delete_product/<id_product>', methods = ['GET'])
@login_required
def delete_product(id_product):
    products_ctrl.delete_product(id_product)
    return redirect(url_for('products.home'))   
    


