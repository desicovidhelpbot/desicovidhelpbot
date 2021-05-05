import twint
import pandas as pd
import nest_asyncio
nest_asyncio.apply()
import time
import os
import twitter
from flask import Flask, request, make_response, jsonify

app = Flask("desicovidhelpbot")
api = twitter.Api(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token_key=os.getenv("ACCESS_TOKEN_KEY"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)


cityDf = pd.read_csv('desicovidhelpbot/CityWiseData - indian-cities-Latitude-Longitude.csv')
indian_cities = cityDf['City'].tolist()

@app.route("/getTweets", methods=["POST"])
def endpoint():
    query = request.get_json().get("query")
    location = request.get_json().get("location")
    since = request.get_json().get("since")
    output = {"status": "Success"}
    try:
        if since != None:
            get_tweet(query, Location = location, Since=since)
        else:
            get_tweet(query, Location = location)
    except:
        output = {"status": "Failure"}

    return make_response(jsonify(output))


def get_tweet_csv(query, Location = None, Since='2021-04-01'):
    c = twint.Config()
    c.Search = query
    c.Since = Since
    c.Lang = "en"
    c.Limit = 20
    # c.Geo = 
    c.Store_csv = True
    loc = 'All' if Location == None else Location
    current_time = time.strftime("%Y%m%d-%H%M%S")
    filename = 'tweets_query_{}_loc_{}_since_{}_{}.csv'.format(query, loc, Since, current_time)
    filename_final = 'final' + filename
    c.Output = filename
    if Location != None:
        c.Near = Location    
        twint.run.Search(c)
    else:
        for city in indian_cities:
            c.Near = city
            twint.run.Search(c)

    df = pd.read_csv(filename)
    df.drop_duplicates(inplace=True)
    df.to_csv(filename_final, index=False)

def get_follower_count(username):
    friends = api.GetFollowers(screen_name=username)
    friendList = [u.name for u in friends]
    return len(friendList)

def post_reply(tweetID, text):
    api.PostUpdate(status = text, 
    in_reply_to_status_id=tweetID,
    auto_populate_reply_metadata=True)

def get_mentions(Location = None, Since = '2021-04-01'):
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)