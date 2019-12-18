from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required, logout_user, login_user
from src.models.user import db, User, OAuth, Token, Order, Order_item, Order_status
from src.models.product import Product, Inventory, Rating, Category
from src.models.trading import Shipment, Invoice, Invoice_status, Payment
import uuid
from datetime import date

import os
from dotenv import load_dotenv
load_dotenv()
import stripe

user_blueprint = Blueprint('userbp', __name__)

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}
stripe.api_key = stripe_keys['secret_key']

@user_blueprint.route("/logout", methods=['POST'])
@login_required
def logout():
    token = Token.query.filter_by(user_id = current_user.id).first()
    if token:
        db.session.delete(token)
        db.session.commit()
    logout_user()
    flash("You have logged out")
    return jsonify({'success': "true"})
    # return redirect("https://freshfarm-ecomerce.netlify.com/")

@user_blueprint.route("/get_user")
def get_user():
    if current_user.is_authenticated:
        return jsonify(current_user.jsonize())
    return jsonify({'id': 'Anomynous'})

@user_blueprint.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if current_user.is_authenticated:
        print("not need to register")
    if request.method == "POST":
        # import code; code.interact(local=dict(globals(), **locals()))
        check_user = User.query.filter_by(email = request.get_json(force=True)['email']).first()
        if not check_user:
            new_user = User(login_name = request.get_json(force=True)['username'], email = request.get_json(force=True)['email'])
            new_user.set_password(request.get_json(force=True)['password'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"state": "success"})
        return jsonify({"state": "user already exist"})
    return jsonify({"state": "fail"})

@user_blueprint.route('/login', methods=['OPTIONS', 'POST'])
def login():
    if request.method == 'POST':
        check_user = User.query.filter_by(login_name=request.get_json(force=True)['username']).first()
        if check_user:
            if check_user.check_password(request.get_json(force=True)['password']):
                token = Token.query.filter_by(user_id = check_user.id).first()
                if not token:
                    new_token = Token(user_id= check_user.id, uuid=str(uuid.uuid4().hex))
                    db.session.add(new_token)
                    db.session.commit()
                    token =  new_token
                    print('token', token)
                print('token', token)
                login_user(check_user)
                return jsonify({"currentUser": check_user.jsonize(), "state": "success", "token": token.uuid})
            print('wrong password')
            return jsonify({"state": "WrongPass"})
        print('no user')
        return jsonify({"state": "NoUser"})

@user_blueprint.route('/change_profile', methods=['POST'])
@login_required
def change_profile():
    editted_user = current_user
    editted_user.name = request.get_json(force=True)['name']
    editted_user.email = request.get_json(force=True)['email']
    editted_user.phone = request.get_json(force=True)['phone']
    editted_user.address = request.get_json(force=True)['address']
    editted_user.gender = request.get_json(force=True)['gender']
    db.session.commit()
    return jsonify({'state':'success'})

@user_blueprint.route('/get_order')
@login_required
def get_order():
    order = Order.query.filter_by(user_id=current_user.id).first()
    if not order:
        new_order = Order(user_id = current_user.id)
        db.session.add(new_order)
        db.session.commit()
        order = new_order
    order_items = Order_item.query.filter_by(order_id=order.id).all()
    return jsonify({"order_items":[order_item.jsonize() for order_item in order_items]})

@user_blueprint.route('/create_order_item', methods=['POST'])
@login_required
def create_order_item():
    # import code; code.interact(local=dict(globals(), **locals()))
    order = Order.query.filter_by(user_id=current_user.id).first()
    if not order:
        new_order = Order(user_id = current_user.id)
        db.session.add(new_order)
        db.session.commit()
        order = new_order
    order_item = Order_item.query.filter_by(
        product_id=request.get_json(force=True)['product_id'],
        order_id=order.id,
        order_status_id=5
        ).first()
    if not order_item:
        new_order_item = Order_item(order_id=order.id, product_id=request.get_json(force=True)['product_id'], quantity=request.get_json(force=True)['quantity'], total_price=request.get_json(force=True)['total_price'])
        db.session.add(new_order_item)
        db.session.commit()
        order_item=new_order_item
    order_item.quantity=request.get_json(force=True)['quantity']
    order_item.total_price=request.get_json(force=True)['total_price']
    db.session.commit()

    order_items = Order_item.query.filter_by(order_id=order.id).all()
    return jsonify({"order_items":[order_item.jsonize() for order_item in order_items]})

@user_blueprint.route('/delete_order_item/<id>', methods=['DELETE'])
@login_required
def delete_order_item(id):
    Order_item.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'state': 'deleted'})

@user_blueprint.route('store/product', methods=['GET', 'POST'])
@login_required
def store_product():
    print(current_user.id)
    products = Product.query.filter_by(user_owner_id=current_user.id, active=True).all()

    return jsonify({"product":[product.jsonize() for product in products]}) 

@user_blueprint.route('/store/product/<id>', methods=['DELETE'])
@login_required
def delete_store_product(id):
    Product.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'state': 'deleted'})

@user_blueprint.route('/charge', methods=["POST"])
def charge():
    # LOI SAID REMEMEBR WHAT I DO
    # import code; code.interact(local=dict(globals(), **locals()))

    amount = request.get_json(force=True)['data']['total_amount']
    print('amount', amount)

    customer = stripe.Customer.create(
        email='sample@customer.com',
        source=request.get_json(force=True)['data']['token']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    order = Order.query.filter_by(user_id=current_user.id).first()
    order_items = Order_item.query.filter_by(
        order_id=order.id,
        order_status_id=5
        ).all()
    for order_item in order_items:
        product = Product.query.filter_by(id=order_item.product_id)
        order_item.order_status_id = 1
        order_item.date_of_sell = date.today().strftime("%Y/%m/%d")
        db.session.commit()
    return jsonify({"order_items":[order_item.jsonize() for order_item in order_items]}) 
