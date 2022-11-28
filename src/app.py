from flask import Flask, jsonify, render_template, request, redirect, url_for
import pymongo
from pymongo import MongoClient
import json
from forms import RegisterForm 

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

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

def get_navbar_lang(lang):
    if request.args.get("lang") == "es":
        lang["navbar"] = json.load( open("static/config/es/navbar.json") )
    else:
        lang["navbar"] = json.load( open("static/config/en/navbar.json") )

# home route
@app.route('/')
def index():
    posts = json.load( open("data/dummy/posts_home.json") )
    # read GET variable
    lan = request.args.get("lang")
    if lan == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/index.json") )
    else:
        lang = json.load( open("static/config/en/index.json") )
    get_navbar_lang(lang)
    return render_template("index.html", postList = posts, lang=lang, language=lan)

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
            perfil = json.load( open("./ati_2022_1/"+str(user["ci"])+"/perfil.json") )
            database_hook["usuarios"].insert_one( {
                "email": perfil["email"],
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

    app.run(host="0.0.0.0", port=5000, debug=True)
    # global database_hook
    # if type(database_hook)!=MongoClient:
    #     database_hook = get_db("users_db")


    # database.usuarios.insert_many( datos )