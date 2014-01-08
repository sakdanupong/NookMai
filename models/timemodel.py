from google.appengine.ext import db

class TimeModel(db.Model):
     text = db.StringProperty(multiline=False)
     timestamp = db.IntegerProperty()