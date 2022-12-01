from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, DateField, SubmitField)
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, Length, EqualTo, DataRequired
from datetime import date

class RegisterForm(FlaskForm):
    profile_image = FileField(u'Image File')
    email = StringField(validators=[InputRequired(message="Introduzca un correo")])
    password = StringField(validators=[InputRequired(), EqualTo('confirm'), Length(min=7)])
    confirm = StringField()
    name = StringField(validators=[InputRequired()])
    biography = TextAreaField()
    birthday = DateField(default=date.today(), format='%Y-%m-%d')
    languages = StringField()
    videogames = StringField()
    music = StringField()
    book = StringField()
    color = StringField()
    submit = SubmitField()


class PostForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")