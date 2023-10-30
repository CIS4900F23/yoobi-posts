import pymongo
import pytest
from src.db.connect import DBConnect


@pytest.fixture
def dbc():
    dbc = DBConnect()
    try:
        dbc.writeFileToCollection("test_UBI", "test_tweets", "test_tweets.json")
    except pymongo.errors.BulkWriteError as e:
        print(e)
    return dbc

def test_getDatabaseNames(dbc):
    assert dbc.getDatabaseNames() == ["test_UBI"]


def test_getCollectionNames(dbc):
    assert dbc.getCollectionNames("test_UBI") == ["test_tweets"]

def test_getCollectionSize(dbc):
    assert dbc.getCollectionSize("test_UBI", "test_tweets") == 3393

def test_getRandomDocument(dbc):
    doc = dbc.getRandomDocument("test_UBI", "test_tweets")

    assert doc is not None

def test_getDocumentById(dbc):
    doc = dbc.getDocumentById("test_UBI", "test_tweets", "1623133583446806529")

    assert doc is not None