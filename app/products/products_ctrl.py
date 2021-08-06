from hashlib import new
from app.models import *
from flask import jsonify, flash, current_app
from flask_login.utils import current_user
from app.models import db
from app import ALLOWED_EXTENSIONS

import os, string, random

from app.email.email import send_buyorder_email

def get_product_image_filename(name):
    """
        Obtains the product filename from the current logged user.
     
        Parameters
        ----------
        name : str
            The products name

        Returns
        -------
        String
            The product filename or empty if its not found
    """
    for product in current_user.products:
        if product.name == name:
            return product.photo
    return ""

def get_product(id_product):
    """
        Obtains the product using its identifier.
     
        Parameters
        ----------
        id_product : int
            The products identifier

        Returns
        -------
        Product
            The product searched
    """
    product = Product.query.get(id_product)
    return product

def verify_product(id_product):
    """
        Check if the product exists and belongs to the current user
     
        Parameters
        ----------
        id_product : int
            The products identifier

        Returns
        -------
        Boolean
            True: Product exists and belongs to the current logged user.
            False: Otherwise.
    """
    product = get_product(id_product)
    if (id_product is None or product is None):
        return False
    if product.user_id != current_user.id:
        return False
    return True

def get_secure_filename(filename):
    """
        Creates a new and secure filename, using random characters.
        Identifies the filename extension.
     
        Parameters
        ----------
        filename : str
            The filename to sanitize

        Returns
        -------
        String
            The sanitized filename.
    """
    return f"{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))}.{filename.rsplit('.', 1)[1].lower()}"

def allowed_extension(filename):
    """
        Obtains the filename extension and checks if they are in the ALLOWED_EXTENSIONS
          list defined in init.py
     
        Parameters
        ----------
        filename : str
            The filename to check

        Returns
        -------
        Boolean
            True: If the filename extension is allowed
            False: If the filename extension is not allowed

    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_product(name, price, description, image_file):
    """Creates a new product, checks the security and integrity of the image file
        Also links the product to the seller.

    Parameters
    ----------
    name : str
        The Product's name
    price : int
        The Product's price
    description : str
        The Product's description
    image_file : FILE
        The Product's image

    Returns
    -------
    boolean
        True if the product was successfully created
        False if a issue happened, flask's flash feature is used to display the issue to the user.
    """
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
        #Creates the image path using FLASK app constant (defined in init.py)
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

def update_product(id_product, name, price, description, available, image_file):
    if name == '' or price == '' or description == '':
        flash("Campos incompletos, por favor llene todos los campos","error")
        return False;

    product = Product.query.get(id_product)
    product.name = name
    product.price = price
    product.description = description
    product.available = True if available == "on" else False
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

def buy_product(product_id):
    """Creates an Order and links it to the buyer an seller user, checks if the
        product is available and other alternate cases.
        Flashes if something went wrong and also if the transaction was successful.

    Parameters
    ----------
    product_id : int
        Product identifier

    Returns
    -------
        Any

    """
    product = get_product(product_id)

    if product is None or not product.available:
        flash('El producto no está disponible. \n Intente con otro producto.', 'error')
        return
    seller = User.query.filter_by(id = product.user_id).first()
    if seller is None:
        flash('Ocurrio un error', 'error')
        return
    order = Order()
    current_user.buyer_orders.append(order)
    seller.seller_orders.append(order)
    product.orders.append(order)
    db.session.add(order)
    db.session.commit()
    send_buyorder_email(current_user.email, product, order, seller.name)
    flash(f'La compra ha sido exitosa. \n Se ha mandado su orden de compra al correo: \n {current_user.email}','success')
    return