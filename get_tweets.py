import twint
import pandas as pd
import nest_asyncio
nest_asyncio.apply()
import time
import twitter

from passwords import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET

api = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN_KEY,
    access_token_secret=ACCESS_TOKEN_SECRET
)


cityDf = pd.read_csv('CityWiseData - indian-cities-Latitude-Longitude.csv')
indian_cities = cityDf['City'].tolist()

def get_tweet(query, Location = None, Since='2021-04-01'):
    c = twint.Config()
    c.Search = query
    c.Since = Since
    c.Lang = "en"
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

def get_mentions(Location = None, Since = '2021-04-01' ):
    pass

if __name__ == '__main__':
    import sys
    # qstring = sys.argv[1]
    # location = sys.argv[2]
    # date = sys.argv[3]
    # get_tweet(qstring, location, date)
    username = sys.argv[1]
    get_follower_count(username)
    post_reply(1388878996981518339, "lead found 2")