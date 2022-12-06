from flask import Flask, render_template, request
from flask_migrate import Migrate
from .models import db
import requests
from app.auth.auth_templates.forms import PokemonForm, UserCreationForm, UserSignInForm
from app.models import User
from config import Config
from flask_moment import Moment

app = Flask(__name__)

app.config.from_object(Config)

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
            email = form.userEmail.data
            password = form.userPassword.data

            user = User.query.filter_by(email=email).first()
            if user:
                db_password = User.query.filter_by(password=password).first()
                if password == db_password:
                    print('logged in')
                else:
                    print('Invalid password')
            else:
                print('user does not exist')
            return render_template('login.html', form=form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserCreationForm()
    if request.method == 'POST':
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(first_name, last_name, username, email, password)
            db.session.add(user)
            db.session.commit()
    return render_template('signup.html', form=form)