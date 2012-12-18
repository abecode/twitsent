from flask import Flask
from flask import render_template
import pymongo
import iso8601
import random
#from config import *

app = Flask(__name__)

css = '/static/orange.css'

@app.route("/")
def displayOverview():
                        
    return render_template('orangeOverview.html', css=css)


if __name__ == '__main__':
    app.run(host="homebrew.usc.edu", debug=True)
