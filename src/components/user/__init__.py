from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required, logout_user, login_user
from src.models.user import db, User, OAuth, Token, Order, Order_item, Order_status_id
from src.models.product import Product, Inventory, Inventory_item, Rating, rating_count, Category, Store
from src.models.trading import Shipment, Invoice, Invoice_status, Payment
import uuid

user_blueprint = Blueprint('userbp', __name__)

@user_blueprint.route("/logout")
@login_required
def logout():
    token = Token.query.filter_by(user_id = current_user.id).first()
    if token:
        db.session.delete(token)
        db.session.commit()
    logout_user()
    flash("You have logged out")
    # return jsonify({'head', 'logged out'})
    return redirect("https://127.0.0.1:3000/")

@user_blueprint.route("/get_user")
def get_user():
    return jsonify({
        "id" : current_user.id,
        "name": current_user.name,
        "phone" : current_user.phone,
        "email" : current_user.email,
        "address" : current_user.address,
    })

@user_blueprint.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if current_user.is_authenticated:
        print("not need to register")
    if request.method == "POST":
        # import code; code.interact(local=dict(globals(), **locals()))
        check_user = User.query.filter_by(email = request.get_json()['email']).first()
        if not check_user:
            new_user = User(login_name = request.get_json()['username'], email = request.get_json()['email'])
            new_user.set_password(request.get_json()['password'])
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
            # return redirect("https://127.0.0.1:3000/?api_key={}".format(token.uuid))
                return jsonify({
                    "id" : current_user.id,
                    "name": current_user.name,
                    "phone" : current_user.phone,
                    "email" : current_user.email,
                    "address" : current_user.address,
                    "login_name": check_user.login_name,
                    "token" : token.uuid ,
                    "state" : "success"
                })
            print('wrong password')
            return jsonify({"state": "WrongPass"})
        print('no user')
        return jsonify({"state": "NoUser"})



