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

def get_secure_filename(filename):
    return f"{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))}.{filename.rsplit('.', 1)[1].lower()}"

def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_product(name, price, description, image_file):
    if image_file and allowed_extension(image_file.filename):
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
    print(id_product)
    print(name)
    print(price)
    print(description)
    if (id_product is None):
        flash("BAD REQUEST")
        return False
    if image_file and allowed_extension(image_file.filename):
        secure_filename = get_secure_filename(image_file.filename)
        #new_product.photo = secure_filename
        product = Product.query.get(id_product)
        product.name = name
        #image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename)
        #image_file.save(image_path)
        db.session.commit()
        flash("Producto editado exitosamente.","success")
        return True
    else:
        flash("Extensión incorrecta, extensiones permitidas: png|jpg|jpeg","error")
        return False
