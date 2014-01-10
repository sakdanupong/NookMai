from google.appengine.ext import db

class TrailerCacheModel(db.Model):
    id = db.IntegerProperty()
    trailer_vdo = db.BlobProperty(default=None)