'''Tests for reddit.py'''
import pytest
from src.lib.reddit import Reddit

@pytest.fixture()
def reddit():
    return Reddit()

def test_OAuthToken(reddit):
    res = reddit.getOAuthToken()
    assert 200 == res.status_code

def test_emptyPostList(reddit):
    reddit.getHotPosts()
    reddit.emptyPostList()
    post_list = reddit.getPostList()
    assert 0 == len(post_list)

def test_getNumPosts(reddit):
    """Test reddit object returns 100 posts in the list after getting hot posts"""
    reddit.getHotPosts()
    assert 100 == reddit.getNumPosts()

def test_HotPosts(reddit):
    reddit.getHotPosts()
    assert 100 == reddit.getNumPosts()

def test_NewPosts(reddit):
    reddit.getNewPosts()
    assert 100 == reddit.getNumPosts()


def test_TopPosts(reddit):
    reddit.getTopPosts()
    assert 100 == reddit.getNumPosts()

# This test takes a very long time.
def test_getComments(reddit):
    """Test number of comments in the reddit object is less than or equal to the number of comments for each post in the postList"""
    reddit.getHotPosts()
    hotPosts = reddit.getPostList()
    reddit.getComments()
    reddit.addCommentsToPost()
    commentCount = 0
    for post in hotPosts:
        commentCount = commentCount + post.getNumComments()

    totalComments = reddit.getNumComments()
    assert commentCount >= totalComments
