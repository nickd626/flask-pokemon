from flask import Blueprint, render_template
from app.auth.auth_templates.forms import PokemonForm, UserCreationForm

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/poke')
def poke():
    form = PokemonForm()
    return render_template('poke.html', form=form)

@auth.route('/signup')
def signup():
    form = UserCreationForm()
    return render_template('signup.html', form=form)