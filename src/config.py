from flask import Flask, jsonify, render_template, request, url_for, redirect, send_file, session
from models import User
from functools import wraps
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from  werkzeug.security import generate_password_hash, check_password_hash
import json
import gridfs

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
oauth = None

def get_navbar_lang(lang):
    if request.args.get("lang") == "es":
        lang["navbar"] = json.load( open("static/config/es/navbar.json") )
    else:
        lang["navbar"] = json.load( open("static/config/en/navbar.json") )

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

def logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return redirect('/')
        else:
            return f(*args, **kwargs)
    return wrap