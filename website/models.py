from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(400), nullable = False)
    creation_date = db.Column(db.DateTime(timezone = True), default = func.now())
    posts = db.relationship('Posts', backref='user')


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    creation_date = db.Column(db.DateTime(timezone = True), default = func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
