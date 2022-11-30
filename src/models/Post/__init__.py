from uuid import uuid1
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (TextAreaField, SubmitField)
from wtforms.validators import DataRequired

class Post:
    id = uuid1().int
    content = ""
    author = ""
    timestamp = datetime.now()

class PostForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")