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
def dispatch():
    #blob = flask.request.cookies
    blob = flask.request.environ
    #if the user is already logged in:
    if flask.request.args.get('cmd')=="login":
        return flask.redirect(flask.url_for("login"))
    #if the user is trying to log in
    if flask.request.args.get('cmd'):
            
        return render_template('login.html', css=css, blob=blob)
    else:
        return render_template('welcome.html', css=css, blob=blob)

@app.route("/annotate")
def annotate():
    #blob = flask.request.cookies
    blob = flask.request.environ
    username = flask.session.get('username')
    sessionid = flask.session.get('sessionid')
    count = flask.session.get('count')
    return render_template('annotate.html', css=css, 
                           blob=blob,
                           username=username,
                           sessionid=sessionid,
                           count=count)

@app.route("/login")
def login():
    #blob = flask.request.cookies
    blob = flask.request.environ
    if flask.request.args.get('username'):
            #set username, session id, and count=0 in cookie
            flask.session['username'] = flask.request.args.get('username')
            import uuid
            flask.session['sessionid'] = uuid.uuid4()
            flask.session['count'] = 0
            return flask.redirect(flask.url_for('annotate'))
    return render_template('login.html', css=css, blob=blob)

@app.route("/logout")
def logout():
    #blob = flask.request.cookies
    blob = flask.request.environ
    return render_template('logout.html', css=css, blob=blob)


if __name__ == '__main__':
    #app.run(host="homebrew.usc.edu", debug=True)
    app.run(host='0.0.0.0', debug=True)
