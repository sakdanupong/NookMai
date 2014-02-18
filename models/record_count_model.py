from google.appengine.ext import db

class RecordCountModel(db.Model):
	nowshowing_count = db.IntegerProperty(default=0)
	comingsoon_count = db.IntegerProperty(default=0)
	movie_count = db.IntegerProperty(default=0)
	comment_count = db.IntegerProperty(default=0)
	user_count = db.IntegerProperty(default=0)