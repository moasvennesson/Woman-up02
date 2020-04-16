from bottle import route, run, template, request, redirect, error, static_file, TEMPLATE_PATH
from datetime import datetime, date
import sqlite3
import os     
abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'views')
abs_static_path = os.path.join(abs_app_dir_path, 'static')
TEMPLATE_PATH.insert(0, abs_views_path )

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=abs_static_path)

@route("/", methods=["GET","POST"])
def login():
    ''' Loginsidan'''
    msg = ""
    if request.method == "POST" and "email" in request.forms and "password" in request.forms:
        email = request.forms.get("email")
        password = request.forms.get("password")
        with sqlite3.connect("woman-up.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM user WHERE email = ? and password = ?")
        cursor.execute(find_user,[(email), (password)])
        account = cursor.fetchone()
        if account:
            msg = "Inloggningen lyckades!"
        else:
            msg = "Inkorrekt email eller lösenord"
               
    return template("index", msg = msg)

@route("/register", methods=["GET","POST"])
def register():
    msg =""
    if request.method == "POST" and "email" in request.forms and "password" in requst.forms and "firstname" in request.forms and "lastname" in request.forms and "phonenumber" in request.forms:
        firstname = request.forms.get("firstname")
        lastname = request.forms.get("lastname")
        phonenumber = request.forms.get("phonenumber")
        password = request.forms.get("password")
        email = requst.forms.get("email")
        with sqlite3.connect("woman-up.db") as db:
            cursor =db.cursor()
        cursor.execute("SELECT * FROM user WHERE email = ?",(email))
        account = cursor.fetchone()
        if account:
            msg = "Den email adressen är reddan registrerad"
        #elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            #msg = "Felaktig email adress"
        elif not username or not password or not email:
            msg="Vänligen uppge all uppgifter"
        else:
            cursor.execute(insertData, [(firstname),(lastname),(phonenumber),(password),(email)])
            db.commit()
    else:   
        msg = "Vänligen fyll i formuläret"  

    return template("register", msg = msg)


run(host='localhost', port=8080, debug=True, reloader=True)