from logging.config import dictConfig

from flask import Flask, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

csp = {
    "default-src": [
        "'self'",
    ]
}

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

talisman = Talisman()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"


def create_app():
    app = Flask(__name__)
    app.config[
        "SECRET_KEY"
    ] = b"0)\x08\xe3\xc9\xc8\x83\xb8\xf1\xda\xdb\xd7\xb3\x0eT\x17"
    # app.config['SERVER_NAME'] = '127.0.0.1:5000'

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    talisman.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flask_app.main.routes import main
    from flask_app.users.routes import users
    from flask_app.posts.routes import posts

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    with app.app_context():
        db.create_all()

    talisman.content_security_policy = csp
    talisman.content_security_policy_report_uri = "/csp_error_handling"

    return app
