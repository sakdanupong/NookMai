from google.appengine.ext import db
# from google.appengine.ext import ndb

class MovieModel(db.Model):
    original_id = db.IntegerProperty(default=0)
    id = db.IntegerProperty()
    name_en = db.StringProperty()
    name_th = db.StringProperty()
    duration = db.IntegerProperty()
    rate = db.StringProperty()
    image = db.StringProperty()
    release_time_timestamp = db.IntegerProperty()
    thumbnail = db.StringProperty()
    types = db.StringListProperty()
    youtube_url = db.StringProperty()
    comment_count = db.IntegerProperty(default=0)
    create_ = db.DateTimeProperty(auto_now_add=True)
    is_coming_soon = db.IntegerProperty(default=0)
    coming_month_th = db.StringProperty()
    coming_month_en = db.StringProperty()
    search_tag = db.StringListProperty()

    detail_synopsis_en = db.TextProperty()
    detail_synopsis_th = db.TextProperty()
    detail_image = db.StringProperty()
    detail_thumbnail = db.StringProperty()
    detail_genre_en = db.StringProperty()
    detail_genre_th = db.StringProperty()      
    detail_director_en = db.StringProperty()
    detail_director_th = db.StringProperty()      
    detail_cast_en = db.StringProperty()
    detail_cast_th = db.StringProperty()

    avatar_1_count = db.IntegerProperty(default=0)
    avatar_2_count = db.IntegerProperty(default=0)
    avatar_3_count = db.IntegerProperty(default=0)
    avatar_4_count = db.IntegerProperty(default=0)
    avatar_5_count = db.IntegerProperty(default=0)
    avatar_6_count = db.IntegerProperty(default=0)
    avatar_7_count = db.IntegerProperty(default=0)
    avatar_8_count = db.IntegerProperty(default=0)
    avatar_9_count = db.IntegerProperty(default=0)
    avatar_10_count = db.IntegerProperty(default=0)
    avatar_11_count = db.IntegerProperty(default=0)
    avatar_12_count = db.IntegerProperty(default=0)
    avatar_13_count = db.IntegerProperty(default=0)
    avatar_14_count = db.IntegerProperty(default=0)

    rate_count = db.IntegerProperty(default=10)
    vote_count = db.IntegerProperty(default=0)
    vote_comment_count = db.IntegerProperty(default=0)
    # vote_result = db.ComputedProperty(lambda self: ((self.rate_count * self.vote_comment_count) + self.vote_count))
    vote_result = db.IntegerProperty(default=0)