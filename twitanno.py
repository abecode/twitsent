from flask import Flask
from flask import render_template
import pymongo
import iso8601
import random
from config import *

app = Flask(__name__)

css = '/static/style.css'

@app.route("/")

def display_from_db():
    testvar = "test successful"

    connection = pymongo.Connection(CONFIGMONGOHOST, CONFIGMONGOPORT)
    db = connection.debate
    # print db.collection_names()
    oct3 = db.oct16
    
    DEBATE_START = '2012-10-17T01:40:00.000Z'
    DEBATE_START_DT = iso8601.parse_date(DEBATE_START)
    # print DEBATE_START_DT
    
    DEBATE_END = '2012-10-17T02:00:00.000Z'
    DEBATE_END_DT = iso8601.parse_date(DEBATE_END)
    # print DEBATE_END_DT
    
    RANDNUM = random.randint(1,500000)
    
    query_result = oct3.find({'postedTimeObj': {'$gte':DEBATE_START_DT, '$lte':DEBATE_END_DT}}).skip(RANDNUM).limit(1)
    # query_result = oct3.find({'postedTimeObj': {'$gte':DEBATE_START_DT, '$lte':DEBATE_END_DT}}).limit(10000)

    
    for x in query_result:
    #     print x
        tweet_text = x['body']
#         print tweetbody
        tweet_created_at = x['postedTimeObj']
#         print tweet_posted_at
        tweet_id = x['id_str'] 
        username  = x['actor']['preferredUsername']
        user_bio = x['actor']['summary']
        user_avatar_url = x['actor']['image']
        user_url = x['actor']['link']                    
                    
                    
                        
    return render_template('index.html', testvar=testvar, tweet_text=tweet_text, tweet_created_at=tweet_created_at, tweet_id=tweet_id, username=username, user_bio=user_bio, user_avatar_url=user_avatar_url, user_url=user_url, css=css)


if __name__ == '__main__':
    app.run(host="68.181.174.147", debug=True)