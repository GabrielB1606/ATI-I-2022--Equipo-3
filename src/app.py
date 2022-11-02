from flask import Flask, jsonify, render_template
import pymongo
from pymongo import MongoClient

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
    return render_template("index.html")

# login route
@app.route('/login')
def login():
    return render_template("login.html")

# profile route
@app.route('/user')
def profile():
    return render_template("profile.html")

# chat route
@app.route('/chat')
def chat():
    return render_template("chat.html")

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