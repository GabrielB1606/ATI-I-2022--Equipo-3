from flask import request, render_template, Blueprint, redirect, url_for
from config import get_navbar_lang, logged_in, database_hook, oauth
from  werkzeug.security import generate_password_hash
import json
from models.Form import RegisterForm 
from models.User import User

authentication = Blueprint("authentication", __name__, static_folder="static", template_folder="templates")

# login route
@authentication.route('/sign_in', methods=['GET', 'POST'])
@logged_in
def sign_in():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        database_hook["usuarios"].delete_many({"email" : form.email.data})
        database_hook["usuarios"].insert_one( {
            "email": form.email.data,
            "clave": generate_password_hash(form.password.data),
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
        return redirect(url_for('home.index'))

    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/sign_in.json") )
    else:
        lang = json.load( open("static/config/en/sign_in.json") )
    get_navbar_lang(lang)

    return render_template("sign_in.html", lang=lang, form=form)

# login route
@authentication.route('/logout')
def logout():
    User().signout()
    return redirect('/login')

# login route
@authentication.route('/login')
@logged_in
def login():
    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/login.json") )
    else:
        lang = json.load( open("static/config/en/login.json") )
    get_navbar_lang(lang)
    return render_template("login.html", lang=lang)

@authentication.route('/user-login/',methods=['POST'])
def user_login():
    return User().login(database_hook)


    # facebook
@authentication.route('/facebook/')
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
    redirect_uri = url_for('authentication.facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@authentication.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get('https://graph.facebook.com/me?fields=id,name,email,picture{url}')
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