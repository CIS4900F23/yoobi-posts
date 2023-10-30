"""API route for handling anything that graph plotting using Plotly"""
import gzip
import nltk
from flask import make_response
from flask_restx import Namespace, Resource
from src.lib.languageProcessing import LanguageProcessing
from src.lib.graphPlotter import GraphPlotter
from src.db.connect import DBConnect

try:
    nltk.download('vader_lexicon')
except (EOFError, FileExistsError)  as e:
    print(e)

try:
    nltk.download('stopwords')
except (EOFError, FileExistsError) as e:
    print(e)

api = Namespace('plot', description='Graph Plotting Related Operations')
lp = LanguageProcessing()
gp = GraphPlotter()
dbc = DBConnect()

def compressPlot(plot):
    """
    Compress a plot into response using gzip
    """
    zipped_data = gzip.compress(plot.encode('utf-8'), 5)
    response = make_response(zipped_data)
    response.headers['Content-Encoding'] = 'gzip'

    return response

class TwitterSentiment(Resource):
    """
    Creates a plot of the sentiment of a given tweets
    """
    def get(self, post_id):
        doc = dbc.getDocumentById("UBI", dbc.TWITTER, post_id)
        text = dbc.cleanString(str(doc["content"]))
        sentiment = lp.getSentiment(text)
        df = lp.sentimentToDataFrame(sentiment)
        plot = gp.plotPostSentiment(df)

        response = compressPlot(plot)

        return response
    
class RedditSentiment(Resource):
    """
    Creates a plot of the sentiment of a given tweets
    """
    def get(self, post_id):
        doc = dbc.getDocumentById("UBI", dbc.REDDIT, post_id)
        text = dbc.cleanString(str(doc["content"]))
        sentiment = lp.getSentiment(text)
        df = lp.sentimentToDataFrame(sentiment)
        plot = gp.plotPostSentiment(df)

        response = compressPlot(plot)

        return response

class DataBaseSentiment(Resource):
    """
    Creates a twin pair bar graph of the sentiment of all posts in the database
    """
    def get(self):
        with open('db_sentiment.json', 'r', encoding='utf-8') as file:
            plot = file.read()
            file.close()
            response = compressPlot(plot)
            return response

api.add_resource(TwitterSentiment, "/sentiment/tweets/<string:post_id>")
api.add_resource(RedditSentiment, "/sentiment/reddit/<string:post_id>")
api.add_resource(DataBaseSentiment, "/sentiment/all")
