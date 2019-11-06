from flask import render_template, Blueprint

from flask_app.models import Post, User

main = Blueprint('main', __name__)

@main.route("/")
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/user/<username>")
def user_detail(username):
    user = User.query.filter_by(username=username).first()

    return render_template('user_detail.html', user=user)