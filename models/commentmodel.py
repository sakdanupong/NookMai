from google.appengine.ext import db

class CommentModel(db.Model):
    id_movie = db.IntegerProperty()
    id = db.IntegerProperty()
    author = db.UserProperty()
    content = db.StringProperty(indexed=False)
    date = db.DateTimeProperty(auto_now_add=True)
    
