from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class PokemonForm(FlaskForm):
    pokemonName = StringField('PokemonName')
    submit = SubmitField()

class UserCreationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class UserSignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    userPassword = StringField('Password', validators=[DataRequired()])
    submit = SubmitField()