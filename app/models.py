from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    bio = db.Column(db.String(256), index=True)

class Quest(db.Model):
    id = db.Column(db.integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, index=True, nullable=False)
    image = db.Column(db.LargeBinary)
    createdby = db.relationship("Users", backref="user")

    #user_id = db.Column(db.integer, db.ForeignKey("user.id"))

