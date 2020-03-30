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
        return '<Client \"{}\">'.format(self.name)

class Analyst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    text = db.Column(db.String(1000))
    img = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Analyst \"{}\">'.format(self.name)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(32), unique=True)
    title = db.Column(db.String(32))
    text = db.Column(db.String(10000))
    img = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Page \"{}\">'.format(self.title)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def get_all_items():
    items = Client.query.all() + Analyst.query.all() + Page.query.all()
    for item in items:
        setattr(item, 'class_name', item.__class__.__name__)
    return items

def get_item(id, class_name):
    items = [item for item in get_all_items() if item.id == id and item.__class__.__name__ == class_name]
    if len(items) != 1:
        print('found wrong number of items with id {} and class {}: {}'.format(id, class_name, items))
        return -1
    return items[0]
