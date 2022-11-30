from flask import jsonify, render_template, request
from pymongo import MongoClient
from  werkzeug.security import generate_password_hash
import json

# the app Flask object will be initialized in __init__.py
from __init__ import app

# import resources (not really configuration tho)
from config import get_db, get_navbar_lang, database_hook, image_saver

# import views
from views.home import home
from views.authentication import authentication
from views.chat import chat
from views.images import image_collection
from views.user import users
from views.profile_configuration import profile_configuration

# register routes blueprint in Flask main app
app.register_blueprint(home,                    url_prefix="")
app.register_blueprint(authentication,          url_prefix="")
app.register_blueprint(chat,                    url_prefix="")
app.register_blueprint(image_collection,        url_prefix="/img")
app.register_blueprint(users,                   url_prefix="/user")
app.register_blueprint(profile_configuration,   url_prefix="" )

# dummy profile route
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

# demo for fetching mongoDB users data
@app.route('/listUsers2')
def fetch_users2():
    
    global database_hook
    if type(database_hook)!=MongoClient:
        database_hook = get_db("users_db")
   
    _users = database_hook["usuarios"].find()
    users = [ {"clave": user["clave"], "email": user["email"], "perfil": user["perfil"] } for user in _users]
    # return jsonify(json.load( open("./ati_2022_1/datos/index.json") ))
    return jsonify( users )

# demo for fetching mongoDB users data
@app.route('/listPosts')
def fetch_posts():
    
    global database_hook
    if type(database_hook)!=MongoClient:
        database_hook = get_db("users_db")
   
    _posts = database_hook["posts"].find()
    posts = []
    for p in _posts:
        _user = database_hook["usuarios"].find_one( {"email": p["emailUsuario"] } )
        posts += [{
            "id": p["id"],
            "user_name": _user["perfil"]["nombre"] ,
            "post_time": p["timestamp"],
            "text": p["contenido"]["texto"],
            "profile_url": "/user/"+p["emailUsuario"],
            "profile_img_url": _user["perfil"]["img_url"] ,
            "comments": p["comentarios"]
        }]
    # return jsonify(json.load( open("./ati_2022_1/datos/index.json") ))
    return jsonify( posts )

# file not found
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>custom 404 error page</h1>", 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
    return "<h1>custom 500 error page</h1>", 500

if __name__=='__main__':

    try:    #   Try to validate the "usuarios" collection
        database_hook.validate_collection("usuarios")
    
    except: #   If this collections does not exist, the initial users will be loaded 
        
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
            except: #   If there's an error while loading an user, that user will not be inserted
                pass

    app.run(host="0.0.0.0", port=5000, debug=True)