from flask import Flask,jsonify, redirect,session,request

class User:

    def start_session(self,user):
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user),200

    def login(self):
        user={
            "email": request.form.get('email')
        }
        self.start_session(user)
        return "done"
        

    def signup(self):
        return ""

    def signout(self):
        session.clear()
        return redirect('/login')