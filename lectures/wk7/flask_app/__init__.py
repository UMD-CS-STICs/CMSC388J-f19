from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xa4\x0c\x9c3B\xa8a\xc4\x19<z\x00\xc2\xc9\xcd\x14'

from flask_app import routes