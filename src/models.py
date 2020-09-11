from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    subscriptions = db.relationship("Subscription", backref="contact")    

    def __init__(self, full_name, email, address, phone):
        self.full_name = full_name
        self.email = email
        self.address = address
        self.phone = phone     

    @classmethod
    def new(cls, full_name, email, address, phone):
        """
            normalizacion de nombre email, etc...
            crea un objeto de la clase contact con
            esa normalizacion y devuelve la instancia creada.
        """
        new_contact = cls(
            full_name,
            email,
            address,
            phone
        )
        return new_contact 

    def update(self, diccionario):
        """Actualizacion de contacto"""
        if "email" in diccionario:
            self.email = diccionario["email"]
        if "full_name" in diccionario:
            self.full_name = diccionario["full_name"]
        if "address" in diccionario:
            self.address = diccionario["address"]
        if "phone" in diccionario:
            self.phone = diccionario["phone"]
        return True  

    def __repr__(self):
        return '<Contact %r>' % self.full_name
    
    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "groups": [subscription.group_id for subscription in self.subscriptions]
        }       

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    contact_id = db.Column(db.Integer, ForeignKey('contact.id'))
    group_id = db.Column(db.Integer, ForeignKey('group.id'))


    def __init__(self, contact_id,  group_id):
        """creates an instance of this class"""
        self.contact_id = contact_id
        self.group_id = group_id
        
    def __repr__(self):
        return '<Subscription %r>' % self.group_id        
    
    def serialize(self):
        return {
            "id": self.id,
            "contact_id": self.contact_id,
            "group_id": self.group_id
        }


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    subscriptions = db.relationship("Subscription", backref="group")    

    def __init__(self, name):
        self.name = name   

    @classmethod
    def addn(cls, name):
        """ Normalizacion de los grupos """
        add = cls(
            name.lower().capitalize())
        return add

    def update(self, diccionario):
        """Actualizacion de contacto"""
        if "name" in diccionario:
            self.name = diccionario["name"]
        return True 

    def __repr__(self):
        return '<Group %r>' % self.name             

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
