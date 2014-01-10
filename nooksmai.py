import webapp2
import cgi
import json
import urllib
import os,sys
import jinja2

sys.path.append(os.path.abspath('models'))
from google.appengine.api import users
from google.appengine.api import urlfetch
from moviemodel import *
from cacheimagemodel import *
from commentmodel import *
from trailercachemodel import *


# MAIN_PAGE_HTML = """\
# <html>
#   <body>
#     <form action="/sign" method="post">
#       <div><textarea name="content" rows="3" cols="60"></textarea></div>
#        <div><input type="submit" value="Sign Guestbook"></div>
#     </form>
#     
#     <form action="/nextview?%s" method="post">
#        <div><input type="submit" value="next view"></div>
#     </form>
# 
#   </body>
# </html>
# """


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):
        movie_query = MovieModel.all().order('-release_time_timestamp').fetch(limit=20)
        template_values = {
             'movie_list': movie_query,
        }
        template = JINJA_ENVIRONMENT.get_template('movielist.html')
        self.response.write(template.render(template_values))

class RefreshData(webapp2.RequestHandler):
    def get(self):
        url = 'http://onlinepayment.majorcineplex.com/api/1.0/now_showing?w=320&h=480&x=2&o=0&pf=iOS&mid=iPhone%20Simulator&indent=0&deflate=1&appv=2.6&rev=2'
        result = urlfetch.fetch(url)
        mJson = json.loads(result.content)
        for m in mJson['movies']:
            movie_id = str(m['id'])
            e = MovieModel.get_or_insert(key_name=movie_id)
            e.id = m['id']
            e.ribbon_type = m['ribbon_type']
            if 'avd_time' in m:
                movie_time = m['avd_time']
                e.adv_time_timestamp = movie_time['timestamp']
                e.adv_time_text = movie_time['text']
            movie_name = m['name']
            e.name_en = movie_name['en']
            e.name_th = movie_name['th']
            movie_detail = m['detail']
            e.duration = movie_detail['duration']
            e.rate = movie_detail['rate']
            e.rateWarning = movie_detail['rateWarning']
            e.image = movie_detail['image']
            movie_release_date = movie_detail['releasedate']
            e.release_time_timestamp = movie_release_date['timestamp']
            e.release_time_text = movie_release_date['text']
            movie_trailer = movie_detail['trailer']
            e.yt_id = movie_trailer['yt_id']
            e.rtsp = movie_trailer['rtsp']
            e.thumbnail = movie_trailer['thumbnail']
            e.types = m['types']
            e.cinemas = m['cinemas']
            e.put()
            
            
            url = 'http://onlinepayment.majorcineplex.com/api/1.0/movie_detail?w=320&h=480&x=2&o=0&pf=iOS&mid=iPhone%20Simulator&indent=0&deflate=1&appv=2.6&rev=2&movie_id='+movie_id
            result = urlfetch.fetch(url)
            mJson = json.loads(result.content)
            
            movie_detail = mJson['detail']
            e.detail_duration = movie_detail['duration']
            e.detail_rate = movie_detail['rate']
            e.detail_rateWarning = movie_detail['rateWarning']
            
            releasedate = movie_detail['releasedate']
            e.detail_timestamp = releasedate['timestamp']
            e.detail_text = releasedate['text']

            synopsis = movie_detail['synopsis']
            e.detail_synopsis_en = synopsis['en']
            e.detail_synopsis_th = synopsis['th']

            e.detail_image = movie_detail['image']

            trailer = movie_detail['trailer']
            e.detail_yt_id = trailer['yt_id']
            e.detail_rtsp = trailer['rtsp']
            e.detail_thumbnail = trailer['thumbnail']

            genre = movie_detail['genre']
            e.detail_genre_en = genre['en']
            e.detail_genre_th = genre['th']
            
            director = movie_detail['director']
            e.detail_director_en = director['en']
            e.detail_director_th = director['th']
            
            cast = movie_detail['cast']
            e.detail_cast_en = cast['en']
            e.detail_cast_th = cast['th']
            e.put()



class ImageCache(webapp2.RequestHandler):
    def get(self):
        movie_id = self.request.get('movie_id')
        image_query = CacheImageModel.get_or_insert(key_name=movie_id)
        if image_query.image is None:
            movie_model = MovieModel.get_by_key_name(movie_id)
            image_query.id = movie_model.id
            image_query.image = db.Blob(urlfetch.Fetch(movie_model.image).content)
            image_query.put()
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(image_query.image)

YOUTUBE_EMBED = """<iframe width="560" height="315" src="//www.youtube.com/embed/9aBiHYT_8UI" frameborder="0" allowfullscreen></iframe>"""
class TrailerPlayer(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(YOUTUBE_EMBED)
#         url = 'http://210.1.60.208:1935/vod/_definst_/mp4'
#         trailer_query = TrailerCacheModel.get_or_insert()
#         vdo = db.Blob(urlfetch.Fetch(url).content)
#         self.response.headers['Content-Type'] = 'video/mp4'
#         self.response.out.write(vdo)




class NookMai(webapp2.RequestHandler):

    def post(self):
        self.response.write('<html><body>You wrotesdsdsd:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

class NookMaiDetailMovie(webapp2.RequestHandler):

    def get(self):

        movie_id = self.request.get('movie_id')
        movie_data = MovieModel.get_or_insert(key_name=movie_id)
        template_values = {
            'movie_data': movie_data,
        }
        template = JINJA_ENVIRONMENT.get_template('movie_detail.html')
        self.response.write(template.render(template_values))



# def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
#     """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
#     return ndb.Key('Guestbook', guestbook_name)
# 
# class Greeting(ndb.Model):
#     """Models an individual Guestbook entry with author, content, and date."""
#     author = ndb.UserProperty()
#     content = ndb.StringProperty(indexed=False)
#     date = ndb.DateTimeProperty(auto_now_add=True)
    

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key('CommentModel', guestbook_name)

class CommentMovie(webapp2.RequestHandler):
    def post(self):
        movie_id = self.request.get('movie_id')
        
        self.response.write(movie_id)
        self.response.write(cgi.escape(self.request.get('content')))


#         guestbook_name = self.request.get('guestbook_name',
#                                           DEFAULT_GUESTBOOK_NAME)
#         comment = CommentModel(parent=guestbook_key(guestbook_name))
#         
#          if users.get_current_user():
#              comment.author = users.get_current_user()
# 
#         comment.content = self.request.get('content')
#         comment.id_movie = self.request.get(movie_id)
#         
#         #save comment
#         comment.put()

        
#         guestbook_name = self.request.get('guestbook_name',
#                                           DEFAULT_GUESTBOOK_NAME)
#         greeting = CommentModel(parent=guestbook_key(guestbook_name))
#         
#         if users.get_current_user():
#             greeting.author = users.get_current_user()
# 
#         greeting.content = self.request.get('content')
#         greeting.put()
        
        
        
        
        
#         comment_query = CommentModel.get_or_insert(key_name=movie_id)
        #redirect view
#         self.redirect('/nextview?movie_id='+movie_id)

#     def post(self):
#         movie_id = self.request.get('movie_id')
#         comment_query = CommentModel.get_or_insert(key_name=movie_id)
#         if comment_query.content is None:
#             movie_model = MovieModel.get_by_key_name(movie_id)
#             comment_query.id = movie_model.id
#             comment_query.author = db.Blob(urlfetch.Fetch(comment_query.author).content)
#             comment_query.content = cgi.escape(self.request.get('content'))
#             comment_query.date = db.Blob(urlfetch.Fetch(comment_query.date).content)
#             comment_query.put()
#             self.response.out.write(comment_query.content)
            

#         commentModel = CommentModel.query(
#         ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
#         greetings = greetings_query.fetch(10)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', NookMai),
    ('/nextview', NookMaiDetailMovie),
    ('/refresh_data', RefreshData),
    ('/image', ImageCache),
    ('/comment', CommentMovie),
    ('/trailer', TrailerPlayer),
], debug=True)
