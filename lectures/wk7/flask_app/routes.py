from flask_app import app, talisman

from flask import render_template
from flask_talisman import ALLOW_FROM

# We don't want index to be embeddable
@app.route('/')
def index():
    return render_template('index.html')

# Any site can embed this page with an iframe
# @talisman(frame_options=ALLOW_FROM, frame_options_allow_from='*')

# Only allow trusteddomain.com to embed the about page in an iframe
@app.route('/about')
@talisman(frame_options=ALLOW_FROM, frame_options_allow_from='https://trusteddomain.com/')
def about():
    return render_template('about.html')
