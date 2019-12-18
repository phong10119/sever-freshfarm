from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from src.models.product import Product, Inventory, Rating
from src.models.user import db, User, Order_item
from sqlalchemy import func
from datetime import datetime
product_blueprint = Blueprint('productbp', __name__)

@product_blueprint.route('/', methods=['GET'])
def get_all_product():
    products = Product.query.filter_by(active=True).all()

    return jsonify({"product":[product.jsonize() for product in products]}) 


@product_blueprint.route('/category/<category_id>', methods=['GET'])
def get_fruit(category_id):
    products = Product.query.filter_by(active=True, category_id=category_id).all()

    return jsonify({"product":[product.jsonize() for product in products]}) 
    

@product_blueprint.route('/<id>', methods=['POST', 'GET'])
def product(id):
    product = Product.query.get(id)
    
    if request.method == 'POST':
        order = Order.query.filter_by(user_id=current_user.id)
        new_order_item = Order_item(order_id=order.id, product_id=id, quantity=request.form['quantity'])
        db.sesssion.add(new_order_item)
        db.session.commit()
        print('added to cart')
        return jsonify({'head' : 'added to cart'})
    return jsonify(product.jsonize())

# @product_blueprint.route('/query', methods=['POST', 'GET'])
# def query():
#     product_name = request.get_json(force=True)['query']
#     price_min = request.get_json(force=True)['price']['min']
#     price_max = request.get_json(force=True)['price']['max']
#     ratings = request.get_json(force=True)['rating']

#     products1 = Product.query.filter(
#         Product.price > price_min,
#         Product.price < price_max
#     ).all()

#     result = []
#     if ratings:
#         for rating in ratings:
#             for product1 in products1:
#                 if round(product1.rating) == rating:
#                     if product1.active == True:
#                         if product1.name == product_name:
#                             result.append(product1)
#     for product1 in products1:
#         if product1.active == True:
#             if product1.name == product_name:
#                 result.append(product1)
    
#     return jsonify({"product":[product.jsonize() for product in result]}) 

@product_blueprint.route('/query', methods=['POST', 'GET'])
def query():
    product_name = request.get_json(force=True)['query']
    products = Product.query.filter_by(name=product_name, active=True).all()
    return jsonify({"product":[product.jsonize() for product in products]}) 

@product_blueprint.route('/<id>/rating', methods=['POST', 'GET'])
def rating(id):
    # import code; code.interact(local=dict(globals(), **locals()))

    ratings = Rating.query.filter_by(product_id=id).all()
    ratings_as_dict = []

    for rating in ratings:
        user_cmt = User.query.get(rating.user_id)
        rating_as_dict = {
            "id" : rating.id,
            "rating" : rating.rating,
            "comment" : rating.comment,
            "user_id" : rating.user_id,
            "user_name" : user_cmt.login_name,
            "user_avata" : user_cmt.img_url,
            "product_id" : rating.product_id
        }
        ratings_as_dict.append(rating_as_dict)
    if request.method == 'POST':
        rating = Rating.query.filter_by(
            user_id = current_user.id,
            product_id = id
        ).first()
        if rating:
            rating.comment = request.get_json(force=True)['userComment']
            rating.rating = request.get_json(force=True)['userRating']
            db.session.commit()
        new_rating = Rating(rating = request.get_json(force=True)['userRating'], comment = request.get_json(force=True)['userComment'], user_id=current_user.id, product_id=id)
        db.session.add(new_rating)
        db.session.commit()
        return jsonify({'state': 'success'})
    return jsonify(ratings_as_dict)
    
@product_blueprint.route('<id>/edit', methods=['POST'])
@login_required
def edit_product(id):
    product = Product.query.filter_by(id=request.get_json(force=True)['id']).first()
    product.name = request.get_json(force=True)['name']
    product.discription = request.get_json(force=True)['discription']
    product.price = request.get_json(force=True)['price']
    db.session.commit()
    return jsonify({'state': 'success'})

@product_blueprint.route('/get_sale')
@login_required
def get_sale():
    products = Product.query.filter_by(user_owner_id=current_user.id).all()
    print(products)
    result = []
    for product in products:
        record = Order_item.query.with_entities(func.sum(Order_item.total_price).label("total_price"), func.count(Order_item.total_price).label("count"), Order_item.date_of_sell).filter_by(product_id=product.id, order_status_id=1).group_by(Order_item.date_of_sell).all()
        for el in record:
           # result.append({'total_price': el.total_price,
              #              'count': el.count,
               #             'date': el.date_of_sell})
            try:
                index = [ x["date"] for x in result ].index(el.date_of_sell.strftime("%Y/%m/%d"))
                result[index]["total_price"] += el.total_price
                result[index]["count"] += el.count
            except Exception as Error:
                print(Error)
                result.append({"date": el.date_of_sell.strftime("%Y/%m/%d"), "count": 1, "total_price": el.total_price})
    result2 = []
    for product in products:
        record2 = Rating.query.with_entities(func.count(Rating.rating).label("count"), Rating.rating).filter_by(product_id=product.id).group_by(Rating.rating).all()
        for el in record2:
            try:
                index = [ x["rating"] for x in result2 ].index(el.rating)
                result2[index]["count"] += el.count
            except Exception as Error:
                print(Error)
                result2.append({"count": 1, "rating": el.rating})
    new_result2 = sorted(result2, key=lambda k: k['rating'])
    return jsonify({'sale': result,
                    'rating': new_result2})
            
