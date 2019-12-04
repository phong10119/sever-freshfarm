from flask import Flask, redirect, url_for, flash, render_template, jsonify
from flask_login import login_required, logout_user, current_user
from .config import Config
from .models.user import db, login_manager, Token
from .components.oauth import blueprint
from .cli import create_db
from flask_cors import CORS
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(blueprint, url_prefix="/login")
CORS(app)
app.cli.add_command(create_db)
db.init_app(app)
login_manager.init_app(app)

migrate = Migrate(app, db)

from src.components.fakedata import fakedata_blueprint
app.register_blueprint(fakedata_blueprint, url_prefix='/fakedata')

from src.components.product import product_blueprint
app.register_blueprint(product_blueprint, url_prefix='/product')

from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')



@app.route("/")
def index():
    return render_template("home.html")

# @app.route("/get_hard_date")
# def hardcode():
    

