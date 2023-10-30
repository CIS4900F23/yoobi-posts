import os
import json
from datetime import datetime
import requests

class Reddit:
    """Class that handles Reddit API"""

    def __init__(self):
        """Initialize"""
        self.headers = {'User-Agent': 'dataFetcher'}
        self.res = self.getOAuthToken()
        self.postList = []
        self.commentList = []
        self.query_result = None
        self.mongo_client = None


    def getOAuthToken(self):
        """Returns OAuth token from Reddit API"""
        auth = requests.auth.HTTPBasicAuth(os.environ.get("CLIENT_ID"), os.environ.get("SECRET_TOKEN"))
        data = {
            'grant_type': 'password',
            'username': os.environ.get("REDDIT_USERNAME"),
            'password': os.environ.get("REDDIT_PASSWORD")
        }
        #may have to write a function to refresh the token when it expires for asynchronous calls to reddit api when the program is hosted on kubernetes
        res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth, data=data, headers=self.headers, timeout=5)
        TOKEN = res.json()['access_token']
        self.headers = {**self.headers, **{'Authorization': f"bearer {TOKEN}"}}
        return res


    def getPostList(self):
        """Returns the post list"""
        return self.postList
    

    def emptyPostList(self):
        """Empty the post list"""
        self.postList.clear()


    def getNumPosts(self):
        """Returns total number of posts"""
        return len(self.postList)


    def postExists(self, post_id):
        """Returns true if post exists in postList"""
        for post in self.postList:
            if post.post_id == post_id:
                return True
        return False


    def getHotPosts(self):
        """Adds hot posts to postList"""
        redRes = requests.get('https://oauth.reddit.com/r/basicincome/hot',params={'limit': '100'},headers=self.headers,timeout=5)
        self.query_result = redRes.json()['data']['children']
        self.initPostList()


    def getNewPosts(self):
        """Adds new posts to postList"""	
        redRes = requests.get('https://oauth.reddit.com/r/basicincome/new',params={'limit': '100'},headers=self.headers,timeout=5)
        self.query_result = redRes.json()['data']['children']
        self.initPostList()


    def getTopPosts(self):
        """Adds top posts to list"""
        redRes = requests.get('https://oauth.reddit.com/r/basicincome/top',params={'limit': '100','t': 'all'},headers=self.headers,timeout=5)
        self.query_result = redRes.json()['data']['children']
        self.initPostList()


    def initPostList(self):
        """Adds posts to postList"""
        for child in self.query_result:
            title = child['data']['title']
            author = child['data']['author']
            date = datetime.fromtimestamp(child['data']['created_utc'])
            post_id = child['data']['id']

            #i think this should be done in the database file as well
            #database should check by id for repeating posts
            if not self.postExists(post_id):
                post = self.Post(
                        title,
                        author,
                        post_id,
                        date
                    )
                self.postList.append(post)


    def getComments(self):
        """Gets a list of comments for each post in postList"""
        if not self.postList:
            return
        
        for post in self.postList:
            url = 'https://oauth.reddit.com/r/basicincome/comments/' + str(post.getPostID())
            redRes = requests.get(url,params={'depth': '1'},headers=self.headers,timeout=5)
            self.query_result = redRes.json()[1]['data']['children']
            self.initCommentList()


    def emptyCommentList(self):
        """Empty the comment list"""
        self.commentList.clear()


    def getNumComments(self):
        """Return number of comments"""
        return len(self.commentList)
    
    
    def initCommentList(self):
        """Add Comments to the commentList"""
        for child in self.query_result:
            author = child['data']['author']
            body = child['data']['body']
            date = datetime.fromtimestamp(child['data']['created_utc'])
            post_id = self.splitPostID(child['data']['link_id'])
            comment_id = child['data']['id']
            comment = self.Comment(author,body,post_id,date)
            comment.setCommentID(comment_id)
            self.commentList.append(comment)


    def addCommentsToPost(self):
        """Adds comments to its respective post"""
        for post in self.postList:
            for comment in self.commentList:
                if comment.getPostID() == post.getPostID():
                    post.addComment(comment)


    def splitPostID(self,post_id):
        """Splits post_id field from comment to return only the post id"""
        return post_id.split('_',1)[1]
    

    def writeToJSON(self):
        """Returns a JSON object of redditList"""
        file_dict = {
            "date" : str(datetime.now())
        }
        posts = []

        for post in self.postList:
            posts.append(post.toDict())

        file_dict['data'] = posts
        obj = json.dumps(file_dict,indent=4)
        return obj


    def writeToFile(self, filename):
        """Writes redditList to a JSON file"""
        obj = self.writeToJSON()

        with open(filename, "w", encoding="UTF-8") as file:
            file.write(obj)
    

    class Post:
        """Class that represents a post"""
        def __init__(self, title, author, post_id, date):
            self.title = title
            self.author = author
            self.post_id = post_id
            self.date = date
            self.commentList = []


        def getPostID(self):
            """Returns post id"""
            return self.post_id
        

        def getNumComments(self):
            """Return total number of comments"""
            return len(self.commentList)
        

        def getTitle(self):
            """Returns the post title"""
            return self.title
        

        def getDate(self):
            """Returns the post date"""
            return self.date
        

        def addComment(self,comment):
            """Add comment to commentList"""
            self.commentList.append(comment)


        def commentsToDict(self):
            """Returns dictionary representation of commentList"""
            commentsDict = []
            for comment in self.commentList:
                commentsDict.append(comment.toDict())
            return commentsDict
        

        def toDict(self):
            """Returns dictionary representation of Post"""
            return {
                'content': str(self.title),
                'author_id': str(self.author),
                '_id': str(self.post_id),
                'created_at': str(self.date),
                'comments': self.commentsToDict()
            }
        

    class Comment:
        """Class that represents a a comment"""
        def __init__(self, author, body, post_id, date):
            self.author = author
            self.body = body
            self.post_id = self.parsePostID(post_id)
            self.date = date
            self.id = None
      

        def getComment(self):
            """Return comment"""
            return self.body
        

        def getPostID(self):
            """Return comment post id"""
            return self.post_id

        def setCommentID(self, comment_id):
            self.id = comment_id
        

        def parsePostID(self, post_id):
            """Returns post id without subscript t3"""
            return post_id
        

        def toDict(self):
            """Returns dictionary representation of Comment"""
            return{
                'author_id': str(self.author),
                '_id': str(self.id),
                'post_id': str(self.post_id),
                'created_at': str(self.date),
                'content': str(self.body)
            }
        