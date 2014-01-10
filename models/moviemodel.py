from google.appengine.ext import db

class MovieModel(db.Model):
    id = db.IntegerProperty()
    ribbon_type = db.IntegerProperty()
    adv_time_timestamp = db.IntegerProperty()
    adv_time_text = db.StringProperty()
    name_en = db.StringProperty()
    name_th = db.StringProperty()
    duration = db.IntegerProperty()
    rate = db.StringProperty()
    rateWarning = db.BooleanProperty()
    image = db.StringProperty()
    release_time_timestamp = db.IntegerProperty()
    release_time_text = db.StringProperty()
    yt_id = db.StringProperty()
    rtsp = db.StringProperty()
    thumbnail = db.StringProperty()
    types = db.StringListProperty()
    cinemas = db.ListProperty(int)
    youtube_url = db.StringProperty()
    
    detail_duration = db.IntegerProperty()
    detail_rate = db.StringProperty()
    detail_rateWarning= db.BooleanProperty()        
    detail_timestamp = db.IntegerProperty()
    detail_text = db.StringProperty()
    detail_synopsis_en = db.TextProperty()
    detail_synopsis_th = db.TextProperty()
    detail_image = db.StringProperty()
    detail_yt_id = db.StringProperty()
    detail_rtsp = db.StringProperty()
    detail_thumbnail = db.StringProperty()
    detail_genre_en = db.StringProperty()
    detail_genre_th = db.StringProperty()      
    detail_director_en = db.StringProperty()
    detail_director_th = db.StringProperty()      
    detail_cast_en = db.StringProperty()
    detail_cast_th = db.StringProperty()
    
    
    
    
# #We set a parent key on the 'Greetings' to ensure that they are all in the same
# # entity group. Queries across the single entity group will be consistent.
# # However, the write rate should be limited to ~1/second.
# 
# def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
#     """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
#     return db.Key('Guestbook', guestbook_name)
# 
# # The following defines a data model for a greeting
# class Greeting(db.Model):
#     """Models an individual Guestbook entry with author, content, and date."""
#     author = db.UserProperty()
#     content = db.StringProperty(indexed=False)
#     date = db.DateTimeProperty(auto_now_add=True)