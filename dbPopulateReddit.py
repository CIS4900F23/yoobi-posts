import pymongo
# from src.lib.reddit import Reddit
from src.db.connect import DBConnect

#initialize
# r = Reddit()
dbc = DBConnect()

#fetch new data
# r.getNewPosts()
# r.getComments()
# r.addCommentsToPost()

#get jsonObject of new data
# jsonObj = r.writeToJSON()

#add to database collection
try:
    # dbc.writeJSONToCollection("UBI","reddit_posts",jsonObj)
    dbc.writeFileToCollection(dbc.DB, dbc.REDDIT, "reddit_posts.json")
except pymongo.errors.BulkWriteError as e:
    print("BulkWriteError occured, likely due to duplicate posts. Non duplicate posts should have been added.")
