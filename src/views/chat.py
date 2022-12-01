from flask import request, render_template, Blueprint, session
from config import get_navbar_lang, login_required, database_hook
import json

# from app import app

chat = Blueprint("chat", __name__, static_folder="static", template_folder="templates")

# chat route
@chat.route('/chat')
@login_required
def chats():
    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/chat.json") )
    else:
        lang = json.load( open("static/config/en/chat.json") )

    _users = database_hook["usuarios"].find()
    chats = []
    for u in _users:
        if u["email"] != session["user"]["email"]:
            chats += [{
                "user_from": u["perfil"]["nombre"],
                "img_url": u["perfil"]["img_url"],
                "status": "Online" if u["conectado"] else "Offline",
                "email": u["email"],
                "new_messages": 0,
                "messages":[]
            }]

    # chats = json.load( open("data/dummy/chats.json") )
    get_navbar_lang(lang)
    return render_template("chat.html", chatList = chats, lang=lang)