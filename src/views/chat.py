from flask import request, render_template, Blueprint
from config import get_navbar_lang, login_required
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

    chats = json.load( open("data/dummy/chats.json") )
    get_navbar_lang(lang)
    return render_template("chat.html", chatList = chats, lang=lang)