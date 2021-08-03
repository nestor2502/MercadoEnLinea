from hashlib import new
from app.models import *
from flask import jsonify, flash, current_app
from flask_login.utils import current_user
from app.models import db
from app import ALLOWED_EXTENSIONS

import os, string, random

def get_product_image_filename(name):
    for product in current_user.products:
        if product.name == name:
            return product.photo
    return ""

def get_product(id_product):
    product = Product.query.get(id_product)
    return product

def verify_product(id_product):
    # check if the product exists and belongs to the current user
    product = get_product(id_product)
    if (id_product is None or product is None):
        return False
    if product.user_id != current_user.id:
        return False
    return True

def get_secure_filename(filename):
    return f"{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))}.{filename.rsplit('.', 1)[1].lower()}"

def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_product(name, price, description, image_file):
    if name == '' or price == '' or description == '' or image_file.filename == '':
        flash("Campos incompletos, por favor llene todos los campos.","error")
        return False;

    if image_file and allowed_extension(image_file.filename):
        for product in current_user.products:
            if product.name == name:
                flash("Producto ya existente.","error")
                return False
        new_product = Product(name, description, price,"")
        secure_filename = get_secure_filename(image_file.filename)
        new_product.photo = secure_filename
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename)
        image_file.save(image_path)
        current_user.products.append(new_product)
        db.session.add(new_product)
        db.session.commit()
        flash("Producto agregado exitosamente.","success")
        return True
    else:
        flash("Extensión incorrecta, extensiones permitidas: png|jpg|jpeg","error")
        return False

def update_product(id_product, name, price, description, image_file):
    if name == '' or price == '' or description == '':
        flash("Campos incompletos, por favor llene todos los campos","error")
        return False;

    product = Product.query.get(id_product)
    product.name = name
    product.price = price
    product.description = description
    db.session.commit()

    if image_file and image_file.filename != "":
        if allowed_extension(image_file.filename):
            old_image = os.path.join(current_app.config['UPLOAD_FOLDER'], product.photo)

            secure_filename = get_secure_filename(image_file.filename)
            product.photo = secure_filename
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename)
            image_file.save(image_path)
            db.session.commit()
            if os.path.isfile(old_image):
                os.remove(old_image)

            flash("Producto editado exitosamente.","success")
            return True
        else:
            flash("Extensión incorrecta, extensiones permitidas: png|jpg|jpeg","error")
            return False

    flash("Producto editado exitosamente.","success")
    return True

def get_top_products():
    return Product.query.all()

def get_my_products():
    return Product.query.filter((Product.user_id == current_user.id))

def delete_product(id_product):
    try:
        Product.query.filter_by(id=id_product).delete()
        db.session.commit()
        flash("Producto eliminado exitosamente.","success")
        return True
    except Exception as e:
        print(e)
        flash('Ocurrió un error al intentar eliminar el producto, intente más tarde.','error')
        return False
