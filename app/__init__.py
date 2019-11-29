from flask import Flask, redirect, url_for, flash, render_template, jsonify
from flask_login import login_required, logout_user, current_user
from .config import Config
from .models import db, login_manager, Token
from .oauth import blueprint
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


@app.route("/logout")
@login_required
def logout():
    token = Token.query.filter_by(user_id = current_user.id).first()
    if token:
        db.session.delete(token)
        db.session.commit()
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))

@app.route("/get_user")
@login_required
def get_user():
    return jsonify({
        "user_name": current_user.name
    })


@app.route("/")
def index():
    return render_template("home.html")
