from flask import Flask
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = b'0)\x08\xe3\xc9\xc8\x83\xb8\xf1\xda\xdb\xd7\xb3\x0eT\x17'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

talisman = Talisman(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

from flask_app import models

db.create_all()

# from flask_app import routes

from flask_app.main.routes import main
from flask_app.users.routes import users

app.register_blueprint(main)
app.register_blueprint(users, url_prefix='/users')

