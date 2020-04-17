from bottle import route, run, template, request, redirect, error, static_file, TEMPLATE_PATH, get, post
from datetime import datetime, date
import sqlite3
import os
abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'views')
abs_static_path = os.path.join(abs_app_dir_path, 'static')
TEMPLATE_PATH.insert(0, abs_views_path)


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=abs_static_path)


@route("/startpage")
def startpage():
    return template("startpage")

@get("/")
def login_page():
       return template("index", msg="")

@post("/")
def login():
    ''' Loginsidan'''
    msg = ""
    if  "email" in request.forms and "password" in request.forms:
        email = request.forms.get("email")
        password = request.forms.get("password")
        with sqlite3.connect("woman-up.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM user WHERE email = ? and password = ?")
        cursor.execute(find_user, [(email), (password)])
        account = cursor.fetchall()
        if account:
            redirect("/startpage")
    else:
        msg = "Inkorrekt email eller lösenord"

    return template("index", msg=msg)

@get("/register")
def register_page():
        return template("register", msg="")

@post("/register")
def register():
    msg = ""
    if  "email" in request.forms and "password" in requst.forms and "firstname" in request.forms and "lastname" in request.forms and "phonenumber" in request.forms:
        firstname = request.forms.get("firstname")
        lastname = request.forms.get("lastname")
        phonenumber = request.forms.get("phonenumber")
        password = request.forms.get("password")
        email = request.forms.get("email")
        with sqlite3.connect("woman-up.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM user WHERE email =?")
        cursor.execute(find_user[(email)])

        if cursor.fetchall():
            msg = "Den email adressen är reddan registrerad"
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            #msg = "Felaktig email adress"
        elif not username or not password or not email:
            msg = "Vänligen uppge all uppgifter"
        else:
            insertdata ='''INSERT INTO user (first_name, last_name, tel_num, password, email)
            VALUES(?,?,?,?,?)'''
            cursor.execute(insertdata[(firstname),(lastname),(phonenumber),(password),(email)])
            db.commit()
            redirect("/")
    else:
        msg = "Vänligen fyll i formuläret"

    return template("register", msg=msg)


run(host='localhost', port=8080, debug=True, reloader=True)
