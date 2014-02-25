from google.appengine.ext import db
from commentmodel import *

class UserVoteCommentModel(db.Model):
    comment = db.ReferenceProperty(commentmodel,
                                   collection_name='user_comments')
    create_date = db.DateTimeProperty(auto_now_add=True)
    user_id = db.IntegerProperty(default=0)
    vote_state = db.IntegerProperty(default=0)