from uuid import uuid1
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (TextAreaField, SubmitField )
from wtforms.validators import DataRequired
from config import database_hook

last_post = 1

class Post:
    id = 0
    content = ""
    author = ""
    timestamp = datetime.now()
    privacy = False

    def __init__(self, content, author):
        self.content = content
        self.author = author
        
        global last_post
        self.id = last_post
        last_post+=1

    def save(self):
        if self.author != "" and self.content != "":
            database_hook["posts"].insert_one({
                "id": self.id,
                "emailUsuario": self.author,
                "privacidad": "privado" if self.privacy else "publico",
                "timestamp": self.timestamp,
                "contenido": {
                    "texto": self.content,
                    "multimedia": "blob"
                },
                "comentarios": []
            })
        pass

class PostForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")