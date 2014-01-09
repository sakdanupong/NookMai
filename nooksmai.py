from google.appengine.api import users
from google.appengine.api import urlfetch


import webapp2
import cgi
import json
import urllib

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

DEFAULT_MOVIE_NAME = 'no content'


class MainPage(webapp2.RequestHandler):

    def get(self):
#         self.response.write(MAIN_PAGE_HTML)
        url = 'http://onlinepayment.majorcineplex.com/api/1.0/now_showing?w=320&h=480&x=2&o=0&pf=iOS&mid=iPhone%20Simulator&indent=0&deflate=1&appv=2.6&rev=2'
        result = urlfetch.fetch(url)
        mJson = json.loads(result.content)
#         self.response.out.write(mJson['success'])

        sign_query_params = urllib.urlencode({'mJson': mJson})

        self.response.write(MAIN_PAGE_HTML % (sign_query_params))
#         self.response.out.write(mJson)
        self.response.out.write(mJson['md5'])

class NookMai(webapp2.RequestHandler):

    def post(self):
        self.response.write('<html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

class NookMaiDetailMovie(webapp2.RequestHandler):

    def post(self):

#         self.response.write(MAIN_PAGE2_HTML)
        self.response.write('<html><body>DetailMovie<pre>')
        
        mJson = self.request.get('mJson', DEFAULT_MOVIE_NAME)
#         self.response.out.write(mJson['md5'])
        json_data = json.dumps(mJson)
        self.response.out.write(json_data)
        
# !!        
#         json_data = response.read()
#         print '\n '
#         response_dict = json.loads(json_data)
#         print response_dict.get("response_code",{})
# !!   
        
#         self.response.out.write(json_data['movies'])

#         self.response.write(cgi.escape(self.request.get(mJson['movies'])))
        
        self.response.write('</pre></body></html>')


#         self.response.write(MAIN_PAGE2_HTML)
#         mJson = self.request.get('mJson', )
#         self.response.out.write(mJson)



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', NookMai),
    ('/nextview', NookMaiDetailMovie),
], debug=True)