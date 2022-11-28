from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, DateField, RadioField, SubmitField)

from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired()])
    password = StringField(validators=[InputRequired(), Length(min=7)])
    name = StringField(validators=[InputRequired()])
    biography = TextAreaField()
    birthday = DateField(format='%d/%m/%y')
    languages = StringField()
    videoGames = StringField()
    music = StringField()
    book = StringField()
    color = StringField()
    gender = RadioField(choices=['Male', 'Female', 'Other'])
    submit = SubmitField()