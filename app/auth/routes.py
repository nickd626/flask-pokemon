from sqlalchemy import func
from flask import Blueprint, render_template, request, flash
import requests
import random
from app.auth.forms import PokemonForm, CatchPokemonForm, UserCreationForm, UserSignInForm
from app.models import Pokemon, Team, User, db
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/', methods=['GET'])
def index():
    user = User.first_name
    return render_template('index.html', user=user)


@auth.route('/poke', methods=['GET', 'POST'])
def poke():
    form = PokemonForm()
    catch = CatchPokemonForm()
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokemonName.data.lower()
            pkURL = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
            pokemonRequest = requests.get(pkURL)
            pokemonName = pokemonRequest.json()['forms'][0]['name'].title()
            pokemonAbility = pokemonRequest.json(
            )['abilities'][1]['ability']['name']
            pokemonSpriteShiny = pokemonRequest.json()[
                'sprites']['front_shiny']
            pokemonAttack = pokemonRequest.json()['stats'][1]['base_stat']
            pokemonHP = pokemonRequest.json()['stats'][0]['base_stat']
            pokemonDefense = pokemonRequest.json()['stats'][2]['base_stat']

            pk = Pokemon.query.filter_by(name=pokemonName).first()
            if not pk:
                pk = Pokemon(pokemonName, pokemonHP, pokemonDefense,
                             pokemonAttack, pokemonSpriteShiny, pokemonAbility)
                db.session.add(pokemon)
                db.session.commit()

        if catch.validate():
            user = User.query.filter_by(id=current_user.id).first()
            pokemon = Pokemon.query.filter_by(name=pokemonName).first()

            user.teams[0].pokemon.append(pokemon)
            db.session.commit()
            return render_template('poke.html', form=form, catch=catch, pokemonName=pokemonName, pokemonAbility=pokemonAbility, pokemonAttack=pokemonAttack, pokemonSpriteShiny=pokemonSpriteShiny, pokemonHP=pokemonHP, pokemonDefense=pokemonDefense)
    return render_template('poke.html', form=form)


@auth.route('/team', methods=['GET', 'POST'])
def team():
    user = current_user
    team = Team.query.filter_by(userID=user.id).first()
    pokemon_list = [team.pk1, team.pk2, team.pk3, team.pk4, team.pk5]
    return render_template('team.html', user=user, team=team, pokemon_list=pokemon_list, Pokemon=Pokemon)


@auth.route('/battle', methods=['GET', 'POST'])
def battle():
    user = current_user
    user_team = Team.query.filter_by(userID=user.id).first()
    opponent_id = User.query.order_by(func.random()).limit(1).first().id
    print(opponent_id)
    opponent_team = Team.query.filter_by(userID=opponent_id).first()
    user_pokemon_list = [Pokemon.query.filter_by(name=user_team.pk1).first(), Pokemon.query.filter_by(name=user_team.pk2).first(),
                         Pokemon.query.filter_by(name=user_team.pk3).first(), Pokemon.query.filter_by(name=user_team.pk4).first(), Pokemon.query.filter_by(name=user_team.pk5).first()]
    opponent_pokemon_list = [Pokemon.query.filter_by(name=opponent_team.pk1).first(), Pokemon.query.filter_by(name=opponent_team.pk2).first(),
                             Pokemon.query.filter_by(name=opponent_team.pk3).first(), Pokemon.query.filter_by(name=opponent_team.pk4).first(), Pokemon.query.filter_by(name=opponent_team.pk5).first()]
    winner = 'tie'

    for user_pokemon in user_pokemon_list:
        for opponent_pokemon in opponent_pokemon_list:
            user_hp = user_pokemon.hp
            user_attack = user_pokemon.attack
            user_defense = user_pokemon.defense

            opponent_hp = opponent_pokemon.hp
            opponent_attack = opponent_pokemon.attack
            opponent_defense = opponent_pokemon.defense

            user_hp = user_hp - (opponent_attack - user_defense)
            opponent_hp = opponent_hp - (user_attack - opponent_defense)

            if user_hp <= 0:
                user_pokemon_list.remove(user_pokemon)
                print(f'{user_pokemon.name} has fainted.')
            if opponent_hp <= 0:
                opponent_pokemon_list.remove(opponent_pokemon)
                print(f'{opponent_pokemon.name} has fainted.')

            if len(user_pokemon_list) == 0:
                winner = User.query.filter_by(
                    UserID=opponent_id).first().username
            if len(opponent_pokemon_list) == 0:
                winner = current_user.username

    return render_template('battle.html', user_team=user_pokemon_list, opponent_team=opponent_pokemon_list, winner=winner)


@auth.route('/signup', methods=['GET', 'POST'])
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


@auth.route('/login', methods=['GET', 'POST'])
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
