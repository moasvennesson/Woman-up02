from bottle import route, run, template, request, redirect, error, static_file
from datetime import datetime, date

@route("/")
def show_homepage():
    ''' Hemsidan '''
    return template("index")