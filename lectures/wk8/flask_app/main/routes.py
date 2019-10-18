from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from flask_app import app, db, bcrypt
from flask_app.models import User, Post

main = Blueprint('main', __name__)


@main.route("/")
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')