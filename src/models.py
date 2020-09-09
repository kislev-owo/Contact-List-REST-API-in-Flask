from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return 'Contact %r>' % self.full_name
    
    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone
        }

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    contact_id = db.Column(db.Integer, ForeignKey('contact.id'))
    group_id = db.Column(db.Integer, ForeignKey('group.id'))

    def __repr__(self):
        return 'Subscription %r>' % self.Subscription
    
    def serialize(self):
        return {
            "id": self.id,
            "contact_id": self.contact_id,
            "group_id": self.group_id
        }


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return 'Group %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
"""
