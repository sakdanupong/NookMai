from google.appengine.ext import db
from moviemodel import *
class UserRateModel(db.Model):
    movie_model = db.ReferenceProperty(MovieModel, collection_name='user_rates')
    username = db.StringProperty(default=None)
    create_date = db.DateTimeProperty(auto_now_add=True)
    user_id = db.IntegerProperty(default=0)
    rate_state = db.IntegerProperty(default=0)