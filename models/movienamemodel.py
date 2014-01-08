from google.appengine.ext import db

class MovieNameModel(db.Model):
     en = db.StringProperty(multiline=True)
     th = db.StringProperty(multiline=True)