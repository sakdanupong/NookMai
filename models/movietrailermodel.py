from google.appengine.ext import db

class MovieTrailerModel(db.Model):
    yt_id = db.StringProperty(multiline=False)
    rtsp = db.StringProperty(multiline=True)
    thumbnail = db.StringProperty(multiline=True)