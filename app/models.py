from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    bio = db.Column(db.String(256), index=True)
    password_hash = db.Column(db.String(128))
    image = db.Column(db.LargeBinary)
    admin = db.Column(db.Boolean, default=False)

    created_by = db.relationship("Quest", backref="user", lazy='dynamic')
    review = db.relationship('Review', backref='user', lazy='dynamic')
    in_progress = db.relationship('QuestsInProgress', backref='user', lazy='dynamic')


    #Implement something for badges?

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), index=True, nullable=False, unique=True)
    description = db.Column(db.Text, index=True, nullable=False)
    image = db.Column(db.LargeBinary)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    review = db.relationship('Review', backref='quest', lazy='dynamic')
    genre = db.relationship('QuestGenres', backref='quest', lazy='dynamic')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_text = db.Column(db.Text, index=True)
    image = db.Column(db.LargeBinary)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    quest_id = db.Column(db.Integer, db.ForeignKey("quest.id"))


class QuestsInProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    in_progress = db.relationship('Quest', backref='quest_in_progress')


class QuestsCompleted(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    completed = db.relationship('Quest', backref='quest_completed')


class QuestsCreatedBy(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('Quest', backref='quest_created')


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String(64), index=True, unique=True)
    associatedQuests = db.relationship('QuestGenres', backref='genre', lazy='dynamic')


class QuestGenres(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


