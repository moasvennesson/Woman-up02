from bottle import route, run, template, request, redirect, error, static_file, TEMPLATE_PATH, get, post, hook, app
from bottle.ext import beaker # Import session beaker
from datetime import datetime, date
import sqlite3
import os
import datetime
import json
import websockets
abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, "views")
abs_static_path = os.path.join(abs_app_dir_path, "static")
TEMPLATE_PATH.insert(0, abs_views_path)


# Settings for the session
session_opts = {
    "session.type": "file",
    "session.cookie_expires": True,
    "session.data_dir": "./data",
    "session.auto": True
}


# Activate sessions for the app
app = beaker.middleware.SessionMiddleware(app(), session_opts)


# Added hook for easier access to session
@hook("before_request")
def setup_request():
    request.session = request.environ["beaker.session"]


@route("/static/<filename>")
def server_static(filename):
    return static_file(filename, root=abs_static_path)


@route("/startpage")
def startpage():
    if "logged-in" in request.session:
        if request.session["logged-in"] == True:
            email = request.session["email"]
            conn = sqlite3.connect("woman-up.db")
            c = conn.cursor()
            c.execute("SELECT first_name FROM user WHERE email = ?", (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template("startpage", user = uid)
            
    else:
        redirect("/")


@route("/", method=["POST", "GET"]) 
def login():
    '''The login page, checks if the e-mail and password in the html form is in the sqlite database'''
    msg = ""
    if request.method == "POST":
        email = getattr(request.forms, "email")
        password = getattr(request.forms, "password")
        conn = sqlite3.connect("woman-up.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE email = ? and password = ?",(email, password))
        user = c.fetchone() 
        if user:
            # Save logged in user in session
            request.session["logged-in"] = True
            request.session["email"] = email
            inloggad = email
            print(inloggad)

            redirect("/startpage") 
        else:
            msg = "Inkorrekt email eller lösenord"

    return template("index", msg=msg)


@route("/logout")
def logout():
    if "logged-in" in request.session:
        request.session["logged-in"] = False
        redirect("/")


@route("/register", method=["POST", "GET"])
def register():
    '''Registers a new user in the database and also checks if the e-mail is already in use'''
    msg = ""
    if request.method =="POST":
        firstname = getattr(request.forms, "firstname")
        lastname = getattr(request.forms, "lastname")
        password = getattr(request.forms, "password")
        email = getattr(request.forms, "email")
        conn = sqlite3.connect("woman-up.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE email = ?", (email,))
        if c.fetchone():
            msg = "Den email adressen är redan registrerad"
        elif not password or not email:
            msg = "Vänligen uppge all uppgifter"
        else:
            c.execute("INSERT INTO user VALUES(?,?,?,?)",(firstname, lastname, password, email,))
            conn.commit()
            redirect("/updateaccount")

    return template("register", msg=msg)


@route("/updateaccount")
def updateaccount():
    return template("updateaccount")


@route("/settings", method=["POST", "GET"])
def settings():
    msg = ""
    success_msg =""
    if "logged-in" in request.session:
        if request.session["logged-in"] == True:
            email = request.session["email"]
            conn = sqlite3.connect("woman-up.db")
            c = conn.cursor()
            c.execute("SELECT first_name FROM user WHERE email = ?", (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            if request.method == "POST":
                password = getattr(request.forms, "password")
                new_password = getattr(request.forms, "new_password")
                c.execute("SELECT * FROM user WHERE email = ? and password = ?",(email, password))
                found_user = c.fetchone()
                if found_user:
                    sql_update_query = """Update user set password = ? where email = ?"""
                    data = (new_password, email)
                    c.execute(sql_update_query,data)
                    conn.commit()
                    success_msg = "Lyckades byta lösenord"
                    c.close()
                else:
                    msg = "Fel lösenord"
       
        return template("settings", msg=msg, user=uid,success_msg=success_msg)

    else:
        redirect("/")


@route("/FullPrivacyPolicy")
def popup():
    return template("FullPrivacyPolicy")


@route("/map", method=["POST", "GET"])
def map(): 
    global Listarop
    if "logged-in" in request.session:
        if request.session["logged-in"] == True:
            email = request.session["email"]
            conn = sqlite3.connect("woman-up.db")
            c = conn.cursor()
            c.execute("SELECT first_name FROM user WHERE email = ?", (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            print(uid)
            print(Listarop)
            return template("map",Listarop=Listarop, user = uid)
    else:
        redirect("/")

Listarop = []


@route("/remove")
def remove_emergency():
    global Listarop
    if "logged-in" in request.session:
        if request.session["logged-in"] == True:
            email = request.session["email"]
            Listarop.clear()
            redirect("/map")


@route("/emergency",method=["POST", "GET"])
def emergency():
    global Listarop
    if "logged-in" in request.session:
        if request.session["logged-in"] == True:
            email = request.session["email"]
            conn = sqlite3.connect("woman-up.db")
            c = conn.cursor()
            c.execute("SELECT first_name FROM user WHERE email = ?", (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            if request.method == "POST":
                Etext=getattr(request.forms, "Truta")
                datum = datetime.datetime.now()
                pos = getattr(request.forms, "pos")
                listan = [Etext,uid,datum,pos]
                Listarop.append(listan)
                redirect("/map")
            return template("emergency", email = email, user = uid,)
    
    else:
        redirect("/")


@route("/external-links")
def hamburgare():
    if "logged-in" in request.session:
        if request.session["logged-in"] == True:
            email = request.session["email"]
            conn = sqlite3.connect("woman-up.db")
            c = conn.cursor()
            c.execute("SELECT first_name FROM user WHERE email = ?", (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template("external-links", user = uid)
            
    else:
        redirect("/")


@route("/PrivacyPolicy")
def PrivacyPolicy():
    if "logged-in" in request.session:
        if request.session["logged-in"] == True:
            email = request.session["email"]
            conn = sqlite3.connect("woman-up.db")
            c = conn.cursor()
            c.execute("SELECT first_name FROM user WHERE email = ?", (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template("PrivacyPolicy", user = uid)
        
    else:
        redirect("/")
    

@route("/FAQ")
def FAQ():
    if "logged-in" in request.session:
        if request.session["logged-in"] == True:
            email = request.session["email"]
            conn = sqlite3.connect("woman-up.db")
            c = conn.cursor()
            c.execute("SELECT first_name FROM user WHERE email = ?", (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template("FAQ", user = uid)
            
    else:
        redirect("/")
    

@route("/chatt")
def chatt():
    if "logged-in" in request.session:
        if request.session["logged-in"] == True:
            email = request.session["email"]
            conn = sqlite3.connect("woman-up.db")
            c = conn.cursor()
            c.execute("SELECT first_name FROM user WHERE email = ?", (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template("chatt", user = uid, email = email)
    else:
        redirect("/")


run(app=app, host='localhost', port=9090, debug=True, reloader=True) # Updated according to documentation with 'app=app'