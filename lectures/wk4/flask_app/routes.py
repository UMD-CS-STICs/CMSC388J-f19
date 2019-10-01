from flask_app import app, db
from flask import render_template, request, redirect, url_for
from flask_app.data import posts
from flask_app.models import *

@app.route('/')
@app.route('/index')
def index():
    print(Users.query.all())
    return render_template('index.html', title='Front page')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user/<username>')
def profile(username):
    return render_template('user.html', username=username)

@app.route('/feed')
def feed():
    return render_template('feed.html', message='feed', posts=posts)

user_info_data = []

@app.route('/info', methods=['GET', 'POST'])
def user_info():
    global user_info_data
    if request.method == 'POST':

        # cursor = db.cursor()
        user_info_data = Users.query.filter_by(name=request.form['Username']).all()

        # Unsafe sqlite3 usage
        # stmt = "SELECT name, bio FROM Users WHERE name = '%s' " % request.form['Username']
        # result = cursor.execute(stmt) 

        # Safe sqlite3 usage
        # stmt = "SELECT name, bio FROM Users WHERE name = ?"
        # result = cursor.execute(stmt, (request.form['Username'],))

        # data = []
        # for item in result:
        #     data.append(item)

        # user_info_data = data

        # print(stmt)
        
        print(request.form['Username'])

        return redirect(request.path)
    else:
        return render_template('user_info.html', title='User Info', user_info=user_info_data)
    