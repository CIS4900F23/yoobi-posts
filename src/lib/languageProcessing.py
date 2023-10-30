"""Class that handles Language Processing for our backend"""
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#Expecting the use of NLTK, plotly, pandas, and scikit-learn

class LanguageProcessing:
    """Class that handles Language Processing for our backend"""
    def __init__(self):
        """Initializes the VADER sentiment analyzer"""
        self.sentiment_analysis = SentimentIntensityAnalyzer()

    def getSentiment(self, text):
        """Return sentiment analysis data as pandas dataframe"""
        return self.sentiment_analysis.polarity_scores(text)

    def sentimentToDataFrame(self, sentiment_scores: dict):
        """Return sentiment analysis data as pandas dataframe"""
        sent = ['Negative', 'Neutral', 'Positive', 'Compound']
        vals = sentiment_scores.values()

        df = pd.DataFrame(sent, columns=['Sentiment'])
        df['Sentiment Score'] = vals

        return df

    def getDatabaseSentiment(self, dbc):
        """Return sentiment analysis of entire database collection"""
        db = dbc.client["UBI"]

        twitter_col = db[dbc.TWITTER]
        reddit_col = db[dbc.REDDIT]

        twitter_list = []
        reddit_list = []

        #Build string with all tweets
        for document in twitter_col.find({}):
            tmp_tweet_list = (str(document["content"])).split()
            twitter_list.extend(tmp_tweet_list)

        #Build string with all reddit posts
        for document in reddit_col.find({}):
            tmp_reddit_list = (str(document["content"])).split()
            reddit_list.extend(tmp_reddit_list)

        #get sentiment for tweets
        twitter_sentiment = self.getSentiment(' '.join(twitter_list))

        #get sentiment for reddit posts
        reddit_sentiment = self.getSentiment(' '.join(reddit_list))

        return twitter_sentiment, reddit_sentiment
