from flask_app import db
from datetime import datetime

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return 'User: %s' % self.name

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    writer_email = db.Column(db.Integer, db.ForeignKey('user.email'), nullable=False)

    def __repr__(self):
        return 'Comment id: %s by User with email: %s' % (self.id, self.writer_email)