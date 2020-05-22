from bottle import route, run, template, request, redirect, error, static_file, TEMPLATE_PATH, get, post, hook, app
from bottle.ext import beaker # Import session beaker
from datetime import datetime, date
import sqlite3
import os
import datetime
import json
import websockets
abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'views')
abs_static_path = os.path.join(abs_app_dir_path, 'static')
TEMPLATE_PATH.insert(0, abs_views_path)


# Settings for the session
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.data_dir': './data',
    'session.auto': True
}

# Activate sessions for the app
app = beaker.middleware.SessionMiddleware(app(), session_opts)

# Added hook for easier access to session
@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=abs_static_path)


@route('/startpage')
def startpage():
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            email = request.session['email']
            conn = sqlite3.connect('woman-up.db')
            c = conn.cursor()
            c.execute('SELECT first_name FROM user WHERE email = ?', (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template('startpage', user = uid)
            
    else:
        return "Inte in loggade!"


@route('/', method=['POST', 'GET']) 
def login():
    ''' Loginsidan, hämtar email och password från HTML formuläret,
    ansluter till sqlite databasen woman-up och kollar om de uppgifterna finns'''
    msg = ""
    if request.method == 'POST':
        email = getattr(request.forms, 'email')
        password = getattr(request.forms, 'password')
        conn = sqlite3.connect('woman-up.db')
        c = conn.cursor()
        c.execute('SELECT * FROM user WHERE email = ? and password = ?',(email, password))
        user = c.fetchone() 
        if user:
            # Save logged in user in session
            request.session['logged-in'] = True
            request.session['email'] = email
            inloggad = email
            print(inloggad)

            redirect('/startpage') 
        else:
            msg = 'Inkorrekt email eller lösenord'

    return template('index', msg=msg)


@route('/logout')
def logout():
    if "logged-in" in request.session:
        request.session['logged-in'] = False
        redirect("/")


@route('/register', method=['POST', 'GET'])
def register():
    '''Registerar en ny användare i databasen och kollar om mailen redan är registrerad'''
    msg = ""
    if request.method =='POST':
        firstname = getattr(request.forms, 'firstname')
        lastname = getattr(request.forms, 'lastname')
        phonenumber = getattr(request.forms, 'phonenumber')
        password = getattr(request.forms, 'password')
        email = getattr(request.forms, 'email')
        conn = sqlite3.connect('woman-up.db')
        c = conn.cursor()
        c.execute('SELECT * FROM user WHERE email = ?', (email,))
        if c.fetchone():
            msg = 'Den email adressen är redan registrerad'
        elif not password or not email:
            msg = 'Vänligen uppge all uppgifter'
        else:
            c.execute('INSERT INTO user VALUES(?,?,?,?,?,?,?,?)',(firstname, lastname, phonenumber, password, email, None, None, None))
            conn.commit()
            redirect('/updateaccount')

    return template('register', msg=msg)

@route('/updateaccount')
def updateaccount():
    return template('updateaccount')

@route('/login-status')
def login_status():
    '''Demo page to see if a user logged in'''
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            return "User logged in with: " + request.session['email']
    else:
        return "Not logged in!"


@route('/FullPrivacyPolicy')
def popup():
    return template('FullPrivacyPolicy')


@route('/map', method=['POST', 'GET'])
def map(): 
    global Listarop
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            email = request.session['email']
            conn = sqlite3.connect('woman-up.db')
            c = conn.cursor()
            c.execute('SELECT first_name FROM user WHERE email = ?', (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            print(uid)
            print(Listarop)
            return template('map',Listarop=Listarop, user = uid)
    else:
        return "Inte in loggade!"

Listarop = []


@route("/remove")
def remove_emergency():
    global Listarop
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            email = request.session['email']
            Listarop.clear()
            redirect("/map")


@route('/emergency',method=['POST', 'GET'])
def emergency():
    global Listarop
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            email = request.session['email']
            conn = sqlite3.connect('woman-up.db')
            c = conn.cursor()
            c.execute('SELECT first_name FROM user WHERE email = ?', (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            if request.method == 'POST':
                Etext=getattr(request.forms, 'Truta')
                datum = datetime.datetime.now()
                pos = getattr(request.forms, 'pos')
                listan = [Etext,uid,datum,pos]
                Listarop.append(listan)
                redirect("/map")
            return template('emergency', email = email, user = uid,)
    else:
        return "Inte in loggade!"


@route('/hamburgare')
def hamburgare():
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            email = request.session['email']
            conn = sqlite3.connect('woman-up.db')
            c = conn.cursor()
            c.execute('SELECT first_name FROM user WHERE email = ?', (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template('hamburgare', user = uid)
            
    else:
        return "Inte in loggade!"


@route('/PrivacyPolicy')
def PrivacyPolicy():
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            email = request.session['email']
            conn = sqlite3.connect('woman-up.db')
            c = conn.cursor()
            c.execute('SELECT first_name FROM user WHERE email = ?', (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template('PrivacyPolicy', user = uid)
            
    else:
        return "Inte in loggade!"
    


@route('/FAQ')
def FAQ():
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            email = request.session['email']
            conn = sqlite3.connect('woman-up.db')
            c = conn.cursor()
            c.execute('SELECT first_name FROM user WHERE email = ?', (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template('FAQ', user = uid)
            
    else:
        return "Inte in loggade!"
    


@route('/profilsida')
def profilsida():
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            email = request.session['email']
            conn = sqlite3.connect('woman-up.db')
            c = conn.cursor()
            c.execute('SELECT first_name FROM user WHERE email = ?', (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template('profilsida', user = uid)
            
    else:
        return "Inte in loggade!"
    


@route("/chatt")
def chatt():
    if "logged-in" in request.session:
        if request.session['logged-in'] == True:
            email = request.session['email']
            conn = sqlite3.connect('woman-up.db')
            c = conn.cursor()
            c.execute('SELECT first_name FROM user WHERE email = ?', (email,))
            user = c.fetchone()
            uid=str(user).strip("(,')")
            return template('chatt', user = uid, email = email)
    else:
        return "Inte in loggade!"


run(app=app, host='localhost', port=9087, debug=True, reloader=True) # Updated according to documentation with 'app=app'
