from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
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
        self.password = generate_password_hash(password)


team_pokemon = db.Table('team_pokemon',
                        db.Column('team_id', db.Integer, db.ForeignKey(
                            'team.id'), primary_key=True),
                        db.Column('pokemon_id', db.Integer, db.ForeignKey(
                            'pokemon.id'), primary_key=True)
                        )


class Team(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pk1 = db.Column(db.String(15), db.ForeignKey('pokemon.name'))
    pk2 = db.Column(db.String(15), db.ForeignKey('pokemon.name'))
    pk3 = db.Column(db.String(15), db.ForeignKey('pokemon.name'))
    pk4 = db.Column(db.String(15), db.ForeignKey('pokemon.name'))
    pk5 = db.Column(db.String(15), db.ForeignKey('pokemon.name'))

    def __init__(self, userID, pk1, pk2, pk3, pk4, pk5):
        self.userID = userID
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
