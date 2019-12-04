from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from src.models.product import Product, Inventory, Inventory_item, Rating, rating_count, Category, Store
from src.models.user import db

product_blueprint = Blueprint('productbp', __name__)

@product_blueprint.route('/', methods=['GET'])
def get_all_product():
    products = Product.query.filter_by(active=True).all()

    products_as_dict = []

    for product in products:
        product_as_dict = {
            'name' : product.name,
            'discription' : product.discription,
            'img_url' : product.img_url,
            'price' : product.price,
            'inventory_item_id': product.inventory_item_id,
            'category_id' : product.category_id,
            'location' : product.inventory_item.inventory.location,
            'store' : product.inventory_item.store.name,
            'stock' : product.inventory_item.stock,
            'active' : product.active
        }
        products_as_dict.append(product_as_dict)
    print(products_as_dict)
    return jsonify(products_as_dict)

@product_blueprint.route('/category/<category_id>', methods=['GET'])
def get_fruit(category_id):
    fruits = Product.query.filter_by(
        active=True,
        category_id=category_id
        ).all()

    fruits_as_dict = []

    for fruit in fruits:
        fruit_as_dict = {
            'id' : fruit.id,
            'name' : fruit.name,
            'discription' : fruit.discription,
            'img_url' : fruit.img_url,
            'price' : fruit.price,
            'inventory_item_id': fruit.inventory_item_id,
            'category_id' : fruit.category_id,
            'location' : product.inventory_item.inventory.location,
            'store' : product.inventory_item.store.name,
            'stock' : product.inventory_item.stock,
            'active' : fruit.active
        }
        fruits_as_dict.append(fruit_as_dict)
    return jsonify(fruits_as_dict)

@product_blueprint.route('/<id>', methods=['POST', 'GET'])
def product(id):
    product = Product.query.get(id)
    print(product)
    if request.method == 'POST':
        order = Order.query.filter_by(user_id=current_user.id)
        new_order_item = Order_item(order_id=order.id, product_id=id, quantity=request.form['quantity'])
        db.sesssion.add(new_order_item)
        db.session.commit()
        print('added to cart')
        return jsonify({'head' : 'added to cart'})
    return jsonify({
            'id' : product.id,
            'name' : product.name,
            'discription' : product.discription,
            'img_url' : product.img_url,
            'price' : product.price,
            'unit' : product.unit,
            'inventory_item_id': product.inventory_item_id,
            'category_id' : product.category_id,
            'location' : product.inventory_item.inventory.location,
            'store' : product.inventory_item.store.name,
            'stock' : product.inventory_item.stock,
            'active' : product.active
        })
