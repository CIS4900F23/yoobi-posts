"""Script to refresh database sentiment plot when the database is updated"""
from src.lib.languageProcessing import LanguageProcessing
from src.lib.graphPlotter import GraphPlotter
from src.db.connect import DBConnect

lp = LanguageProcessing()
gp = GraphPlotter()
dbc = DBConnect()

twitter_sentiment, reddit_sentiment = lp.getDatabaseSentiment(dbc)

twitter_df = lp.sentimentToDataFrame(twitter_sentiment)
reddit_df = lp.sentimentToDataFrame(reddit_sentiment)

db_plot = gp.plotDatabaseSentiment(twitter_df, reddit_df)

with open("db_sentiment.json", "w", encoding='utf-8') as file:
    file.write(db_plot)
    file.close()