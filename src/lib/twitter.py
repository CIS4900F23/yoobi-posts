"""Class that handles tweets for our backend API"""
import os
import json
from datetime import datetime
import tweepy

class Twitter:
    """Class that handles tweets for our backend API"""    
    def __init__(self):
        self.tweepy_client = tweepy.Client(os.environ.get("BEARER_TOKEN"))       
        self.tweet_list = []

    def getTweepyBearerToken(self):
        return self.tweepy_client.bearer_token

    def getRecentTweets(self, query: str, limit: float) -> int:
        """Returns a list of recent tweets"""
        query_result = tweepy.Paginator(
        self.tweepy_client.search_recent_tweets,
        query=query,
        tweet_fields=['created_at', 'author_id'],
        max_results=100
        ).flatten(limit=limit)

        # Save Tweets to memory as Tweet objects.
        for tweet in query_result:
            self.tweet_list.append(
                self.Tweet(
                    tweet.id,
                    tweet.author_id,
                    tweet.created_at,
                    tweet.text
                )
            )

    def emptyList(self):
        self.tweet_list.clear()
        
    def getNumTweets(self):
        """Returns the number of tweets"""
        return len(self.tweet_list)

    def toString(self):
        """Prints the tweet list"""
        tString = ""
        for tweet in self.tweet_list:
            tString += "\n" + tweet.toString()

        return tString

    def writeToJSON(self, filename):
        """Writes the tweet list to a JSON file"""
        file_dict = {
            "date" : str(datetime.now())
        }

        tweet_list = []
        for tweet in self.tweet_list:      
            tweet_list.append(tweet.toDict())

        file_dict["data"] = tweet_list
        obj = json.dumps(file_dict)

        with open(filename, "w", encoding="UTF-8") as file:
            file.write(obj)

        return 1

    def readFromJSON(self, filename):
        """Reads the tweet list from a JSON file"""
        with open(filename, "r", encoding="UTF-8") as file:
            obj = json.load(file)
            data = obj["data"]
            for l in data:
                self.tweet_list.append(
                    self.Tweet(l["_id"],
                    l["author_id"],
                    l["created_at"],
                    l["content"])
                )

    class Tweet:
        """Class that represents a tweet as a data type"""
        def __init__(self, tweet_id, author_id, created_at, text):
            self.id  = tweet_id
            self.author_id = author_id
            self.created_at = created_at
            self.text = text

        def toString(self):
            """Returns a string representation of the tweet"""
            return f"tweet_id: {self.id}\nauthor_id: {self.author_id}\ncreated_at: {self.created_at}\ncontent: {self.text}\n"

        def toDict(self):
            """Returns a dictionary representation of the tweet"""
            return {
                "_id" : str(self.id),
                "author_id" : str(self.author_id),
                "created_at" : str(self.created_at),
                "content" : str(self.text)
            }
