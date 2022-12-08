from flask import Blueprint, render_template, request, flash
import requests
from app.auth.forms import PokemonForm, UserCreationForm, UserSignInForm
from app.models import Pokemon, Team, User, db
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/', methods = ['GET'])
def index():
    user = User.first_name
    return render_template('index.html', user=user)

@auth.route('/poke', methods = ['GET', 'POST'])
def poke():
    form = PokemonForm()
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokemonName.data.lower()
            pkURL = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
            pokemonRequest = requests.get(pkURL)
            pokemonName = pokemonRequest.json()['forms'][0]['name'].title()
            pokemonAbility = pokemonRequest.json()['abilities'][1]['ability']['name']
            pokemonSpriteShiny = pokemonRequest.json()['sprites']['front_shiny']
            pokemonAttack = pokemonRequest.json()['stats'][1]['base_stat']
            pokemonHP = pokemonRequest.json()['stats'][0]['base_stat']
            pokemonDefense = pokemonRequest.json()['stats'][2]['base_stat']
            
            if Pokemon.query.filter_by(name=pokemonName).all() == False:
                pk = Pokemon(pokemonName, pokemonHP, pokemonDefense, pokemonAttack, pokemonSpriteShiny, pokemonAbility)
                db.session.add(pk)
                db.session.commit()
            
            tpk = Pokemon.query.filter_by(name=pokemonName).first()
            team = Team(User.id, tpk.name, tpk.name, tpk.name, tpk.name, tpk.name)
            db.session.add(team)
            db.session.commit()
            return render_template('poke.html', form=form, pokemonName=pokemonName, pokemonAbility=pokemonAbility, pokemonAttack=pokemonAttack, pokemonSpriteShiny=pokemonSpriteShiny, pokemonHP=pokemonHP, pokemonDefense=pokemonDefense)
    return render_template('poke.html', form=form)

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserCreationForm()
    if request.method == 'POST':
        if form.validate():
            print('Testing')
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(first_name, last_name, username, email, password)
            db.session.add(user)
            db.session.commit()
    return render_template('signup.html', form=form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserSignInForm()
    print('Doing something')
    username = form.username.data
    password = form.password.data

    user = User.query.filter_by(username=username).first()
    if user:
        print('user recognized')
        if password == user.password:
            print('Logged in successfully')
            login_user(user)
        else:
            print('Invalid Password')
    else:
        print('User does not exist')
    return render_template('login.html', form=form)