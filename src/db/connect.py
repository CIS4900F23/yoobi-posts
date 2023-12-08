import json
import re
from typing import List
from nltk.corpus import stopwords
from pymongo import MongoClient
from profanity_filter import ProfanityFilter
from pymongo.errors import ConnectionFailure

# For Docker Compose
 # mongo_uri = "mongodb://root:example@yoobi-db:27017/"

# For K8s
mongo_uri = "mongodb://yoobi-db.production.svc.cluster.local:27017"


class DBConnect:
    DB: str = "UBI"
    TWITTER: str = "tweets"
    REDDIT: str = "reddit_posts"

    def __init__(self) -> None:
        try:
            self.client = MongoClient(mongo_uri)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command("ismaster")
            print("MongoDB connection successful.")
        except ConnectionFailure:
            print("MongoDB connection failed.")

    def getDatabaseNames(self) -> List[str]:
        return self.client.list_database_names()

    def getCollectionNames(self, database: str) -> List[str]:
        return self.client[database].list_collection_names()

    def getCollectionSize(self, database: str, collection: str) -> int:
        """Returns size of the collection"""
        db = self.client[database]
        cl = db[collection]

        return cl.estimated_document_count()

    def getRandomDocument(self, database: str, collection: str) -> dict:
        """Returns a random document from the collection"""
        db = self.client[database]
        cl = db[collection]
        doc = list(cl.aggregate([{"$sample": {"size": 1}}]))

        # Check if the random sampler failed. Perhaps the collection does not exist, for example.
        if len(doc) == 0:
            return {
                "_id": "abc123",
                "created_at": "01-01-1900",
                "content": "The random sampler failed!",
            }

        return doc[0]

    def writeFileToCollection(
        self, database: str, collection: str, filename: str
    ) -> None:
        with open(filename, "r", encoding="UTF-8") as file:
            obj = json.load(file)
            data = obj["data"]
            db = self.client[database]
            cl = db[collection]
            cl.insert_many(data, ordered=False)

    def writeJSONToCollection(
        self, database: str, collection: str, jsonObject: object
    ) -> None:
        # print(jsonObject)
        obj = json.loads(jsonObject)
        data = obj["data"]
        # print(data)
        db = self.client[database]
        cl = db[collection]
        cl.insert_many(data, ordered=False)

    def writeCollectionToFile(
        self, database: str, collection: str, filename: str
    ) -> None:
        db = self.client[database]
        cl = db[collection]
        docs = list(cl.find({}))
        file = {}
        file["data"] = docs
        obj = json.dumps(file)

        with open(filename, "w", encoding="UTF-8") as file:
            file.write(obj)

    def dropCollection(self, database: str, collection: str) -> None:
        db = self.client[database]
        cl = db[collection]
        cl.drop()

    def getCollection(self, database: str, collection: str) -> str:
        db = self.client[database]
        cl = db[collection]
        docs = list(cl.find({}))
        obj = {}
        obj["data"] = docs

        return obj

    def censorCollection(self, database: str, collection: str) -> None:
        pf = ProfanityFilter()
        db = self.client[database]
        col = db[collection]

        for document in col.find({}):
            col.update_one(
                document, {"$set": {"content": pf.censor(document["content"])}}
            )

    def getDocumentById(self, database: str, collection: str, doc_id: str) -> dict:
        """Returns a document from the collection by querying for an id"""
        db = self.client[database]
        cl = db[collection]
        result = cl.find_one({"_id": doc_id})

        return result

    def cleanCollection(self, database: str, collection: str) -> None:
        db = self.client[database]
        cl = db[collection]

        for document in cl.find({}):
            result = document["content"]

            # Remove mentions
            result = re.sub("@([a-zA-Z0-9_]{1,50})", "", result)
            # Remove hashtags
            result = re.sub("#([a-zA-Z0-9_]{1,50})", "", result)
            # Remove hyperlinks
            result = re.sub(r"http\S+", "", result)
            # Remove newlines
            result = re.sub("\n", "", result)

            # Remove stop words
            tokens = [
                word
                for word in result.split()
                if word.lower() not in stopwords.words("english")
            ]
            result = " ".join(tokens)

            cl.update_one(document, {"$set": {"content": result}})

    def cleanString(self, content: str) -> str:
        # Copy parameter.
        result = content
        # Remove mentions
        result = re.sub("@([a-zA-Z0-9_]{1,50})", "", result)
        # Remove hashtags
        result = re.sub("#([a-zA-Z0-9_]{1,50})", "", result)
        # Remove hyperlinks
        result = re.sub(r"http\S+", "", result)
        # Remove newlines
        result = re.sub("\n", "", result)
        # Remove stop words
        tokens = [
            word
            for word in result.split()
            if word.lower() not in stopwords.words("english")
        ]
        # Concatenate tokens.
        result = " ".join(tokens)

        return result

    def closeConnection(self) -> None:
        self.client.close()
