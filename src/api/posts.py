"""API route for handling anything that pertains to tweets"""
import random
import gzip
import json
from flask import make_response
from flask_restx import Namespace, Resource
from src.db.connect import DBConnect
from src.lib.languageProcessing import LanguageProcessing

api = Namespace('posts', description='Post related operations')
dbc = DBConnect()

def compressData(data):
    """
    Compress a post response using gzip.
    """
    zipped_data = gzip.compress(json.dumps(data).encode('utf-8'), 5)
    response = make_response(zipped_data)
    response.headers['Content-Encoding'] = 'gzip'

    return response

class Tweets(Resource):
    """
    Handles API calls for all tweets.
    """
    def get(self):
        """Get string representation of the Twitter data.."""
        data = dbc.getCollection(dbc.DB, dbc.TWITTER)
        response = compressData(data)
        return response

    def post(self):
        """Add a new list of tweets."""

class Tweet(Resource):
    """
    Handles single tweet api calls.
    """

    def get(self, tweet_id):
        """Get a tweet by ID."""

    def put(self, tweet_id):
        """Update a tweet by ID."""

    def delete(self, tweet_id):
        """Delete a tweet by ID."""
    
class Reddit(Resource):
    """
    Handles API calls for all Reddit data.
    """
    def get(self):
        """Get a string representation of the Reddit data."""

        data = dbc.getCollection(dbc.DB, dbc.REDDIT)
        response = compressData(data)
        return response

class Random(Resource):
    """
    Returns a random post.
    """
    def get(self):
        """Get a random post"""

        rand = random.randint(0, 1)

        if rand == 0:
            tweet = dbc.getRandomDocument("UBI", dbc.TWITTER)
            data = {"text" : str(tweet["content"]), "id": str(tweet["_id"]), "date": str(tweet["created_at"]), "comments": None, "type": "tweet"}
            response = compressData(data)
        
        if rand == 1:
            reddit = dbc.getRandomDocument("UBI", dbc.REDDIT)
            data = {"text" : str(reddit["content"]), "id": str(reddit["_id"]), "date": str(reddit["created_at"]), "comments": reddit["comments"], "type": "reddit"}
            response = compressData(data)
        
        return response

class SizeAll(Resource):
    """
    Return total number of tweets and reddit posts.
    """
    def get(self):
        """
        Get total number of tweets and reddit posts.
        """
        collection_size = dbc.getCollectionSize("UBI", dbc.TWITTER) + dbc.getCollectionSize("UBI", dbc.REDDIT)
        data = {"size": collection_size}
        response = compressData(data)

        return response
    
class SizeTweets(Resource):
    """
    Return total number of tweets from database collection.
    """
    def get(self):
        """
        Get total number of tweets from database collection.
        """
        collection_size = dbc.getCollectionSize("UBI", dbc.TWITTER)
        data = {"size": collection_size}
        response = compressData(data)

        return response
    
class SizeReddit(Resource):
    """
    Return total number of reddit posts.
    """
    def get(self):
        """
        Get total number of reddit posts.
        """
        collection_size = dbc.getCollectionSize("UBI", dbc.REDDIT)
        data = {"size": collection_size}
        response = compressData(data)

        return response


class Sentiment(Resource):
    """
    Handles sentiment api calls on tweets
    """
    def get(self, post_id:str):
        """
        Get the sentiment of a post by ID
        """
        lp = LanguageProcessing()
        doc = dbc.getDocumentById("UBI", dbc.TWITTER, post_id)
        tweet_text = str(doc["content"])
        sentiment = lp.getSentiment(tweet_text)
        data = {'Sentiment Analysis': sentiment}
        response = compressData(data)

        return response


# Define routes for the API
api.add_resource(Tweets, "/tweets")
api.add_resource(Tweet, "/<string:post_id>")
api.add_resource(Reddit, "/reddit")
api.add_resource(Random, "/random")
api.add_resource(SizeAll, "/size")
api.add_resource(SizeTweets, "/tweets/size")
api.add_resource(SizeReddit, "/reddit/size")
api.add_resource(Sentiment, "/sentiment/<string:post_id>")