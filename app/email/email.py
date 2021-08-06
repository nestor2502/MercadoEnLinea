from app.models import *
import smtplib, ssl, pathlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_signin_email(user_email, password):
    """Obtains the email template used in the send_email() function.

    Parameters
    ----------
    user_email : str
        The User's email

    password : str
        The User's new password to be sent via email

    Returns
    -------
    str
        body, the email template.
    """
    email_path = str(pathlib.Path(__file__).parent.resolve()).split("/email")[0]+"/templates/email-signin.html"
    body = ""
    with open(email_path, 'r') as reader:
        for line in reader.readlines():
            if "<b>#PASSWORD#</b>" in line:
                body += line.replace("<b>#PASSWORD#</b>", f"<b>{password}</b>")
            else:
                body += line
    send_email(user_email,"Correo de Verificación", body)

def send_buyorder_email(user_email, product, order, seller_name):
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
    email_path = str(pathlib.Path(__file__).parent.resolve()).split("/email")[0]+"/templates/email-buyorder.html"
    body = ""
    with open(email_path, 'r') as reader:
        for line in reader.readlines():
            if "(Order_ID)" in line:
                body += line.replace("(Order_ID)", str(order.id))
            elif "(Order_Date)" in line:
                body += line.replace("(Order_Date)", str(order.date))
            elif "(Product_Name)" in line:
                body += line.replace("(Product_Name)", product.name)
            elif "(Product_Price)" in line:
                body += line.replace("(Product_Price)", str(product.price))
            elif "(Product_Description)" in line:
                body += line.replace("(Product_Description)", product.description).replace("(Seller_Name)", seller_name)
            else:
                body += line
    send_email(user_email,f"Confirmación de compra #{order.id}", body)


def send_email(receiver_email, subject, body):
    """Sends an email 

    Parameters
    ----------
    receiver_email : str
        The User's email
    subject : str
        The emails subject
    body : str
        The emails body

    Returns
    -------
    Any
    """

    #TODO Find a way to not display mercado en linea email's password in the code

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "mercadoenlinea.is21@gmail.com"
    sender_pass = "y$ny2s4GfG"


    html = MIMEText(body, "html")
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
