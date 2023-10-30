'''Integration tests for Twitter class'''
import os
import pytest
from src.lib.twitter import Twitter

@pytest.fixture
def emptyTwitter():
    '''Initialize an empty Twitter object.'''
    return Twitter()

@pytest.fixture
def twitter():
    '''Returns am initialized Twitter object.'''
    t = Twitter()
    t.readFromJSON("tweets.json")
    return t

def test_tweepyBearerToken(emptyTwitter):
    '''Test that the Tweepy client was given the correct bearer token.'''
    assert emptyTwitter.getTweepyBearerToken() == os.environ.get("BEARER_TOKEN")

def test_emptyList(twitter):
    twitter.emptyList()

    assert twitter.getNumTweets() == 0

def test_getNumTweets(twitter):
    assert twitter.getNumTweets() > 0

def test_toString(twitter):
    asString = twitter.toString()

    assert asString is not None