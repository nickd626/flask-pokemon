from flask import Flask, render_template, request
from flask_migrate import Migrate
from .models import db
import requests
from app.auth.forms import PokemonForm, UserCreationForm, UserSignInForm
from app.models import User
from config import Config
from flask_moment import Moment
from .auth.routes import auth

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(auth)

db.init_app(app)
migrate = Migrate(app, db)

from . import models

moment = Moment(app)

@app.route('/', methods = ['GET'])
def index():
    user = User.first_name
    return render_template('index.html', user=user)

pokemonName = ''
pokemonAbility = ''
pokemonAttack = ''
pokemonSpriteShiny = ''
pokemonHP = ''
pokemonDefense = ''

@app.route('/poke', methods = ['GET', 'POST'])
def poke():
    form = PokemonForm()
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokemonName.data.lower()
            pkURL = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
            pokemonRequest = requests.get(pkURL)
            pokemonName = pokemonRequest.json()['forms'][0]['name']
            pokemonAbility = pokemonRequest.json()['abilities'][1]['ability']['name']
            pokemonSpriteShiny = pokemonRequest.json()['sprites']['front_shiny']
            pokemonAttack = pokemonRequest.json()['stats'][1]['base_stat']
            pokemonHP = pokemonRequest.json()['stats'][0]['base_stat']
            pokemonDefense = pokemonRequest.json()['stats'][2]['base_stat']
            return render_template('poke.html', form=form, pokemonName=pokemonName, pokemonAbility=pokemonAbility, pokemonAttack=pokemonAttack, pokemonSpriteShiny=pokemonSpriteShiny, pokemonHP=pokemonHP, pokemonDefense=pokemonDefense)
    return render_template('poke.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserSignInForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.userPassword.data

            user = User.query.filter_by(username=username).first()
            if user:
                db_password = User.query.filter_by(password=password).first()
                if password == db_password:
                    print('logged in')
                else:
                    print('Invalid password')
            else:
                print('user does not exist')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

