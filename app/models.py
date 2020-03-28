from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    clients = db.relationship('Client', backref='author', lazy='dynamic')
    analysts = db.relationship('Analyst', backref='author', lazy='dynamic')
    pages = db.relationship('Page', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    text = db.Column(db.String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.text[:10])

class Analyst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    text = db.Column(db.String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.text[:10])

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    html = db.Column(db.String(16), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Page {}>'.format(self.html)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
