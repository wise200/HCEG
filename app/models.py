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
        return '<User \"{}\">'.format(self.username)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    text = db.Column(db.String(1000))
    img = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Client \"{}\">'.format(self.text[:15])

class Analyst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128), index=True, unique=True)
    text = db.Column(db.String(1000))
    img = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Analyst \"{}\">'.format(self.text[:15])

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    html = db.Column(db.String(32), unique=True)
    text = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Page \"{}\">'.format(self.html)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def get_all_items():
    return Client.query.all() + Analyst.query.all() + Page.query.all()

def get_item(id):
    items = [item for item in get_all_items() if item.id == id]
    if len(items) != 1:
        return -1
    return items[0]
