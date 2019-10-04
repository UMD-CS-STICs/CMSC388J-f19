from flask_app import app, db, bcrypt
from flask_app.data import posts
from flask_app.forms import LoginForm, RegistrationForm
from flask_app.models import User, Post, Comment

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def index():
    # if current_user.is_authenticated:
    #     return render_template('index.html', posts=posts, user=current_user)    
    return render_template('index.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    


@app.route('/login', methods=['GET', 'POST'])
def login():

@app.route('/logout')
def logout():

@app.route('/profile')
@login_required
def account():

