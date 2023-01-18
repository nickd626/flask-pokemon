from . import models
from flask import Flask, render_template, request
from flask_migrate import Migrate
from .models import db
from flask_login import LoginManager
import requests
from app.auth.forms import PokemonForm, UserCreationForm, UserSignInForm
from app.models import User
from config import Config
from flask_moment import Moment
from .auth.routes import auth

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(auth)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db.init_app(app)
migrate = Migrate(app, db)


moment = Moment(app)

pokemonName = ''
pokemonAbility = ''
pokemonAttack = ''
pokemonSpriteShiny = ''
pokemonHP = ''
pokemonDefense = ''
