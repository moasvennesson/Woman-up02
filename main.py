from bottle import route, run, template, request, redirect, error, static_file, TEMPLATE_PATH
from datetime import datetime, date
import os     
abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'views')
abs_static_path = os.path.join(abs_app_dir_path, 'static')
TEMPLATE_PATH.insert(0, abs_views_path )

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=abs_static_path)

@route("/")
def show_homepage():
    ''' Hemsidan '''
    return template("index")

run(host='localhost', port=8080, debug=True, reloader=True)