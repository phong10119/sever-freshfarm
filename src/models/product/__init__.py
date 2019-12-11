from flask_login import UserMixin, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    discription = db.Column(db.String)
    img_url = db.Column(db.String)
    price = db.Column(db.Integer)
    unit = db.Column(db.String)
    order_item = db.relationship('Order_item', backref='product', lazy=True)
    buyer = db.relationship('User', backref='product', lazy=True)
    rating = db.relationship('Rating', secondary='rating_count', backref='product', lazy=True)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    active = db.Column(db.Boolean, default=True)

class Inventory_item(db.Model):
    __tablename__ = 'inventory_items'
    id = db.Column(db.Integer, primary_key=True)
    product = db.relationship('Product', backref='inventory_item', lazy=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    stock = db.Column(db.Integer)
    time = db.Column(db.Date)
    expired_date = db.Column(db.Date)
    
class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    inventory_item = db.relationship('Inventory_item', backref='inventory', lazy=True)
    location = db.Column(db.String, unique=True) 
    
class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

rating_count = db.Table('rating_count',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('rating_id', db.Integer, db.ForeignKey('ratings.id'), primary_key=True)
 )

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    product = db.relationship('Product', backref='category', lazy=True)

class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    inventory_item = db.relationship('Inventory_item', backref='store', lazy=True)
    login_name = db.Column(db.String)
    password = db.Column(db.String)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)