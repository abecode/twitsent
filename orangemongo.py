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
from datetime import datetime

#from config import *
from collections import defaultdict
from pymongo import MongoClient

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

css = '/static/orange.css'

# Setting up the parameters for connecting to Mongo

connection = MongoClient(host)
db = connection.sasa
collection = db.analysedtweets
archive = db.archivedtweets

@app.route("/")
def displayOverview():
    dygraphsData = getDygraphsDailyVolumeData()
    return render_template('orangeOverview.html', css=css,
                           dygraphsTimeData=dygraphsData)

def getDygraphsDailyVolumeData():
    columns = ['tweet','retweets','date','sentiment','valence','negative','neutral','positive','unsure']
    dayCounts = defaultdict(int)
    dayList = []
    for entry in archive.find():
        date = entry['timeStamp']
        #print entry
        #m = re.search(r'^(....)-(..)-(..)T(..)',date)
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        #    month, day, hour = map(lambda x: getattr(re.search(r'^(....)-(..)-(..)T(..)',date), 'group')(x), [1,2,3,4])
        dayCounts[(year,month,day)] +=1
        if dayCounts[(year,month,day)] == 1:
            dayList.append((year,month,day))
    data = []
    for day in dayList:
        y,m,d = day
        volume = dayCounts[day]
        data.append("\"%s-%s-%s, %s \\n\""%(y,m,d,volume))
    outString = "+".join(data) + ','
    return outString
        
def getDygraphsHourlyVolumeData(year,month,day):
    f = open("static/orange/dayModels/hourlyCounts_%s-%s-%s"%(year,month,day))
    data = []
    for l in f:
        y,m,d,h,v = l.split()
        data.append("\"%s-%s-%s %02d:00:00, %s \\n\""%(y,m,d,int(h),v))
    outString = "+".join(data) + ','
    return outString

def getDygraphsHourlyVolumeData_new(searchYear,searchMonth,searchDay):
    # setup column labes
    columns = ['tweet','retweets','date','sentiment','valence','negative','neutral','positive','unsure']
    
    #dayModelFile = AutoVivification()
    hourlyDict = defaultdict(int)
    #dayModelFile = OrderedDict(int)
    dayList = []
    data = []

    #TO-DO : Check if find() returns all entries or just the first 20. Also find the difference between find() and find({})

    for entry in collection.find():
    # for line in open("static/orange/2012-12.tsv"):
        # fields = line.split('\t')
        # date = fields[columns.index('date')]
        date = entry['date']
        m = re.search(r'^(....)-(..)-(..)T(..)',date)
        year = int(m.group(1))
        month = int(m.group(2))
        day = int(m.group(3))
        hour = int(m.group(4))
    #    month, day, hour = map(lambda x: getattr(re.search(r'^(....)-(..)-(..)T(..)',date), 'group')(x), [1,2,3,4])
        if year ==searchYear and month==searchMonth and day==searchDay: 
            hourlyDict[hour] +=1
    data = []
    for hr in range(0,24):
        data.append("\"%s-%s-%s %02d:00:00, %s \\n\""%(searchYear,
                                                       searchMonth,
                                                       searchDay,
                                                       hr,hourlyDict[hr]))
    outString = "+".join(data) + ','
    return outString

#TO-DO : This probably can be done with date range queries on mongo find()
#TO-DO : Check if the date inserted in mongoDB is in the python date time format

def getTweetData(year,month,day):
    f = open("static/orange/%s-%s.tsv"%(year,month))
    data = []
    for l in f:
        tweet,retweet,ts,sentiment,valence,neg,neu,pos,uns  = l.split("\t")
        valence = valence.strip() # address probelm converting to float
        try:
            valence = float(valence)*100 #scale to -100,100 for display purposes
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
    

#@app.route('/<path:path>')
#def catch_all(path):
@app.route('/<int:year>/<int:month>/<int:day>')
def catch_all(year,month,day):
    if not app.debug:
        flask.abort(404)
#    if path == "favicon.ico":
#        flask.abort(404)
    # check if path denotes a day
#    m  = re.search(r'^(\d\d\d\d)/(\d\d)/(\d\d)$', path)
#    year = int(m.group(1))
#    month = int(m.group(2))
#    day = int(m.group(3))
#if m:
    if True:
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
            dygraphsTimeData = getDygraphsHourlyVolumeData_new(year,month,day)
            return render_template('orangeDayView.html', css=css,
                                   dygraphsTimeData=dygraphsTimeData,
                                   year=year,month=month,day="%02d"%day,
                                   host=host)
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
    app.run(host='0.0.0.0', debug=True)
