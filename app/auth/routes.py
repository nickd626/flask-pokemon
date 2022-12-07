from flask import Blueprint, render_template, request
import requests
from app.auth.forms import PokemonForm, UserCreationForm, UserSignInForm
from app.models import User, db

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/poke')
def poke():
    form = PokemonForm()
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
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.userPassword.data

            user = User.query.filter_by(username=username).first()
            print(user)
    return render_template('login.html', form=form)