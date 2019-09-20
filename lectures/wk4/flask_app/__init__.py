from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sqlite3
db_path = 'users.db'
db = sqlite3.connect(db_path)

app = Flask(__name__)

# For absolute path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'

# Relative Path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# For an in-memory
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

from flask_app import routes
from flask_app.models import *

