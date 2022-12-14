from flask import Flask,jsonify, redirect,session,request
from  werkzeug.security import check_password_hash
from config import database_hook

class User:

    def start_session(self,user):
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user),200

    def login(self,database_hook,email,password):
        found = database_hook.usuarios.find_one({ "email": email }) 
        
        if (not found) or ( not check_password_hash( found["clave"], password) ) :
            return jsonify({"message":"Incorrect email address or password"}),400

        user={
            "email": email,
            "perfil": found["perfil"]
        }
        return self.start_session(user)
    
    # login with email and password
    def login_email(self, email, password):
        found = database_hook.usuarios.find_one({ "email": email }) 
        
        if (not found) or ( not check_password_hash( found["clave"], password ) ) :
            return jsonify({"message":"Incorrect email address or password"}),400

        user={
            "email": email,
            "perfil": found["perfil"]
        }
        return self.start_session(user)
        

    def signup(self):
        return ""

    def signout(self):
        session["logged_in"] = False
        session['user'] = None
        session.clear()