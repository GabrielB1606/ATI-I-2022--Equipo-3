from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, DateField)

from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired(), Length(min=7)])
    name = StringField('Name', validators=[InputRequired()])
    biography = TextAreaField('Biography')
    birthday = DateField('Birthday', format='%d/%m/%y')
    videoGames = StringField('VideoGame')
    music = StringField('Music')
    book = StringField('Book')
    color = StringField('Color')