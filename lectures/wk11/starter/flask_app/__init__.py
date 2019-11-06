from flask import Flask
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

csp = {
    'default-src': [
        '\'self\'',
        'https://code.jquery.com/',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/',
        'https://stackpath.bootstrapcdn.com/bootstrap/'
    ]
}

talisman = Talisman(content_security_policy=csp)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b'0)\x08\xe3\xc9\xc8\x83\xb8\xf1\xda\xdb\xd7\xb3\x0eT\x17'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    talisman.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flask_app.main.routes import main
    from flask_app.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app

