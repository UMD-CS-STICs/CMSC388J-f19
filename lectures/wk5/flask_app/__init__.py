from flask import Flask, session
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = b'z\x8b\x7fs\xb2\xfa\xeb\x1a\xe6\xa8\xcd\x81\xf2Qq\xdb'

csrf = CSRFProtect(app)

from flask_app import routes