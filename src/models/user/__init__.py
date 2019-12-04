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
    admin = db.Column(db.Boolean, default=False)
    address = db.Column(db.String)
    gender = db.Column(db.Boolean)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256), unique=True)
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


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
    Order_status_id = db.Column(db.Integer, db.ForeignKey('order_status_ids.id'))
    ship = db.relationship('Shipment', backref='order', lazy = True)
    invoice = db.relationship('Invoice', backref='order', lazy = True)

class Order_item(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Order_status_id(db.Model):
    __tablename__ = 'order_status_ids'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    order_id = db.relationship('Order', backref='status', lazy=True)