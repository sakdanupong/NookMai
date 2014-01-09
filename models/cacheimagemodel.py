from google.appengine.ext import db

class CacheImageModel(db.Model):
    id = db.IntegerProperty()
    image = db.BlobProperty(default=None)