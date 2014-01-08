from google.appengine.ext import ndb
from timemodel import *

class MovieDetailModel(db.Model):
    duration = db.IntegerProperty()
    rate = db.StringProperty(multiline=True)
    rateWarning = db.BooleanProperty()
    image = db.StringProperty(multiline=True)
    release_date = db.ReferenceProperty(TimeModel)