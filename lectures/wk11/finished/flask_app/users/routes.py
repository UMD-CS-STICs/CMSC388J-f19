from flask import render_template, url_for, redirect, request, current_app, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required

from flask_app import db, bcrypt
from flask_app.models import User, Post
from flask_app.users.forms import RegistrationForm, LoginForm, UpdateForm

import qrcode
import qrcode.image.svg as svg

from io import BytesIO

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()

        # return redirect(url_for('users.login'))
        session['reg_username'] = user.username

        return redirect(url_for('users.tfa'))
    
    return render_template('register.html', title='Register', form=form)


@users.route("/tfa")
def tfa():
    if 'reg_username' not in session:
        return redirect(url_for('main.index'))

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    return render_template('tfa.html'), headers

@users.route("/qr_code")
def qr_code():
    if 'reg_username' not in session:
        return redirect(url_for('main.index'))
    
    user = User.query.filter_by(username=session['reg_username']).first()

    session.pop('reg_username')

    img = qrcode.make(user.get_auth_uri(), image_factory=svg.SvgPathImage)

    stream = BytesIO()

    img.save(stream)

    headers = {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    return stream.getvalue(), headers


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('users.account'))

    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    username = current_user.username
    logout_user()
    current_app.logger.info('%s logged out successfully', username)
    return redirect(url_for('main.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()

    if form.validate_on_submit():
        current_user.username = form.username.data

        db.session.commit()

        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
    
    return render_template('account.html', title='Account', form=form)