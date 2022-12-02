from flask import Blueprint, render_template, request
import requests
from app.auth.auth_templates.forms import PokemonForm, UserCreationForm, UserSignInForm

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/poke')
def poke():
    form = PokemonForm()
    return render_template('poke.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserCreationForm()
    if request.method == 'POST':
        if form.validate():
            pokemon = form.pokemonName.data.lower()
            pkURL = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
            pokemon = requests.get(pkURL)
            pokemonAbility = pokemon.json()['abilities'][1]['ability']['name']
            pokemonSpriteShiny = pokemon.json()['sprites']['front_shiny']
            pokemonAttack = pokemon.json()['stats'][1]['base_stat']
            pokemonHP = pokemon.json()['stats'][0]['base_stat']
            pokemonDefense = pokemon.json()['stats'][2]['base_stat']
    return render_template('signup.html', form=form)

@auth.route('/login')
def login():
    form = UserSignInForm()
    return render_template('login.html', form=form)