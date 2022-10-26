from flask import Flask, jsonify, render_template
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                        authSource="admin")
    db = client["users_db"]
    return db

@app.route('/')
def ping_server():
    return render_template("index.html")

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

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)