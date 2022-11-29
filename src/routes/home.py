from flask import Flask, request, render_template, Blueprint
from config import get_db, get_navbar_lang, database_hook, image_saver, login_required
import json

home = Blueprint("home", __name__, static_folder="static", template_folder="templates")

# home route
@home.route('/')
@login_required
def index():
    posts = json.load( open("data/dummy/posts_home.json") )
    key = request.args.get("key")
    # read GET variable
    lan = request.args.get("lang")
    if lan == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/index.json") )
    else:
        lang = json.load( open("static/config/en/index.json") )
    get_navbar_lang(lang)
    return render_template("index.html", postList = posts, lang=lang, language=lan, key=key)