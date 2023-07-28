from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app = app


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), nullable=False,
                         primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    feedback = db.relationship("Feedback", backref='user')

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')
        user = cls(username=username, password=hashed_utf8,
                   first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password){
            return user
        }
        else {
            return False
        }


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, db.ForeignKey(
        'users.username'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
