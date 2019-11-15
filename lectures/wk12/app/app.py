from flask import Flask, render_template
from flask_mail import Mail, Message
app = Flask(__name__)

mail = Mail(app)

# app.config['MAIL_PASSWORD'] = 
# app.config['MAIL_SENDER'] = 
# app.config['MAIL_PORT'] = 

posts = [
    {
        'user': 'Elon Musk',
        'text': 'The sun is a theronuclear explosion fyi',
        'location': 'California',
        'likes': 3_000_000,
    },
    {
        'user': 'John Smith',
        'text': 'Excited for school!!!!',
        'location': 'College Park',
        'likes': 5
    }
]


@app.route('/')
@app.route('/index')
def index():
    msg = Message("Hello from my flask app",
                  recipients=["kenton@gmail.com"])
    
    mail.send(msg)

    return render_template('base.html', message='hello')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user/<username>')
def profile(username):
    return render_template('user.html', username=username)

@app.route('/feed')
def feed():
    return render_template('feed.html', message='feed', posts=posts)

# -- Not well supported -- #
# if __name__=='__main__':
#     app.run(debug=True)