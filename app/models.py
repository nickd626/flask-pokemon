from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    team = db.relationship('Team', backref='Captain', lazy=True)

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teamName = db.Column(db.String(25), nullable=False)
    pk1 = db.Column(db.String(15), db.ForeignKey('pokemon.name'), nullable=False)
    pk2 = db.Column(db.String(15), db.ForeignKey('pokemon.name'), nullable=False)
    pk3 = db.Column(db.String(15), db.ForeignKey('pokemon.name'), nullable=False)
    pk4 = db.Column(db.String(15), db.ForeignKey('pokemon.name'), nullable=False)
    pk5 = db.Column(db.String(15), db.ForeignKey('pokemon.name'), nullable=False)

    def __init__(self, teamName, pk1, pk2, pk3, pk4, pk5):
        self.teamName = teamName
        self.pk1 = pk1
        self.pk2 = pk2
        self.pk3 = pk3
        self.pk4 = pk4
        self.pk5 = pk5

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    hp = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    front_shiny = db.Column(db.String(250), nullable=False)
    ability = db.Column(db.String(50), nullable=False)

    def __init__(self, name, hp, defense, attack, front_shiny, ability):
        self.name = name
        self.hp = hp
        self.defense = defense
        self.attack = attack
        self.front_shiny = front_shiny
        self.ability = ability