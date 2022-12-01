from flask import request, render_template, Blueprint, session, redirect
from config import get_navbar_lang, login_required, database_hook
import json
from models.Post import Post
from models.Form import PostForm

home = Blueprint("home", __name__, static_folder="static", template_folder="templates")

# home route
@home.route('/', methods=['GET', 'POST'])
@login_required     # a session must be initialized to access this route
def index():

    form = PostForm(request.form)
    if form.validate_on_submit():
        
        post_id = database_hook["posts"].count_documents({})
        
        post = Post( form.content.data , session['user']["email"] )
        form.content.data = ""
        
        database_hook["posts"].insert_one({
            "id": 0 if not post_id else post_id ,
            "emailUsuario": post.author,
            "privacidad": "privado" if post.privacy else "publico",
            "timestamp": post.timestamp,
            "contenido": {
                "texto": post.content,
                "multimedia": ""
            },
            "comentarios": []
        })
        return redirect("/")

    _posts = database_hook["posts"].find().sort("id", -1)
    posts = []
    for p in _posts:
        _user = database_hook["usuarios"].find_one( {"email": p["emailUsuario"].lower() } )
        posts += [{
            "id": p["id"],
            "user_name": _user["perfil"]["nombre"] ,
            "post_time": p["timestamp"],
            "text": p["contenido"]["texto"],
            "profile_url": "/user/"+p["emailUsuario"],
            "profile_img_url": _user["perfil"]["img_url"] ,
            "comments": p["comentarios"]
        }]
    
    _users = database_hook["usuarios"].find()
    users = []
    for u in _users:
        if u["email"] != session["user"]["email"]:
            users += [{
                "nombre": u["perfil"]["nombre"],
                "img_url": u["perfil"]["img_url"],
                "conectado": u["conectado"],
                "email": u["email"]
            }]

    # posts = json.load( open("data/dummy/posts_home.json") ) #load posts to show in feed (currently dummy)

    # read GET variables
    lan = request.args.get("lang")
    
            # open config file according to the GET variable lang
    if lan == "es":
        lang = json.load( open("static/config/es/index.json") )
    else:   # default
        lang = json.load( open("static/config/en/index.json") )

    get_navbar_lang(lang)

    return render_template("index.html", postList = posts, lang=lang, language=lan, form = form, userList=users)

# updates route
@home.route('/notifications')
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
@home.route('/search/<name>')
@login_required
def search_users(name):
    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/search.json") )
    else:
        lang = json.load( open("static/config/en/search.json") )
    get_navbar_lang(lang)

    _users = database_hook["usuarios"].find()
    users = []
    for user in _users:
        if name.lower() in user["perfil"]["nombre"].lower():
            users += [ {"nombre": user["perfil"]["nombre"], "img_url": user["perfil"]["img_url"], "email": user["email"] } ]

    return render_template("search.html",lang=lang, userList = users)