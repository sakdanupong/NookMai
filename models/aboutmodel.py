# from google.appengine.ext import ndb

# class CommentModel(ndb.Model):
#     movie_id = ndb.IntegerProperty()
#     author = ndb.StringProperty(indexed=False)
#     content = ndb.StringProperty(indexed=False)
#     date = ndb.DateTimeProperty(auto_now_add=True)
    
from google.appengine.ext import db

class AboutModel(db.Model):
    name = db.StringProperty(indexed=False)
    description = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    email = db.TextProperty()
