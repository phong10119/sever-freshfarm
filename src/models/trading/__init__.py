from flask_login import UserMixin, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import db

class Shipment(db.Model):
    __tablename__ = 'shipments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    invoice_status_id = db.Column(db.Integer, db.ForeignKey('invoice_statuses.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))

class Invoice_status(db.Model):
    __tablename__ = 'invoice_statuses'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    invoice_id = db.relationship('Invoice', backref='invoice_status', lazy=True)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    invoice_id = db.relationship('Invoice', backref='payment', lazy=True)


