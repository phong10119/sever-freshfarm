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
    active = db.Column(db.Boolean, default=True)
    stock = db.Column(db.Integer)
    time = db.Column(db.Date)
    expired_date = db.Column(db.Date)

    rating = db.relationship('Rating', backref='product', lazy=True)
    order_item = db.relationship('Order_item', backref='product', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    user_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def jsonize(self):
        return {
            "id": self.id,
            "name": self.name,
            "discription": self.discription,
            "img_url": self.img_url,
            "price": self.price,
            "active": self.active,
            "stock": self.stock,
            "time": self.time,
            "expired_date": self.expired_date,
            "category_id": self.category_id,
            "inventory": self.inventory.location,
            "store_name": self.user.store_name,
            "user_owner_id": self.user_owner_id
        }
class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    product = db.relationship('Product', backref='inventory', lazy=True)
    location = db.Column(db.String, unique=True) 
    
class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    product = db.relationship('Product', backref='category', lazy=True)

