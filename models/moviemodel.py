from google.appengine.ext import db
from timemodel import *
from movienamemodel import *
from moviedetailmodel import *
from movietrailermodel import *

class MovieModel(db.Model):
    id = db.IntegerProperty()
    ribbon_type = db.IntegerProperty()
    advande_time = db.ReferenceProperty(TimeModel)
    name = db.ReferenceProperty(MovieNameModel)
    detail = db.ReferenceProperty(MovieDetailModel)
    trailer = db.ReferenceProperty(MovieTrailerModel)
    types = db.StringListProperty()
    cinemas = db.ListProperty(long)