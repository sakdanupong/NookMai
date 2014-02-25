from google.appengine.ext import db

class RateMovieModel(db.Model):
    movie_id = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    rate_score = db.IntegerProperty()
    user_id = db.IntegerProperty()
    username = db.StringProperty()