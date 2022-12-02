from flask import Flask, render_template, request
from flask_migrate import Migrate
from .models import db
import requests
from app.auth.auth_templates.forms import PokemonForm, UserCreationForm, UserSignInForm
from app.models import User
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from . import routes
from . import models

def pokemonStats(pk):
    pkURL = f'https://pokeapi.co/api/v2/pokemon/{pk}'
    pokemon = requests.get(pkURL)
    pokemonName = pokemon.json()['forms'][0]['name']
    pokemonAbility = pokemon.json()['abilities'][1]['ability']['name']
    pokemonSpriteShiny = pokemon.json()['sprites']['front_shiny']
    pokemonAttack = pokemon.json()['stats'][1]['base_stat']
    pokemonHP = pokemon.json()['stats'][0]['base_stat']
    pokemonDefense = pokemon.json()['stats'][2]['base_stat']


@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/poke', methods = ['GET', 'POST'])
def poke():
    form = PokemonForm()
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokemonName.data.lower()
            pokemonStats(pokemon)
    return render_template('poke.html', form=form)

@app.route('/login', methods = ['GET'])
def login():
    form = UserSignInForm()
    return render_template('login.html', form=form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserCreationForm()
    if request.method == 'POST':
        if form.validate():
            name = form.name.data
            email = form.email.data
            password = form.password.data

            print(name, email, password)

            user = User(name, email, password)
    return render_template('signup.html', form=form)