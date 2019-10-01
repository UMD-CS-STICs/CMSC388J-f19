from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.forms import *

@app.route('/', methods=['GET', 'POST'])
def index():
    form = WelcomeForm()
    if request.method == 'POST':
        if form.validate():
            session['name'] = form.name.data
            session['location'] = form.location.data
            session['age'] = form.age.data
            session.modified = True
        else:
            print('validation failed')
        
        return redirect(request.path)

    message = None
    if 'name' in session:
        message = 'Welcome %s of %s' % (session['name'], session['location'])
    
    return render_template('index.html', title='Front page', message=message, form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')