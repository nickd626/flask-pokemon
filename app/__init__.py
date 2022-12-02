from flask import Flask, render_template
import requests
from app.auth.auth_templates.forms import PokemonForm
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

# def pokemonStats(pk):
#     pkURL = f'https://pokeapi.co/api/v2/pokemon/{pk}'
#     pokemon = requests.get(pkURL)
#     pokemonName = pokemon.json()['forms'][0]['name']
#     pokemonAbility = pokemon.json()['abilities'][1]['ability']['name']
#     pokemonBaseExperience = pokemon.json()['base_experience']
#     pokemonSpriteDefault = pokemon.json()['sprites']['front_default']
#     pokemonSpriteShiny = pokemon.json()['sprites']['front_shiny']
#     pokemonAttack = pokemon.json()['stats'][1]['base_stat']
#     pokemonHP = pokemon.json()['stats'][0]['base_stat']
#     pokemonDefense = pokemon.json()['stats'][2]['base_stat']
#     print(f'Name: {pokemonName}\nAbility: {pokemonAbility}\nBase Experience: {pokemonBaseExperience}\nDefault sprite url: {pokemonSpriteDefault}\nShiny sprite url: {pokemonSpriteShiny}\nBase attack: {pokemonAttack}\nBase HP: {pokemonHP}\nBase Defense: {pokemonDefense}\n------------------------------')


@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/poke', methods = ['GET', 'POST'])
def poke():
    form = PokemonForm()
    return render_template('poke.html', form=form)

@app.route('/login', methods = ['GET'])
def login():
    return render_template('login.html')

@app.route('/signup', methods = ['GET'])
def signup():
    return render_template('signup.html')