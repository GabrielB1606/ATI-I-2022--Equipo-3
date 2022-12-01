from flask import Blueprint, request, render_template, redirect, jsonify, session
from config import database_hook, get_navbar_lang
import json

users = Blueprint("users", __name__, static_folder="static", template_folder="templates")

@users.route('/')
def profile():
    return redirect("/user/chachy.drs@mail.com")

@users.route('/search/<name>')
def searchUserJSON(name):
    _users = database_hook["usuarios"].find()
    users = []
    for user in _users:
        if user["email"] != session["user"]["email"] and name.lower() in user["perfil"]["nombre"].lower():
            users += [ {"nombre": user["perfil"]["nombre"], "img_url": user["perfil"]["img_url"], "email": user["email"] } ]
    
    return jsonify(users)

# demo for fetching mongoDB data
@users.route('/<email>')
def profileUser(email):
    # find user info mongodb
    user_info = database_hook["usuarios"].find_one( {"email": email} )["perfil"]

    _posts = database_hook["posts"].find({"emailUsuario": email.lower() }).sort("id", -1)
    posts = []
    for p in _posts:
        posts += [{
            "id": p["id"],
            "user_name": user_info["nombre"] ,
            "post_time": p["timestamp"],
            "text": p["contenido"]["texto"],
            "profile_url": "/user/"+p["emailUsuario"],
            "profile_img_url": user_info["img_url"] ,
            "comments": p["comentarios"]
        }]

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