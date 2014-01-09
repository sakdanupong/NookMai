import webapp2
import cgi
import json
import urllib
import os,sys

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

MAIN_PAGE2_HTML = """\
<html>
  <body>
    <div>name %s</div>
    <div>date %s</div>
    <div>image %s</div>
  </body>
</html>
"""

# <<<<<<< HEAD
# DEFAULT_MOVIE_NAME = 'no content'
# 
# 
# class MainPage(webapp2.RequestHandler):
# 
#     def get(self):
# #         self.response.write(MAIN_PAGE_HTML)
#         url = 'http://onlinepayment.majorcineplex.com/api/1.0/now_showing?w=320&h=480&x=2&o=0&pf=iOS&mid=iPhone%20Simulator&indent=0&deflate=1&appv=2.6&rev=2'
#         result = urlfetch.fetch(url)
#         mJson = json.loads(result.content)
# #         self.response.out.write(mJson['success'])
# 
#         sign_query_params = urllib.urlencode({'mJson': mJson})
# 
#         self.response.write(MAIN_PAGE_HTML % (sign_query_params))
# #         self.response.out.write(mJson)
#         self.response.out.write(mJson['md5'])
# =======






class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)

class RefreshData(webapp2.RequestHandler):
    def get(self):
        url = 'http://onlinepayment.majorcineplex.com/api/1.0/now_showing?w=320&h=480&x=2&o=0&pf=iOS&mid=iPhone%20Simulator&indent=0&deflate=1&appv=2.6&rev=2'
        result = urlfetch.fetch(url)
        mJson = json.loads(result.content)
        for m in mJson['movies'] :
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

class NookMai(webapp2.RequestHandler):

    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

class NookMaiDetailMovie(webapp2.RequestHandler):

    def post(self):


        self.response.write('<html><body>DetailMovie<pre>')
        q = MovieModel.all()
        //self.request.get('name_en')
        //self.response.write(name_en)
        self.response.write('</pre></body></html>')

        
#         self.response.write(MAIN_PAGE2_HTML)
#         self.response.write('<html><body>DetailMovie<pre>')
#         
#         mJson = self.request.get('mJson', DEFAULT_MOVIE_NAME)
#         self.response.out.write(mJson['md5'])
#         json_data = json.dumps(mJson)
#         self.response.out.write(json_data)
        
#         self.response.write('<html><body>DetailMovie<pre>')
#         
#         mJson = self.request.get('mJson', DEFAULT_MOVIE_NAME)
#         json_data = json.dumps(mJson)
#         self.response.out.write(json_data)
        
        # q = MovieModel.all()
#         self.response.out.write(q)
#         
        
        # query = db.MovieModel.query()
#         self.response.write('%s' % (query))



#         scoreName = 'name_th'
#         if self.request.get('match') :
#             scoreName = 'score_match'
#         q.order('-'+scoreName)
#         result = []
#         for r in q.fetch(limit=100) :
#             result.append(get_facebook_dict(r))
#         dict = {"data":result}
#         out_json(self, dict)
        
# !!        
#         json_data = response.read()
#         print '\n '
#         response_dict = json.loads(json_data)
#         print response_dict.get("response_code",{})
# !!   
        
#         self.response.out.write(json_data['movies'])

#         self.response.write(cgi.escape(self.request.get(mJson['movies'])))
        
#         self.response.write('</pre></body></html>')


#         self.response.write(MAIN_PAGE2_HTML)
#         mJson = self.request.get('mJson', )
#         self.response.out.write(mJson)



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', NookMai),
    ('/nextview', NookMaiDetailMovie),
    ('/refresh_data', RefreshData),    
], debug=True)