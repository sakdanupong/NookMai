import webapp2
import cgi
import json
import os,sys
import jinja2

sys.path.append(os.path.abspath('models'))
from google.appengine.api import users
from google.appengine.api import urlfetch
from moviemodel import *
from cacheimagemodel import *

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/sign" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
       <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    
    <form action="/nextview?data_json={{ data_json }}" method="post">
       <div><input type="submit" value="next view"></div>
    </form>

  </body>
</html>
"""

MAIN_PAGE2_HTML = """\
<html>
  <body>
    <div>name</div>
    <div>date</div>
    <div>image</div>
  </body>
</html>
"""

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

class NookMai(webapp2.RequestHandler):

    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

class NookMaiDetailMovie(webapp2.RequestHandler):

    def post(self):
#         self.response.write(MAIN_PAGE2_HTML)
        self.response.write('<html><body>DetailMovie<pre>')
#         self.response.out.write(mJson)
#         self.response.write(cgi.escape(self.request.get('content')))
        movie_id = self.request.get('movie_id')
        self.response.write('</pre></body></html>')


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', NookMai),
    ('/nextview', NookMaiDetailMovie),
    ('/refresh_data', RefreshData),
    ('/image', ImageCache),
], debug=True)