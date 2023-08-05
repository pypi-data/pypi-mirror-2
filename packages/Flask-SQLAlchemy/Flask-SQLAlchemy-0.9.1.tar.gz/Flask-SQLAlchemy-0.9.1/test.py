from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


user_read_items = db.Table('user_read_items', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('item_id', db.Integer, db.ForeignKey('items.item_id'))
)

user_unread_items = db.Table('user_unread_items', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('item_id', db.Integer, db.ForeignKey('items.item_id'))
)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column('item_id', db.Integer, primary_key=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(125))
    profile_url = db.Column(db.String)
    access_token = db.Column(db.String)


# mapping
User.read = db.relation(Item, secondary=user_read_items)
User.unread = db.relation(Item, secondary=user_unread_items)
