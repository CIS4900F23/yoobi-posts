from src.db.connect import DBConnect

dbc = DBConnect()
#dbc.dropCollection("UBI", "reddit_posts")
#print(dbc.getCollectionNames("UBI"))
#dbc.writeFileToCollection("UBI", "tweets", "tweets.json")
dbc.writeFileToCollection("UBI", "reddit_posts", "reddit_posts.json")
