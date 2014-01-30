from google.appengine.ext import db

class ComingSoonModel(db.Model):
    comming_month_th = db.StringProperty()
    comming_month_en = db.StringProperty()
    create_date = db.DateTimeProperty(auto_now_add=True)