from google.appengine.ext import db
from moviemodel import *
class UserVoteModel(db.Model):
    movie_model = db.ReferenceProperty(MovieModel, collection_name='user_votes')
    username = db.StringProperty(default=None)
    create_date = db.DateTimeProperty(auto_now_add=True)
    user_id = db.IntegerProperty(default=0)
    vote_state = db.IntegerProperty(default=0)