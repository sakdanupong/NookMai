import webapp2
import cgi
import json
import urllib
import os,sys
import jinja2
import logging

sys.path.append(os.path.abspath('models'))
from google.appengine.api import users
from google.appengine.api import urlfetch
from apiclient.discovery import build
from optparse import OptionParser
from moviemodel import *
from cacheimagemodel import *
from commentmodel import *

from os import environ
from recaptcha.client import captcha

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


DEFAULT_COMMENT_NAME = 'default_user'

CAPTCHA_PUBLICE_KEY = '6LcDAO0SAAAAAIYP-BD0kxquYfqz71t1KeUbV1rp'
CAPTCHA_PRIVATE_KEY = '6LcDAO0SAAAAAM4kxOsIOBKRz8oLjj2-dHcBcui5'
CAPTCHA_PUBLICE_KEY_LOCALHOST = '6LdtC-0SAAAAAH5bs8gr19lSa896njyCiY1GE3Ti'
CAPTCHA_PRIVATE_KEY_LOCALHOST = '6LdtC-0SAAAAAKvLvewCc4m0_qb7MxuPgRhg0svA'


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
        url = 'http://onlinepayment.majorcineplex.com/api/1.0/now_showing?w=768&h=1024&x=2&o=0&pf=iOS&mid=iPad&indent=0&deflate=1&appv=2.6&rev=2'
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


def getMovieTrailerFromText(movie_name):
    text_for_serch = movie_name + ' trailer'
    youtube = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION, 
    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
    q=""+text_for_serch,
    part="id,snippet",
    type='video',
    maxResults=5
    ).execute()
    video_items = search_response['items']
    return video_items

DEVELOPER_KEY = "AIzaSyCN0HA7pGrgF6bnLKNckBSc-Lm9NvY0FAk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
class GetTrailer(webapp2.RequestHandler):
    def get(self):
        movie_id = self.request.get('movie_id')
        movie_model = MovieModel.get_by_key_name(movie_id)
        if movie_model.youtube_url is None:
            movie_name_th = movie_model.name_th
            movie_name_en = movie_model.name_en
            text_for_serch = movie_name_en + ' ' + movie_name_th
            video_items = getMovieTrailerFromText(text_for_serch)
            video_item = None
            if len(video_items) > 0:
                video_item = video_items[0]
            if video_item is None:
                video_items = getMovieTrailerFromText(movie_name_en)
                if len(video_items) > 0:
                    video_item = video_items[0]
            if video_item is None:
                video_items = getMovieTrailerFromText(movie_name_th)
                if len(video_items) > 0:
                    video_item = video_items[0]
            item_id = video_item['id']
            b = json.dumps(item_id)
            # save youtube url to movie model
            youtube_url = "//www.youtube.com/embed/"+item_id['videoId'];
            movie_model.youtube_url = youtube_url
            movie_model.put()
            return self.response.out.write(b)

class NookMai(webapp2.RequestHandler):

    def post(self):
        self.response.write('<html><body>You wrotesdsdsd:<pre>')
        self.response.write(cgi.escape(self.request.get('content')))
        self.response.write('</pre></body></html>')

class NookMaiDetailMovie(webapp2.RequestHandler):

    def get(self):

        movie_id = self.request.get('movie_id')
        movie_data = MovieModel.get_or_insert(key_name=movie_id)



        #query show comment
        q = CommentModel.all();
        q.filter('movie_id =', int(movie_id))
        q.order('-date')
        comments = []
        for c in q.fetch(limit=100) :
            comments.append(c)
        

        # chtml = captcha.displayhtml(
        # public_key = "6LdtC-0SAAAAAH5bs8gr19lSa896njyCiY1GE3Ti",
        # use_ssl = False,
        # error = None)
        chtml = captcha.displayhtml(
        public_key = CAPTCHA_PUBLICE_KEY_LOCALHOST,
        use_ssl = False,
        error = None)


        template_values = {
            'movie_data': movie_data,
            'comments':comments,
            'captchahtml': chtml,
        }

        
        template = JINJA_ENVIRONMENT.get_template('movie_detail.html')
        self.response.write(template.render(template_values))







# API 

class AddComment(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        # 
        challenge = self.request.get('recaptcha_challenge_field')
        response  = self.request.get('recaptcha_response_field')
        # remoteip  = environ['REMOTE_ADDR']
        remoteip = self.request.remote_addr

        # cResponse = captcha.submit(
        #             challenge,
        #             response,
        #             "6LdtC-0SAAAAAKvLvewCc4m0_qb7MxuPgRhg0svA",
        #             remoteip)

        cResponse = captcha.submit(
                    challenge,
                    response,
                    CAPTCHA_PRIVATE_KEY_LOCALHOST,
                    remoteip)


        success = 0

        if cResponse.is_valid:
            # response was valid
            # other stuff goes here
            # logging.warning('is_valid')

            content = self.request.get('content')
            movie_id = self.request.get('movie_id')
            author = self.request.get('author')
            if content :
                c = CommentModel()
                c.movie_id = int(movie_id)
                c.content = cgi.escape(content)
                c.author = cgi.escape(author)
                c.put()
                success = 1
       

        else:
            error = cResponse.error_code
            logging.warning(error)

        r = {'success':success}
        self.response.out.write(json.dumps(r))



        # content = self.request.get('content')
        # movie_id = self.request.get('movie_id')
        # author = self.request.get('author')
        # success = 0
        # if content :
        #     c = CommentModel()
        #     c.movie_id = int(movie_id)
        #     c.content = cgi.escape(content)
        #     c.author = cgi.escape(author)
        #     c.put()
        #     success = 1
       
        # r = {'success':success}
        # self.response.out.write(json.dumps(r))

        #redirect view
        #self.redirect('/nextview?movie_id='+movie_id)


class GetComment(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        movie_id = self.request.get('movie_id')
        q = CommentModel.all();
        q.filter('movie_id =', int(movie_id))
        q.order('-date')
        clist = []
        for c in q.fetch(limit=100) :
            clist.append({'author':c.author,'content':c.content})
        r = {'data':clist}
        self.response.out.write(json.dumps(r))

class NookMaiBackOffice(webapp2.RequestHandler):
    def get(self):
        movie_query = MovieModel.all().order('-release_time_timestamp')
        template_values = {
             'movie_list': movie_query,
        }
        template = JINJA_ENVIRONMENT.get_template('back_office.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', NookMai),
    ('/nextview', NookMaiDetailMovie),
    ('/refresh_data', RefreshData),
    ('/image', ImageCache),
    ('/trailer', GetTrailer),
    ('/back_office', NookMaiBackOffice),
    ('/api_add_comment', AddComment),
    ('/api_get_comment', GetComment),
    ('/backoffice', NookMaiBackOffice),
], debug=True)















