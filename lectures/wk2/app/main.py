from flask import Flask, render_template
app = Flask(__name__)

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


@app.route("/")
@app.route("/index", methods=['GET'])
def hello():
    return render_template('base.html', post='Hello')
    # return '<h2>Hello, world!</h2> <b>Welcome to the page!</b>'

@app.route("/about")
def about():
    return 'This is my first flask app!'

@app.route("/feed")
def feed():
    return render_template('feed.html', posts=posts)



# @app.route("/user/<username>")
# def show_profile(username):
#     return "This is %s's page" % username

# @app.route('/login', methods=['GET', 'POST', 'DELETE'])
# def login():
#     if request.method == 'POST':
#         process_login()
    
#     return "Log in page"


# if __name__ == '__main__':
#     app.run(debug=True)