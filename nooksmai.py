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

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/sign" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
       <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    
    <form action="/nextview?%s" method="post">
       <div><input type="submit" value="next view"></div>
    </form>

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



class NookMai(webapp2.RequestHandler):

    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
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




application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', NookMai),
    ('/nextview', NookMaiDetailMovie),
    ('/refresh_data', RefreshData),    
], debug=True)