from google.appengine.ext import db

class UserModel(db.Model):
	username = db.StringProperty(default=None)
	create_date = db.DateTimeProperty(auto_now_add=True)
	password = db.TextProperty()
	user_id = db.IntegerProperty(default=0)
	email = db.StringProperty()
	session_token = db.TextProperty()