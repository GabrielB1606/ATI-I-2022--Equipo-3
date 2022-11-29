from flask import request, render_template, Blueprint
from config import get_navbar_lang, login_required
import json

# from app import app

home = Blueprint("home", __name__, static_folder="static", template_folder="templates")

# home route
@home.route('/')
@login_required     # a session must be initialized to access this route
def index():

    posts = json.load( open("data/dummy/posts_home.json") ) #load posts to show in feed (currently dummy)
    
            # read GET variables
    key = request.args.get("key")
    lan = request.args.get("lang")
    
            # open config file according to the GET variable lang
    if lan == "es":
        lang = json.load( open("static/config/es/index.json") )
    else:   # default
        lang = json.load( open("static/config/en/index.json") )

    get_navbar_lang(lang)

    return render_template("index.html", postList = posts, lang=lang, language=lan, key=key)

# app.register_blueprint(home, url_prefix="")