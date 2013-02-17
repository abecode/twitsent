#!/usr/bin/python
import flask
from flask import Flask
from flask import render_template
#import pymongo
#import random
#import re
#import urlparse
#import json
#from config import *
from collections import defaultdict

MAX_ANNOTATIONS = 25

#for setting up the host name
import subprocess
import sys
host = subprocess.check_output('hostname').strip()
try:
    dns = subprocess.check_output('dnsdomainname').strip()
    if dns:
        host = host + '.' + dns
    else:
        host = subprocess.check_output('hostname -i').strip()
except OSError:
    pass #this happens when you are on a computer not set up as a server 
app = Flask(__name__)
app.secret_key = 'orangeannotation123'
css = '/static/orange.css'

@app.route("/")
def start():
    #blob = flask.request.cookies
    #blob = flask.request.environ
    #if the user is already logged in:
    # if 'sessionid' in flask.session:
    #     if flask.session.get('count') > MAX_ANNOTATIONS:
    #         return flask.redirect(flask.url_for("logout"))
    #     else:
    #         return flask.redirect(flask.url_for("annotate"))
    # #if the user is trying to log in
    # elif flask.request.args.get('cmd')=="login":
        
    #     return flask.redirect(flask.url_for("login"))
    # else:
    return render_template('welcome.html', next="/login")#, blob=blob)

@app.route("/annotate")
def annotate():
    #blob = flask.request.cookies
    blob = flask.request.environ
    sessionid = flask.session.get('sessionid')
    count = flask.session.get('count')
    count += 1
    flask.session['count'] = count
    if flask.session.get('count') > MAX_ANNOTATIONS:
        return flask.redirect(flask.url_for("logout"))
    

    return render_template('annotate.html', 
                           next="/annotate",
                           #css=css, 
                           #blob=blob,
                           sessionid=sessionid,
                           count=count-1)

@app.route("/login")
def login():
    #blob = flask.request.cookies
    blob = flask.request.environ
    if not flask.request.args.get('sessionid'):
            #set username, session id, and count=0 in cookie
            import uuid
            flask.session['sessionid'] = uuid.uuid4()
            flask.session['count'] = 0
            return flask.redirect(flask.url_for('annotate'))
    else:
        #return render_template('login.html', css=css)#, blob=blob)
        return flask.redirect(flask.url_for('annotate'))

@app.route("/logout")
def logout():
    #blob = flask.request.cookies
    blob = flask.request.environ
    sessionid = flask.session.get('sessionid')
    count = flask.session.get('count')
    #return flask.redirect(flask.url_for('dispatch'))
    if flask.request.args.get('cmd') == "restart":
        flask.session.pop('count', None)
        flask.session.pop('sessionid', None)
        return flask.redirect(flask.url_for('start'))
    return render_template('logout.html', css=css,sessionid=sessionid)#, blob=blob)


if __name__ == '__main__':
    #app.run(host="homebrew.usc.edu", debug=True)
    app.run(host='0.0.0.0', debug=True)
