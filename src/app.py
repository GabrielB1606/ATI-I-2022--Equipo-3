from flask import Flask, jsonify, render_template, request, url_for, redirect, send_file, session
from models import User
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from  werkzeug.security import generate_password_hash
import json

from forms import RegisterForm 

from config import get_db, get_navbar_lang, database_hook, image_saver, login_required, logged_in
import config

import os
import gridfs

app = Flask(__name__)

from views.home import home
app.register_blueprint(home, url_prefix="")

from views.authentication import authentication
app.register_blueprint(authentication, url_prefix="")

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

# chat route
@app.route('/chat')
@login_required
def chat():
    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/chat.json") )
    else:
        lang = json.load( open("static/config/en/chat.json") )

    chats = json.load( open("data/dummy/chats.json") )
    get_navbar_lang(lang)
    return render_template("chat.html", chatList = chats, lang=lang)

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

@app.route('/facebook/')
def facebook():
    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = '690747602573297'
    FACEBOOK_CLIENT_SECRET = '8936f7e5d6fc5dda0056b58bcb85bc54'
    config.oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return config.oauth.facebook.authorize_redirect(redirect_uri)



@app.route('/facebook/auth/')
def facebook_auth():
    token = config.oauth.facebook.authorize_access_token()
    resp = config.oauth.facebook.get('https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()   
    username = profile["name"]
    findMongoDB = database_hook.usuarios.find_one({"email": profile["email"]})
    
    #database_hook.usuarios.find_one_and_delete({"email": profile["email"]})
    #return redirect(url_for('index', key = "Nuevo perfil creado"))
    
    if not findMongoDB:    
        database_hook["usuarios"].insert_one( {
            "email": profile["email"],
            "clave": "",
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
                "img_url": profile["picture"]["data"]["url"],
                "ci": "",
                "nombre": profile["name"],
                "descripcion": "",
                "color": "",
                "libro": "",
                "musica": "",
                "video_juego": "",
                "lenguajes": "",
                "genero": "",
                "fecha_nacimiento": ""
            },
            "chats": [],
            "publicaciones": []
        } )
        findMongoDB = database_hook.usuarios.find_one({"email": profile["email"]})
    
    User().start_session( {"email": findMongoDB["email"], "perfil": findMongoDB["perfil"]} )
    return redirect(url_for('home.index', key = profile["name"]))

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
    
    config.__dict__["oauth"] =OAuth(app)

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