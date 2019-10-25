from flask import render_template, url_for, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from flask_app import app, db, bcrypt
from flask_app.models import User, Post
from flask_app.forms import RegistrationForm, LoginForm, UpdateForm


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('account'))

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()

    if form.validate_on_submit():
        current_user.username = form.username.data

        db.session.commit()

        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
    
    return render_template('account.html', title='Account', form=form)


@app.route("/user/<username>")
def user_detail(username):
    user = User.query.filter_by(username=username).first()

    return render_template('user_detail.html', user=user)

@app.route("/")
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')