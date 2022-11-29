from flask import Blueprint, request, render_template, redirect
from config import database_hook, get_navbar_lang
import json

users = Blueprint("users", __name__, static_folder="static", template_folder="templates")

@users.route('/')
def profile():
    return redirect("/user/chachy.drs@mail.com")

# demo for fetching mongoDB data
@users.route('/<email>')
def profileUser(email):
    # find user info mongodb
    user_info = database_hook["usuarios"].find_one( {"email": email} )["perfil"]
    posts = json.load( open("data/dummy/posts_friend.json") )
    # read GET variable
    lan = request.args.get("lang")
    if lan == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/index.json") )
        config = json.load(open("static/config/es/config.json"))
    else:
        lang = json.load( open("static/config/en/index.json") )
        config = json.load(open("static/config/en/config.json"))
    get_navbar_lang(lang)
    # return user_info
    return render_template("profile.html", postList = posts, lang=lang, language=lan, config=config, user_info=user_info)