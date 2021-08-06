from flask_login import UserMixin
from passlib.apps import custom_app_context
from flask_sqlalchemy import SQLAlchemy


from app import login_manager

import datetime

db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(UserMixin,db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	email = db.Column(db.String(50), unique = True)
	phone = db.Column(db.String(20))
	password = db.Column(db.String(50))
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
	products = db.relationship('Product')
	seller_orders = db.relationship('Order', lazy = 'dynamic', foreign_keys = 'Order.seller_id')
	buyer_orders = db.relationship('Order', lazy = 'dynamic', foreign_keys = 'Order.buyer_id')

	def __repr__(self):
		return '<User %r>' % self.name
	
	def __init__(self, name, email, phone, password):
		self.name = name
		self.email = email
		self.phone = phone
		self.password = self.hash_password(password)
	
	def hash_password(self, password):
		return custom_app_context.encrypt(password)
		
	def verify_password(self, password):
		return custom_app_context.verify(password, self.password)

class Role(db.Model):
	__tablename__ = 'role'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	users = db.relationship("User")
	permissions = db.relationship("Permission")

	def __init__(self, name):
		self.name = name

class Permission(db.Model):
	__tablename__ = 'permission'
	name = db.Column(db.String(50), primary_key=True)
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

	def __init__(self, name):
		self.name = name

class Product(db.Model):
	__tablename__ = 'product'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	description = db.Column(db.String(120))
	available = db.Column(db.Boolean)
	price = db.Column(db.Float)
	photo = db.Column(db.String(10000))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	orders = db.relationship('Order')


	def __init__(self, name, description, price, photo):
		self.name = name
		self.description = description
		self.available = True
		self.price =  price
		self.photo = photo

class Order(db.Model):
	__tablename__ = 'order'
	id = db.Column(db.Integer, primary_key=True)
	stars = db.Column(db.Integer)
	review = db.Column(db.String(1000))
	date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

	def __init__(self, stars, review):
		self.stars = stars
		self.review = review
