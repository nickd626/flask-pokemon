from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullible=False, unique=True)
    email = db.Column(db.String(250), nullible=False, unique=True)
    password = db.Column(db.String(250), nullible=False)
    pokemon = db.relationship()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullible=False)
    hp = db.Column(db.Integer, nullible=False)
    defense = db.Column(db.Integer, nullible=False)
    attack = db.Column(db.Integer, nullible=False)
    front_shiny = db.Column(db.String(250), nullible=False)
    ability = db.Column(db.String(50), nullible=False)