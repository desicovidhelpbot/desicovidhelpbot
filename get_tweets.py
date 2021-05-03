import twint
import pandas as pd
import nest_asyncio
nest_asyncio.apply()
import time


cityDf = pd.read_csv('CityWiseData - indian-cities-Latitude-Longitude.csv')
indian_cities = cityDf['City'].tolist()

def get_tweet(query, Location = None, Since='2021-01-01'):
    c = twint.Config()
    c.Search = query
    c.Since = Since
    c.Store_csv = True
    loc = 'All' if Location == None else Location
    current_time = time.strftime("%Y%m%d-%H%M%S")
    filename = 'tweets_query_{}_loc_{}_since_{}_{}.csv'.format(query, loc, Since, current_time)
    c.Output = filename
    if Location != None:
        c.Near = Location    
        twint.run.Search(c)
    else:
        for city in indian_cities:
            c.Near = city
            twint.run.Search(c)

if __name__ == '__main__':
    get_tweet("@desicovidhelper", 'Kolkata')