from flask import Flask, jsonify, render_template, request, url_for, redirect, session
from models import User
import pymongo
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
import json

from forms import RegisterForm 


import os
import gridfs

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O/<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
oauth = OAuth(app)

# get the connection to mongoDB through a client (this should be a variable... i guess)
def get_db(db_name):
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                        authSource="admin")
    db = client[db_name]
    return db

database_hook = get_db("users_db")
image_saver = gridfs.GridFS( database_hook )

def get_navbar_lang(lang):
    if request.args.get("lang") == "es":
        lang["navbar"] = json.load( open("static/config/es/navbar.json") )
    else:
        lang["navbar"] = json.load( open("static/config/en/navbar.json") )

# home route
@app.route('/')
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

# login route
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        database_hook["usuarios"].delete_many({"email" : form.email.data})
        database_hook["usuarios"].insert_one( {
            "email": form.email.data,
            "clave": form.password.data,
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
                "nombre": form.name.data,
                "descripcion": form.biography.data,
                "color": form.color.data,
                "libro": form.book.data,
                "musica": form.music.data,
                "video_juego": form.videogames.data,
                "lenguajes": form.languages.data,
                "genero": "Otro",
                "fecha_nacimiento": form.birthday.data.strftime("%m/%d/%Y")
            },
            "chats": [],
            "publicaciones": []
        })
        return redirect(url_for('index'))

    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/sign_in.json") )
    else:
        lang = json.load( open("static/config/en/sign_in.json") )
    get_navbar_lang(lang)

    return render_template("sign_in.html", lang=lang, form=form)

# login route
@app.route('/login')
def login():
    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/login.json") )
    else:
        lang = json.load( open("static/config/en/login.json") )
    get_navbar_lang(lang)
    return render_template("login.html", lang=lang)

@app.route('/user-login/',methods=['POST'])
def user_login():
    
    return User().login(database_hook)

    



# profile route
@app.route('/user')
def profile():
    posts = json.load( open("data/dummy/posts.json") )
    user = json.load( open("data/dummy/user.json") )
    # read GET variable
    lan = request.args.get("lang")
    if lan == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/index.json") )
        config = json.load((open("static/config/es/config.json")))
    else:
        lang = json.load( open("static/config/en/index.json") )
        config = json.load((open("static/config/en/config.json")))
    get_navbar_lang(lang)
    return render_template("profile.html", postList = posts, lang=lang, language=lan,config=config,user=user)


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

# chat route
@app.route('/chat')
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
@app.route('/listUsers')
def fetch_users():
    # db=""
    try:
        global database_hook
        # datos = json.load( open("./ati_2022_1/datos/index.json") )
        # database_hook["usuarios"].insert_many( datos )
        if type(database_hook)!=MongoClient:
            database_hook = get_db("users_db")
        # db = get_db("users_db")
        _users = database_hook["usuarios"].find()
        users = [{user} for user in _users]
        return jsonify(json.load( open("./ati_2022_1/datos/index.json") ))
    except:
        return jsonify({"error": "did not finish try statement"})
    #     print("error fetching users")

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
    oauth.register(
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
    return oauth.facebook.authorize_redirect(redirect_uri)



@app.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get('https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()   
    username = profile["name"]
    findMongoDB = database_hook.usuarios.find_one({"email": profile["email"]})
    
    #database_hook.usuarios.find_one_and_delete({"email": profile["email"]})
    #return redirect(url_for('index', key = "Nuevo perfil creado"))
    
    if findMongoDB:
        return redirect(url_for('index', key = findMongoDB["perfil"]["nombre"]))
    else:      
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
        return redirect(url_for('index', key = findMongoDB["perfil"]["nombre"]))

# file not found
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>custom 404 error page</h1>", 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
    return "<h1>custom 500 error page</h1>", 500

if __name__=='__main__':
    try:
        database_hook.validate_collection("usuarios")
    except:
        initial_users = json.load( open("./ati_2022_1/datos/index.json") )
        for user in initial_users:
            try:
                perfil = json.load( open("./ati_2022_1/"+str(user["ci"])+"/perfil.json") )
                with open( "./ati_2022_1/"+str(user["ci"])+"/"+str(user["ci"])+".jpg" , 'rb') as f:
                    contents = f.read()
                image_saver.put(contents, filename=str(user["ci"])+".jpg" )
                database_hook["usuarios"].insert_one( {
                    "email": perfil["email"].lower(),
                    "clave": user["ci"],
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
                        "ci": user["ci"],
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
    # global database_hook
    # if type(database_hook)!=MongoClient:
    #     database_hook = get_db("users_db")


    # database.usuarios.insert_many( datos )