from google.appengine.ext import db

class SessionModel(db.Model):
	user_id = db.IntegerProperty(default=0)
	session_token = db.TextProperty()