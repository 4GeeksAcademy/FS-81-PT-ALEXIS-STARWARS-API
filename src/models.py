import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    city = db.Column(db.String(50))
    adress = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.email}'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    __tablename__="people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String, unique=True)
    description = db.Column(String(150))
    
    def __repr__(self):
        
        return f'<People {self.name}>'
    
    def serialize(self):
        return{
        "id": self.id,
        "name": self.name,
        "gender": self.gender,
        "description": self.description,
        }

class Planet(db.Model):
    __tablename__="planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    climate = db.Column(db.String(60))
    terrain = db.Column(db.String(60))
    

    def __repr__(self):
        return f'<Planet {self.name}>'
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
        }
       

class Favorite(db.Model):
    __tablename__="favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id=db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    people=db.relationship('People', backref='favorites')
    planet_id=db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    planet=db.relationship('Planet', backref='favorites')

    def __repr__(self):
        return f'<Favorite User:{self.user_id} People:{self.people_id} Planet:{self.planet_id}'
    
    def serialize(self):
        return{
            "id":self.id,
            "user_id":self.user_id,
            "people_id":self.people_id,
            "planet_id":self.planet_id,
        }

