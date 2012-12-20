#!/usr/bin/python
import flask
from flask import Flask
from flask import render_template
import pymongo
import iso8601
import random
import re
import urlparse
import json
#from config import *

app = Flask(__name__)

css = '/static/orange.css'

@app.route("/")
def displayOverview():
    return render_template('orangeOverview.html', css=css)

def getDygraphsHourlyVolumeData(year,month,day):
    f = open("static/orange/dayModels/hourlyCounts_%s-%s-%s"%(year,month,day))
    data = []
    for l in f:
        y,m,d,h,v = l.split()
        data.append("\"%s-%s-%s %02d:00:00, %s \\n\""%(y,m,d,int(h),v))
    outString = "+".join(data) + ','
    return outString
def getTweetData(year,month,day):
    f = open("static/orange/%s-%s.tsv"%(year,month))
    data = []
    for l in f:
        tweet,retweet,ts,sentiment,valence,neg,neu,pos,uns  = l.split("\t")
        valence = valence.strip() # address probelm converting to float
        try:
            valence = float(valence)
        except TypeError:
            #valence = 0
            return "'%s'"%x[3]
        #return valence
        mtch = re.search(r'^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):',ts)
        y = int(mtch.group(1))
        m = int(mtch.group(2))
        d = int(mtch.group(3))
        h = int(mtch.group(4))
        if year == y and month == m and day == d:
            #return d
            #data.append((tweet, sentiment, valence))
            data.append((tweet, sentiment, valence))
    f.close()
    output = {'cols':[{'id':'tweet', 'label':'tweet','type':'string'},
                      {'id':'sentiment', 'label':'sentiment','type':'string'},
                      {'id':'valence', 'label':'valence','type':'number'}],
              'rows': []}
    for x in data:
        output['rows'].append({'c':[{'v':x[0]},{'v':x[1]},{'v':float(x[2])}]})
    #output = json.dumps(output)
    return output
    

@app.route('/<path:path>')
def catch_all(path):
    if not app.debug:
        flask.abort(404)
    if path == "favicon.ico":
        flask.abort(404)
    # check if path denotes a day
    m  = re.search(r'^(\d\d\d\d)/(\d\d)/(\d\d)$', path)
    year = int(m.group(1))
    month = int(m.group(2))
    day = int(m.group(3))
    if m:
        requestType=""
        if flask.request.query_string :
            output = {}
            output['table'] = getTweetData(year,month,day)
            output['status'] = 'ok'
            qsDict = urlparse.parse_qs(flask.request.query_string)
            handler = "google.visualization.Query.setResponse"
            gChartOpt = {}
            if 'tqx' in qsDict:
                #return str(qsDict)
                options = qsDict['tqx'][0].split(";")
                gChartOpt = {}
                for o in options:
                    (key,val) = o.split(":")
                    gChartOpt[key]=val
            if 'reqId' in gChartOpt:
                output['reqId'] = gChartOpt['reqId']
            if 'responseHandler' in gChartOpt:
                handler = gChartOpt['responseHandler']
            output = handler + "(" + json.dumps(output) + ")"
            return output
        else:
            requestType = "general" 
            dygraphsTimeData = getDygraphsHourlyVolumeData(year,month,day)
            return render_template('orangeDayView.html', css=css,
                                   dygraphsTimeData=dygraphsTimeData,
                                   year=year,month=month,day=day)
    else:
        flask.abort(404)
        
    # try:
    #     f = open(path)
    # except IOError, e:
    #     flask.abort(404)
    #     return
    # return f.read()

if __name__ == '__main__':
    #app.run(host="homebrew.usc.edu", debug=True)
    app.run(host="localhost", debug=True)
