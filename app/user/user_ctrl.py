from app.models import *
from flask import jsonify, flash, session
from flask_login.utils import login_user, logout_user, current_user
from app.models import db

import re, secrets, string, pathlib
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_html(password):
    """Obtains the email template used in the send_email() function.

    Parameters
    ----------
    password : str
        The User's new password to be sended via email

    Returns
    -------
    str
        body, the email template.
    """
    email_path = str(pathlib.Path(__file__).parent.resolve()).split("/user")[0]+"/templates/email-template.html"
    body = ""
    with open(email_path, 'r') as reader:
        for line in reader.readlines():
            if "<b>#PASSWORD#</b>" in line:
                body += line.replace("<b>#PASSWORD#</b>", f"<b>{password}</b>")
            else:
                body += line
    return body



def create_password():
    """Creates a random password for the new user.

    Parameters
    ----------
    Any

    Returns
    -------
    str
        Password, the user's new password
    """
    password = ""
    for _ in range(10):
        password += secrets.choice(string.ascii_lowercase)
    password += secrets.choice(string.digits)
    password += secrets.choice(string.ascii_uppercase)
    return password

def send_email(receiver_email, password):
    """Sends an email to the new user with their new password.

    Parameters
    ----------
    email : str
        The User's email
    password : str
        The User's password

    Returns
    -------
    str
        Password, the user's password
    """

    #TODO Find a way to not display mercado en linea email's password in the code

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "mercadoenlinea.is21@gmail.com"
    sender_pass = "y$ny2s4GfG"

    subject = "Correo de verificación"

    html = MIMEText(get_html(password), "html")
    plain = MIMEText('', 'plain')
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    message.attach(plain)
    message.attach(html)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return password

def is_valid_email(email):
    """Using regex checks if an email is valid

    Parameters
    ----------
    email : str
        The User's email

    Returns
    -------
    boolean
        True if the email is valid
        False if the email is invalid
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

def signin(email, name, phone, role):
    """Creates a new user and sends an email with the user's password.

    Parameters
    ----------
    email : str
        The User's email
    name : str
        The User's name
    phone : str
        The User's phone
    role : str
        The User's role

    Returns
    -------
    boolean
        True if the user was successfully registered
        False if a issue happened, uses flask's flash feature to display the issue to the user.
    """
    if not is_valid_email(email):
        flash("Email incorrecto, intenta con otro",'error')
        return False
    
    already_registered = User.query.filter_by(email = email).first()
    if already_registered is not None:
        flash("Ya existe un usuario con ese correo, por favor intenta con uno nuevo.",'error')
        return False
    
    #Checks if a role exists.
    #For developing purposes a role is created
    #TODO Delete role creation and flash a error message

    registered_role = Role.query.filter_by(name = role).first()

    password = create_password()
    send_email(email, password)
    
    if registered_role is not None:
        new_user = User(name, email, phone, password)
        registered_role.users.append(new_user)
        db.session.add(registered_role)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Usuario registrado exitosamente, tu contraseña llegará al correo: {email}.",'success')
    else:
        new_role = Role(role)
        db.session.add(new_role)
        db.session.commit()
        new_user = User(name, email, phone, password)
        new_role.users.append(new_user)
        db.session.add(new_role)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Usuario registrado exitosamente, tu contraseña llegará al correo: {email}.",'success')
        flash(f"Se creo el siguiente rol: {role}.",'success')
    return True

        

def login(email, password):
    """Checks if there is an existent user and then if the password is correct, finally
       log ins the user

    Parameters
    ----------
    email : str
        The User's email
    password : str
        The User's password

    Returns
    -------
    boolean
        True if the user was successfully logged
        False if a issue happened, flask's flash feature is used to display the issue to the user.
    """
    try:
        registered_user = User.query.filter_by(email = email).first()
    except Exception as e:
        print(e)
        flash('Ocurrió un error, intente más tarde.','error')
        return False
    if registered_user is not None and registered_user.verify_password(password):
        login_user(registered_user)
        return True
    else:
        flash('Email o contraseña incorrectos, intente nuevamente.','error')
        return False


def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        # prevent flashing automatically logged out message
        del session['was_once_logged_in']
    flash('Cerraste sesión exitosamente', 'success')
    return True

def get_user_role():
    return Role.query.filter_by(id = current_user.role_id).first().name