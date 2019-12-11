from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required, logout_user, login_user
from src.models.user import db, User, OAuth, Token, Order, Order_item, Order_status
from src.models.product import Product, Inventory, Inventory_item, Rating, rating_count, Category, Store
from src.models.trading import Shipment, Invoice, Invoice_status, Payment
import uuid

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
    # return redirect("https://127.0.0.1:3000/")

@user_blueprint.route("/get_user")
def get_user():
    if current_user.is_authenticated:
        return jsonify({
            "id" : current_user.id,
            "login-name" : current_user.login_name,
            "name": current_user.name,
            "phone" : current_user.phone,
            "email" : current_user.email,
            "address" : current_user.address,
            "gender" : current_user.gender
        })
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
    return jsonify({"state": "fail"})

@user_blueprint.route('/login', methods=['OPTIONS', 'POST'])
def login():
    if request.method == 'POST':
        check_user = User.query.filter_by(login_name=request.get_json(force=True)['username']).first()
        if check_user:
            if check_user.check_password(request.get_json(force=True)['password']):
                token = Token.query.filter_by(user_id = check_user.id).first()
                if not token:
                    token = Token(user_id= check_user.id, uuid=str(uuid.uuid4().hex))
                    db.session.add(token)
                    db.session.commit()
                    print('token', token)
                print('token', token)
                login_user(check_user)
                return jsonify({
                    "id" : current_user.id,
                    "login_name" : current_user.login_name,
                    "name": current_user.name,
                    "phone" : current_user.phone,
                    "email" : current_user.email,
                    "address" : current_user.address,
                    "gender" : current_user.gender,
                    "token" : token.uuid,
                    "state" : "success"
                })
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
    order = Order.query.filter_by(user_id=current_user.id).first()
    if not order:
        new_order = Order(user_id = current_user.id)
        db.session.add(new_order)
        db.session.commit()
        order = new_order
    order_item = Order_item.query.filter_by(
        product_id=request.get_json(force=True)['product_id'],
        order_id=order.id,
        order_status_id=1
        ).first()
    if not order_item:
        new_order_item = Order_item(order_id=order.id, product_id=request.get_json(force=True)['product_id'], quantity=request.get_json(force=True)['quantity'], total_price=request.get_json(force=True)['total_price'])
        db.session.add(new_order_item)
        db.session.commit()
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
        order_status_id=1
        ).all()
    for order_item in order_items:
        order_item.order_status_id = 2
        db.session.commit()
    return jsonify({"order_items":[order_item.jsonize() for order_item in order_items]}) 
