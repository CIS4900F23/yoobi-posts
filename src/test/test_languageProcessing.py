"""Tests for languageProcessing.py"""
import unittest
import nltk
from src.lib.languageProcessing import LanguageProcessing

try:
    nltk.download('vader_lexicon')
except (EOFError, FileExistsError)  as e:
    print(e)

def test_languageProcessing():
    """Initialize a languageProcessing object"""
    assert LanguageProcessing()

def test_getSentiment():
    """Test the get_sentiment function against an example string with a known output"""
    test_str = "I really love NVIDIA"
    expected_results = [0.0, 0.308, 0.692, 0.6697]
    lp = LanguageProcessing()
    sentiment = lp.getSentiment(test_str)
    results = list(sentiment.values())
    unittest.TestCase().assertListEqual(results, expected_results)

def test_sentimentToDataFrame():
    """Test the sentimentToDataFrame function against an example string with a known output"""
    test_str = "I really love NVIDIA"
    expected_results = [0.0, 0.308, 0.692, 0.6697]
    lp = LanguageProcessing()
    sentiment = lp.getSentiment(test_str)
    df = lp.sentimentToDataFrame(sentiment)
    # Use unittest module to compare the results
    unittest.TestCase().assertListEqual(list(df['Sentiment Score']), expected_results)