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

inloggad = 'None'

# Settings for the session
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
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
    email = request.query.get('email')
    return template('startpage', email = email)


@route('/', method=['POST', 'GET']) 
def login():
    global inloggad
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
            inloggad = email
            print(inloggad)

            # Save logged in user in session
            request.session['logged-in'] = True
            request.session['email'] = email

            redirect('/startpage?email={}'.format(user[4])) 
        else:
            msg = 'Inkorrekt email eller lösenord'

    return template('index', msg=msg)


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
            msg = 'Den email adressen är reddan registrerad'
        elif not password or not email:
            msg = 'Vänligen uppge all uppgifter'
        else:
            c.execute('INSERT INTO user VALUES(?,?,?,?,?,?,?,?)',(firstname, lastname, phonenumber, password, email, None, None, None))
            conn.commit()
            redirect('/')

    return template('register', msg=msg)

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
    global inloggad
    print(inloggad)
    print(Listarop)
    return template('map',Listarop=Listarop)

Listarop = []


@route('/emergency',method=['POST', 'GET'])
def emergency():
    global inloggad
    global Listarop
    email = 'test'
    if request.method == 'POST':
        Etext=getattr(request.forms, 'Truta')
        datum = datetime.datetime.now()
        pos = getattr(request.forms, 'pos')
        listan = [Etext,inloggad,datum,pos]
        Listarop.append(listan)
        redirect("/map")
    return template('emergency', email = email)


@route('/hamburgare')
def hamburgare():
    return template('hamburgare')


@route('/PrivacyPolicy')
def PrivacyPolicy():
    return template('PrivacyPolicy')


@route('/FAQ')
def FAQ():
    return template('FAQ')


@route('/chatt')
def chatt():
    email = request.query.get('email')
    return template('chatt', email = email)


run(app=app, host='localhost', port=9082, debug=True, reloader=True) # Updated according to documentation with 'app=app'
