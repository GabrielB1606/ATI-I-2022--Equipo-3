from flask import Flask, jsonify, render_template, request, url_for, redirect
import pymongo
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
import json
import os

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O/<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
oauth = OAuth(app)

# get the connection to mongoDB through a client (this should be a variable... i guess)
def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                        authSource="admin")
    db = client["users_db"]
    return db

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
    db=""
    try:
        db = get_db()
        _users = db.users_tb.find()
        users = [{"name": user["name"], "password": user["password"]} for user in _users]
        return jsonify({"users": users})
    except:
        print("error fetching users")
    finally:
        if type(db)==MongoClient:
            db.close()

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
	resp = oauth.facebook.get(
		'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
	profile = resp.json()
	print("Facebook User ", profile)
	return redirect('/')

# file not found
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>custom 404 error page</h1>", 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
    return "<h1>custom 500 error page</h1>", 500

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)