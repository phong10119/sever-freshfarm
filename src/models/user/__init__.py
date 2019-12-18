from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String)
    password = db.Column(db.String)
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(256), unique=True)
    address = db.Column(db.String)
    gender = db.Column(db.String)
    name = db.Column(db.String(256))
    img_url = db.Column(db.String())
    store = db.Column(db.Boolean, default=False)
    store_name = db.Column(db.String)
    product_own = db.relationship('Product', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def jsonize(self):
        return {
            "id" : self.id,
            "login_name": self.login_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "gender": self.gender,
            "name": self.name,
            "img_url": self.img_url,
            "store": self.store,
            "store_name": self.store_name,
        }

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)


# setup login manager
login_manager = LoginManager()


@login_manager.user_loader
def load_user(a):
    print(User,a)
    b = User.query.get(1)
    print(b)
    return User.query.get(a)

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user
    return None

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_item = db.relationship('Order_item', backref='order', lazy = True)
    ship = db.relationship('Shipment', backref='order', lazy = True)
    invoice = db.relationship('Invoice', backref='order', lazy = True)

class Order_item(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer)
    date_of_sell = db.Column(db.Date)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    order_status_id = db.Column(db.Integer, db.ForeignKey('order_statuses.id'), default=5)


    def jsonize(self):
        return {
            "id" : self.id,
            "user_id" : self.order.user_id,
            "product_id" : self.product_id,
            "product" : self.product.name,
            "order_status" : self.status.status,
            "quantity" : self.quantity,
            "total_price" : self.total_price,
            "img_url" : self.product.img_url
        }

class Order_status(db.Model):
    __tablename__ = 'order_statuses'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    order_id = db.relationship('Order_item', backref='status', lazy=True)