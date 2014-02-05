# from google.appengine.ext import ndb

# class CommentModel(ndb.Model):
#     movie_id = ndb.IntegerProperty()
#     author = ndb.StringProperty(indexed=False)
#     content = ndb.StringProperty(indexed=False)
#     date = ndb.DateTimeProperty(auto_now_add=True)
    
from google.appengine.ext import db

class CommentModel(db.Model):
    movie_id = db.IntegerProperty()
    author = db.StringProperty(indexed=False)
    content = db.StringProperty(indexed=False)
    date = db.DateTimeProperty(auto_now_add=True)
    emotion_review_id = db.IntegerProperty()