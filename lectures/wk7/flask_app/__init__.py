from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
# app.config['SECRET_KEY'] = b'\xa4\x0c\x9c3B\xa8a\xc4\x19<z\x00\xc2\xc9\xcd\x14'

# Accept all content coming from this same domain
csp = {
    'default-src': '\'self\''
}

# Accept all content coming from this same domain + another trusted domain
csp = {
    'default-src': [
        '\'self\'',
        'mywebsite.com'
    ]
}

# Accept all content from this domain, accept all images from the web,
# but only accept video and audio content from the domains
# listed in 'media-src'.
# Only accept scripts from script-src
csp = {
    'default-src': '\'self\'',
    'img-src': '*',
    'media-src': [
        'audiowebsite.com',
        'videowebsite.com',
    ],
    'script-src': 'trusted-scripts.com'
}

talisman = Talisman(app, content_security_policy=csp)

from flask_app import routes