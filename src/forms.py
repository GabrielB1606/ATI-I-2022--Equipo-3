from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, DateField, SubmitField)
from wtforms.validators import InputRequired, Length
from datetime import date

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(message="Introduzca un correo")])
    password = StringField(validators=[InputRequired(), Length(min=7)])
    name = StringField(validators=[InputRequired()])
    biography = TextAreaField()
    birthday = DateField(default=date.today(), format='%Y-%m-%d')
    languages = StringField()
    videogames = StringField()
    music = StringField()
    book = StringField()
    color = StringField()
    submit = SubmitField()