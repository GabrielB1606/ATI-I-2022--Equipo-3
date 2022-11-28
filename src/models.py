from flask import Flask,jsonify, redirect,session,request

class User:

    def start_session(self,user):
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user),200

    def login(self,database_hook):
        found = database_hook.usuarios.find_one({ "email": request.form.get("email"), "clave": request.form.get("password") }) 
        
        if not found:
            return jsonify({"message":"Incorrect email address or password"}),400

        user={
            "email": request.form.get('email'),
            "perfil": found["perfil"]
        }
        return self.start_session(user)
        

    def signup(self):
        return ""

    def signout(self):
        session.clear()
        return redirect('/login')