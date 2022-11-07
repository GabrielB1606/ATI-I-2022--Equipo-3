from flask import Flask, jsonify, render_template, request
import pymongo
from pymongo import MongoClient
import json

app = Flask(__name__)

# get the connection to mongoDB through a client (this should be a variable... i guess)
def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                        authSource="admin")
    db = client["users_db"]
    return db

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
    return render_template("index.html", postList = posts, lang=lang, language=lan)

# login route
@app.route('/login')
def login():
    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        langs = json.load( open("static/config/es/login.json") )
    else:
        langs = json.load( open("static/config/en/login.json") )
    return render_template("login.html", lang=langs)

# profile route
@app.route('/user')
def profile():
    posts = json.load( open("data/dummy/posts.json") )
    # read GET variable
    lan = request.args.get("lang")
    if lan == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/index.json") )
    else:
        lang = json.load( open("static/config/en/index.json") )
    return render_template("profile.html", postList = posts, lang=lang, language=lan)

# profile route
@app.route('/friend')
def profileFriend():
    posts = json.load( open("data/dummy/posts_friend.json") )
    # read GET variable
    lan = request.args.get("lang")
    if lan == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/index.json") )
    else:
        lang = json.load( open("static/config/en/index.json") )
    return render_template("friend.html", postList = posts, lang=lang, language=lan)

# chat route
@app.route('/chat')
def chat():
    # read GET variable
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        langs = json.load( open("static/config/es/chat.json") )
    else:
        langs = json.load( open("static/config/en/chat.json") )

    chats = json.load( open("data/dummy/chats.json") )
    return render_template("chat.html", chatList = chats, lang=langs)

# config route
@app.route('/config')
def config_page():
    return render_template("config.html")

# updates route
@app.route('/notifications')
def notifications():
    return render_template("notifications.html")

# search all users route
@app.route('/search')
def search_users():
    return render_template("search.html")

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