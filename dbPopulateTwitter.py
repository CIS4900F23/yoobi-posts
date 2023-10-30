import pymongo
# from src.lib.twitter import Twitter
from src.db.connect import DBConnect

# twitter = Twitter()
dbc = DBConnect()
QUERY = '("universal basic income") -is:retweet -is:reply -has:links -has:media lang:en'

# twitter.getRecentTweets(QUERY, 1000)
# twitter.writeToJSON("tweets.json")

try:
    dbc.writeFileToCollection(dbc.DB, dbc.TWITTER, "tweets.json")
except pymongo.errors.BulkWriteError as e:
    print("BulkWriteError occured, likely due to duplicate posts. Non duplicate posts should have been added.")