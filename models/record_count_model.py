from google.appengine.ext import db

class RecordCountModel(db.Model):
	movie_count = db.IntegerProperty(default=0)
	comment_count = db.IntegerProperty(default=0)