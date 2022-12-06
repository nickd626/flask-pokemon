from flask import Blueprint, render_template, request
import requests
from app.auth.auth_templates.forms import PokemonForm, UserCreationForm, UserSignInForm
from app.models import User

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
            
            return render_template('signup.html', form=form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserSignInForm()
    if request.method == 'POST':
        if form.validate():
            email = form.userEmail.data
            password = form.userPassword.data

            user = User.query.filter_by(email=email).first()
            print(user)
    return render_template('login.html', form=form)