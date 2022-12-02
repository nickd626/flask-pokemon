from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullible=False)
    last_name = db.Column(db.String(25), nulliblE=False)
    username = db.Column(db.String(50), nullible=False, unique=True)
    email = db.Column(db.String(250), nullible=False, unique=True)
    password = db.Column(db.String(250), nullible=False)
    pokemon = db.relationship()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullible=False)
    hp = db.Column(db.Integer, nullible=False)
    defense = db.Column(db.Integer, nullible=False)
    attack = db.Column(db.Integer, nullible=False)
    front_shiny = db.Column(db.String(250), nullible=False)
    ability = db.Column(db.String(50), nullible=False)

    def __init__(self, name, hp, defense, attack, front_shiny, ability):
        self.name = name
        self.hp = hp
        self.defense = defense
        self.attack = attack
        self.front_shiny = front_shiny
        self.ability = ability