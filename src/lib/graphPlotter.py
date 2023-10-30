"""Class that uses Plotly to generate graph data to be passed to PlotlyJS as a JSON object."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class GraphPlotter:
    """Class that uses Plotly to generate the graphs that will be used in the app"""
    def plotPostSentiment(self, df: pd.DataFrame, title:str=None, x_label:str=None, y_label:str=None):
        """Generates a bar graph of the sentiment analysis data frame from a post"""
        fig = px.bar(
            data_frame=df, 
            orientation='h',
            color='Sentiment',
            title='Sentiment Analysis of Post',
            x='Sentiment Score',
            y='Sentiment',
            range_x=[0,1],
        )

        if x_label is not None:
            fig.update_layout(
                xaxis_title=x_label,
            )
        
        if y_label is not None:
            fig.update_layout(
                yaxis_title=y_label,
            )

        if title is not None:
            fig.update_layout(
                title=title,
            )

        result = fig.to_json()
        return result
    
    def plotDatabaseSentiment(self, twitter_df: pd.DataFrame, reddit_df: pd.DataFrame):
        
        fig = go.Figure(data = [

            go.Bar(name='Twitter', x=twitter_df['Sentiment Score'], y=twitter_df['Sentiment'], orientation='h'),
            go.Bar(name='Reddit', x=reddit_df['Sentiment Score'], y=reddit_df['Sentiment'], orientation='h')
            ]
        )

        fig.update_layout(
            title='Sentiment Analysis of All Posts',
            xaxis_title="Sentiment Score",
            yaxis_title="Sentiment",
            barmode='group',
        )

        result = fig.to_json()
        return result