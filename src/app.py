from flask import Flask, jsonify, render_template, request, url_for, redirect, send_file, session
from models import User
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from  werkzeug.security import generate_password_hash
import json

from __init__ import app

from config import get_db, get_navbar_lang, database_hook, image_saver, login_required, logged_in

from views.home import home
app.register_blueprint(home, url_prefix="")

from views.authentication import authentication
app.register_blueprint(authentication, url_prefix="")

from views.chat import chat
app.register_blueprint(chat, url_prefix="")

# profile route
@app.route('/friend')
def profileFriend():
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
    return render_template("friend.html", postList = posts, lang=lang, language=lan, config=config)

@app.route('/user')
def profile():
    return redirect("/user/chachy.drs@mail.com")

# profile route
@app.route('/user/<email>')
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

# config route
@app.route('/config')
@login_required
def config_page():
        # read GET variable
    user = json.load( open("data/dummy/user.json") )
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/config.json") )
    else:
        lang = json.load( open("static/config/en/config.json") )
    get_navbar_lang(lang)
    return render_template("config.html",lang=lang, user=user)

# updates route
@app.route('/notifications')
@login_required
def notifications():
    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/notification.json") )
    else:
        lang = json.load( open("static/config/en/notification.json") )
    get_navbar_lang(lang)
    return render_template("notifications.html",lang=lang)

# search all users route
@app.route('/search')
@login_required
def search_users():
    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/search.json") )
    else:
        lang = json.load( open("static/config/en/search.json") )
    get_navbar_lang(lang)
    return render_template("search.html",lang=lang)

# demo for fetching mongoDB data
@app.route('/img/<filename>')
def fetch_users_image(filename):
    if( filename.split(".")[-1] == "png" ):
        mimetype="image/png"
    else:
        mimetype="image/jpeg"
        
    return send_file( image_saver.get_last_version(filename), mimetype=mimetype )

# demo for fetching mongoDB data
@app.route('/listUsers2')
def fetch_users2():
    
    global database_hook
    if type(database_hook)!=MongoClient:
        database_hook = get_db("users_db")
   
    _users = database_hook["usuarios"].find()
    users = [ {"clave": user["clave"], "email": user["email"], "perfil": user["perfil"] } for user in _users]
    return jsonify( users )
    # return jsonify(json.load( open("./ati_2022_1/datos/index.json") ))

# file not found
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>custom 404 error page</h1>", 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
    return "<h1>custom 500 error page</h1>", 500

if __name__=='__main__':
    
    app.config['SECRET_KEY'] = '123'
    app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O/<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

    try:
        database_hook.validate_collection("usuarios")
    except:
        # load initial users profile json location and img
        initial_users = json.load( open("./ati_2022_1/datos/index.json") )
        for user in initial_users:
            try:
                # open profile json
                perfil = json.load( open("./ati_2022_1/"+str(user["ci"])+"/perfil.json") )
                # open image
                with open( "./ati_2022_1/"+user["imagen"] , 'rb') as f:
                    contents = f.read()
                # image filename construction
                img_name = perfil["email"].lower()+ "." + user["imagen"].split(".")[-1]
                # save image in mongodb
                image_saver.put(contents, filename=img_name )
                # save user info in mongodb
                database_hook["usuarios"].insert_one( {
                    "email": perfil["email"].lower(),
                    "clave": generate_password_hash( user["ci"] ),
                    "conectado": False,
                    "solicitudes": [],
                    "notificaciones": [],
                    "configuración": {
                        "privacidad": "publico",
                        "colorPerfil": "#ffffff",
                        "colorMuro": "#ffffff",
                        "idioma": "es",
                        "notificacionesCorreo": 0
                    },
                    "perfil": {
                        "img_url": "/img/" + img_name,
                        "ci": str(user["ci"]),
                        "nombre": perfil["nombre"],
                        "descripcion": perfil["descripcion"],
                        "color": perfil["color"],
                        "libro": perfil["libro"],
                        "musica": perfil["musica"],
                        "video_juego": perfil["video_juego"],
                        "lenguajes": perfil["lenguajes"],
                        "genero": perfil["genero"],
                        "fecha_nacimiento": perfil["fecha_nacimiento"]
                    },
                    "chats": [],
                    "publicaciones": []
                } )
            except:
                pass

    app.run(host="0.0.0.0", port=5000, debug=True)