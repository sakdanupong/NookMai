import webapp2
import cgi
import json
import urllib
import os,sys
import jinja2
import datetime
import logging
import HTMLParser
import time

sys.path.append(os.path.abspath('models'))
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from apiclient.discovery import build
from optparse import OptionParser
from google.appengine.api import images
from pytz.gae import pytz
from pytz import timezone
from moviemodel import *
from cacheimagemodel import *
from commentmodel import *
from record_count_model import *
from decimal import *
from comingsoonmodel import *

from os import environ
from recaptcha.client import captcha

DEFAULT_COMMENT_NAME = 'default_user'

CAPTCHA_PUBLICE_KEY = '6LcDAO0SAAAAAIYP-BD0kxquYfqz71t1KeUbV1rp'
CAPTCHA_PRIVATE_KEY = '6LcDAO0SAAAAAM4kxOsIOBKRz8oLjj2-dHcBcui5'
CAPTCHA_PUBLICE_KEY_LOCALHOST = '6LdtC-0SAAAAAH5bs8gr19lSa896njyCiY1GE3Ti'
CAPTCHA_PRIVATE_KEY_LOCALHOST = '6LdtC-0SAAAAAKvLvewCc4m0_qb7MxuPgRhg0svA'
BANGKOK_TIMEZONE = pytz.timezone('Asia/Bangkok')
ALL_RECORD_COUNTER_KEY = 'allRecordCounter'
REFRESH_DATA_CACHE = 'REFRESH_DATA_CACHE'

def editMovieData():
    r = {'success':'success'}
    b = json.dumps(r)
    return b

def decodeHTML(str):
    html_parser = HTMLParser.HTMLParser()
    unescaped = html_parser.unescape(str)
    return unescaped

def covertUnixTimeToStrFotmat(i_unix_timestamp, str_format):
    tz = BANGKOK_TIMEZONE
    value = datetime.datetime.fromtimestamp(i_unix_timestamp, tz)
    return (value.strftime(str_format))

def checkDateFormat(str_date):
    success = 1
    try:
        datetime.datetime.strptime(str_date,"%d/%m/%Y")
    except ValueError as err:
        success = 0
    return success

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

def splitStr(str_to_split, split):
    s2 = str_to_split.split(split)
    return s2;

def increment_movie_comment_counter(c_key):
    c = db.get(c_key)
    c.comment_count += 1
    c.put()

def increment_record_comment_counter(c_key):
    c = db.get(c_key)
    c.comment_count += 1
    c.put()

def datetime_lctimezone_format(dt):
    ans_time = time.mktime(dt.timetuple())
    tz = BANGKOK_TIMEZONE
    value = datetime.datetime.fromtimestamp(ans_time, tz)
    return value

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,)
JINJA_ENVIRONMENT.filters['covertUnixTimeToStrFotmat']=covertUnixTimeToStrFotmat
JINJA_ENVIRONMENT.filters['editMovieData']=editMovieData
JINJA_ENVIRONMENT.filters['decodeHTML']=decodeHTML
JINJA_ENVIRONMENT.filters['datetime_lctimezone_format']=datetime_lctimezone_format


NOWSHOWING_DATA_PER_PAGE = 15
COMINGSOON_PER_PAGE = 10

class MainPage(webapp2.RequestHandler):

    def get(self):
        comingsoon_query = MovieModel.all().order('release_time_timestamp')
        coming_list = comingsoon_query.filter('is_coming_soon =', 1).fetch(limit=10)
        record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
        template_values = {
             # 'movie_list': movie_list,
             'comingsoon_list' : coming_list,
             'record_object' : record_object,
             'nowshowing_per_page' : NOWSHOWING_DATA_PER_PAGE, 
             'comingsoon_per_page' : COMINGSOON_PER_PAGE,
        }
        template = JINJA_ENVIRONMENT.get_template('movielist.html')
        self.response.write(template.render(template_values))

class RefreshData(webapp2.RequestHandler):


    def increment_record_movie_counter(self, c_key):
        c = db.get(c_key)
        c.movie_count += 1
        self.new_id = c.movie_count
        c.put()


    def increment_record_nowshowing_counter(self, c_key):
        c = db.get(c_key)
        c.nowshowing_count += 1
        c.put()

    def increment_record_comingsoon_counter(self, c_key):
        c = db.get(c_key)
        c.comingsoon_count += 1
        c.put()

    def get(self):
        data = memcache.get(REFRESH_DATA_CACHE)
        if data is not None:
            return
        else:
            memcache.add(key=REFRESH_DATA_CACHE, value=1, time=60)

        url = 'http://onlinepayment.majorcineplex.com/api/1.0/now_showing?w=768&h=1024&x=2&o=0&pf=iOS&mid=iPad&indent=0&deflate=1&appv=2.6&rev=2'
        result = urlfetch.fetch(url)
        mJson = json.loads(result.content)
        record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
        for m in mJson['movies']:
            q = MovieModel.all();
            q.filter('original_id =', m['id'])
            if q.count():
                continue
            db.run_in_transaction(self.increment_record_nowshowing_counter, record_object.key())
            db.run_in_transaction(self.increment_record_movie_counter, record_object.key())
            movie_id = str(self.new_id)
            e = MovieModel.get_or_insert(key_name=movie_id)
            e.original_id = m['id']
            e.id = self.new_id
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
            
            url = 'http://onlinepayment.majorcineplex.com/api/1.0/movie_detail?w=320&h=480&x=2&o=0&pf=iOS&mid=iPhone%20Simulator&indent=0&deflate=1&appv=2.6&rev=2&movie_id='+str(m['id'])
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

        data = memcache.get(REFRESH_DATA_CACHE)
        if data is not None:
            memcache.delete(key=REFRESH_DATA_CACHE)

        # coming_soon

        url = 'http://onlinepayment.majorcineplex.com/api/1.0/coming_soon?w=768&h=1024&x=2&o=0&pf=iOS&mid=iPad&indent=0&deflate=1&appv=2.6&rev=2'
        result = urlfetch.fetch(url)
        mJson = json.loads(result.content)
        
        for g in mJson['groups']:
            month_dict = g['name']
            g_coming_month_th = month_dict['th'];
            g_coming_month_en = month_dict['en'];
            csm = ComingSoonModel.get_or_insert(key_name=g_coming_month_en)
            csm.comming_month_en = g_coming_month_en
            csm.comming_month_th = g_coming_month_th
            for m in g['movies']: 
                q = MovieModel.all()
                q.filter('original_id =', m['id'])
                if q.count():
                  continue
                record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
                db.run_in_transaction(self.increment_record_movie_counter, record_object.key())   
                db.run_in_transaction(self.increment_record_comingsoon_counter, record_object.key())
                movie_id = str(self.new_id)
                e = MovieModel.get_or_insert(key_name=movie_id)
                e.coming_month_en = g_coming_month_en
                e.coming_month_th = g_coming_month_th
                e.is_coming_soon = 1
                e.id = self.new_id
                e.original_id = m['id']
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
                
                url = 'http://onlinepayment.majorcineplex.com/api/1.0/movie_detail?w=320&h=480&x=2&o=0&pf=iOS&mid=iPhone%20Simulator&indent=0&deflate=1&appv=2.6&rev=2&movie_id='+str(m['id'])
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

class ResetCounter(webapp2.RequestHandler):
    def get(self):
        record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
        if record_object is None:
            record_object = RecordCountModel.get_or_insert(key_name=ALL_RECORD_COUNTER_KEY)


class ImageCache(webapp2.RequestHandler):
    def get(self):
        movie_id = self.request.get('movie_id')
        image_query = CacheImageModel.get_or_insert(key_name=movie_id)
        if image_query.image is None:
            movie_model = MovieModel.get_by_key_name(movie_id)
            image_query.id = movie_model.id
            image_query.image = db.Blob(urlfetch.Fetch(movie_model.image).content)
            image_query.put()
        self.response.headers['Content-Type'] = 'image/*'
        self.response.out.write(image_query.image)

class UploadAndCacheImage(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        # logging.warning('############### xxxxxxxxx')
        success = 0
        movie_id = self.request.get('movie_id')
        # poster_img = images.resize(self.request.get('img'), 164, 248)
        poster_img = self.request.get('image')
        if poster_img:
            image_query = CacheImageModel.get_by_key_name(movie_id)
            image_query.id = int(movie_id)
            image_query.image = db.Blob(poster_img)
            image_query.put()
            success = 1
            dic = { 
                'success' : success,
            };
            self.response.out.write(json.dumps(dic))

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
        else:
            youtube_url = movie_model.youtube_url
            split_items = splitStr(youtube_url,'/')
            last_index = len(split_items) - 1
            videoId = split_items[last_index]
            dict = {
                'videoId' : videoId,
            }
            b = json.dumps(dict)
            return self.response.out.write(b)

class NookMai(webapp2.RequestHandler):

    def post(self):
        self.response.write('<html><body>You wrotesdsdsd:<pre>')
        self.response.write(self.request.get('content'))
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


        localhost = self.request.host
        key = CAPTCHA_PUBLICE_KEY
        if "localhost" in localhost.lower():
            key = CAPTCHA_PUBLICE_KEY_LOCALHOST

        chtml = captcha.displayhtml(
        public_key = key,
        use_ssl = False,
        error = None)

        # chtml = captcha.displayhtml(
        # public_key = CAPTCHA_PUBLICE_KEY,
        # use_ssl = False,
        # error = None)


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

        key = CAPTCHA_PRIVATE_KEY
        localhost = self.request.host
        if "localhost" in localhost.lower():
            key = CAPTCHA_PRIVATE_KEY_LOCALHOST

        cResponse = captcha.submit(
                    challenge,
                    response,
                    key,
                    remoteip)

        # cResponse = captcha.submit(
        #             challenge,
        #             response,
        #             CAPTCHA_PRIVATE_KEY,
        #             remoteip)




        success = 0

        if cResponse.is_valid:
            # response was valid
            # other stuff goes here
            # logging.warning('is_valid')

            content = self.request.get('content')
            movie_id = self.request.get('movie_id')
            author = self.request.get('author')
            emotion_review_id = self.request.get('emotion_review_id')
            # emotion_review_id = self.request.get('emotion_review_id')
            if content :
                c = CommentModel()
                c.movie_id = int(movie_id)
                c.content = cgi.escape(content)
                c.author = cgi.escape(author)
                c.emotion_review_id = int(emotion_review_id)
                # c.emotion_review_id = cgi.escape(emotion_review_id)
                movie_object = MovieModel.get_by_key_name(movie_id)
                db.run_in_transaction(increment_movie_comment_counter, movie_object.key())
                record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
                db.run_in_transaction(increment_record_comment_counter, record_object.key())
                c.put()
                success = 1

                

        else:
            error = cResponse.error_code
            logging.warning(error)
            

        r = {'success':success}
        self.response.out.write(json.dumps(r))

        #redirect view
        #self.redirect('/detail?movie_id='+movie_id)


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
            clist.append({'emotion_review_id':c.emotion_review_id,'author':c.author,'content':c.content,'date':datetime_lctimezone_format(c.date).strftime("%B %d, %Y") ,'time_crate':datetime_lctimezone_format(c.date).strftime("%H:%M") })

        r = {'data':clist}
        self.response.out.write(json.dumps(r))

class NookMaiBackOffice(webapp2.RequestHandler):
    def get(self):
        movie_query = MovieModel.all().order('-release_time_timestamp')
        movie_fetch = movie_query.fetch(limit=5)
        template_values = {
             'movie_list': movie_fetch,
        }
        template = JINJA_ENVIRONMENT.get_template('back_office.html')
        self.response.write(template.render(template_values))
        
class EditMovieData(webapp2.RequestHandler):
    def get(self):
        movie_id = self.request.get('movie_id')
        movie_model = MovieModel.get_by_key_name(movie_id);
        template_values = {
            'movie_model' : movie_model,
        }
        template = JINJA_ENVIRONMENT.get_template('edit_movie_data.html')
        self.response.write(template.render(template_values))
    def post(self):
        movie_model = MovieModel()
        template_values = {
            'movie_model' : movie_model,
        }
        template = JINJA_ENVIRONMENT.get_template('edit_movie_data.html')
        self.response.write(template.render(template_values))
        

class APIEditMovie(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        movie_id = self.request.get('movie_id')
        name_th = self.request.get('name_th')
        name_en = self.request.get('name_en')
        duration = self.request.get('duration')
        release_time_timestamp = self.request.get('release_time_timestamp')
        youtube_url = self.request.get('youtube_url')
        synopsis_en = self.request.get('synopsis_en')
        synopsis_th = self.request.get('synopsis_th')
        genre_en = self.request.get('genre_en')
        genre_th = self.request.get('genre_th')
        director_en = self.request.get('director_en')
        director_th = self.request.get('director_th')
        cast_en = self.request.get('cast_en')
        cast_th = self.request.get('cast_th')

        success = 1 

        fieldProblems = []
        movie_model = MovieModel.get_by_key_name(movie_id)

        if  name_th and name_en and youtube_url:
            movie_model.name_th = name_th
            movie_model.name_en = name_en
        else:    
            if not name_en:
                fieldProblems.append(0)
            if not name_th:
                fieldProblems.append(1)
            if not youtube_url:
                fieldProblems.append(4)
            success = 0

        if success == 1:
            if not checkDateFormat(release_time_timestamp):
                success = 0
                fieldProblems.append(3)
            else:
                date_object = datetime.datetime.strptime(release_time_timestamp,"%d/%m/%Y")
                ans_time = time.mktime(date_object.timetuple())
                movie_model.release_time_timestamp = int(ans_time)
                success = 1# to do add data to data store
        
        if success == 1:
            if not isint(duration):
                success = 0
                fieldProblems.append(5)
            else:
                movie_model.duration = int(duration)        
                success = 1# to do add data to data store

        g_yt_url = ''

        if success == 1:
            if youtube_url is None:
                fieldProblems.append(4)
                success = 0
            else:
                split_items = splitStr(youtube_url,'=')
                if len(split_items) <= 1:
                    split_items = splitStr(youtube_url,'/')
                last_index = len(split_items) - 1
                videoId = split_items[last_index]
                yt_url = "//www.youtube.com/embed/" + videoId
                g_yt_url = yt_url
                movie_model.youtube_url = yt_url

        movie_model.detail_synopsis_en = synopsis_en
        movie_model.detail_synopsis_th = synopsis_th
        movie_model.detail_genre_en = genre_en
        movie_model.detail_genre_th = genre_th
        movie_model.detail_director_en = director_en
        movie_model.detail_director_th = director_th
        movie_model.detail_cast_en = cast_en
        movie_model.detail_cast_th = cast_th

        if (success == 1):
            movie_model.put()

        r = {
            'success' : success,
            'fieldProblems' : fieldProblems,
            'youtube_url' : g_yt_url,
        }

        self.response.out.write(json.dumps(r))

class GetNowShowing(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        page = int(self.request.get('page'))
        page -= 1
        data_per_page = 15
        l_offset = page * data_per_page
        movie_query = MovieModel.all().order('-release_time_timestamp').filter('is_coming_soon =', 0)
        movie_list = movie_query.run(offset=l_offset, limit=data_per_page)
        list = []
        for movie in movie_list:
            movie_json = {
                'movie_id' : movie.id,
                'name_en' : movie.name_en,
                'name_th' : movie.name_th,
            }
            list.append(movie_json)

        r = {
            'movie_list' : list,   
        }

        self.response.out.write(json.dumps(r))
    # movie_list = movie_query.filter('is_coming_soon =', 0).fetch(limit=datape)

class GetComingSoon(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        page = int(self.request.get('page'))
        page -= 1
        data_per_page = 10
        l_offset = page * data_per_page
        movie_query = MovieModel.all().order('-release_time_timestamp').filter('is_coming_soon =', 1)
        movie_list = movie_query.run(offset=l_offset, limit=data_per_page)
        list = []
        for movie in movie_list:
            movie_json = {
                'movie_id' : movie.id,
                'name_en' : movie.name_en,
                'name_th' : movie.name_th,
            }
            list.append(movie_json)
        r = {
            'movie_list' : list,   
        }

        self.response.out.write(json.dumps(r))
    # movie_list = movie_query.filter('is_coming_soon =', 0).fetch(limit=datape)



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', NookMai),
    ('/detail', NookMaiDetailMovie),
    ('/refresh_data', RefreshData),
    ('/image', ImageCache),
    ('/trailer', GetTrailer),
    ('/back_office', NookMaiBackOffice),
    ('/api_add_comment', AddComment),
    ('/api_get_comment', GetComment),
    ('/backoffice', NookMaiBackOffice),
    ('/edit_movie_data', EditMovieData),
    ('/api_edit_movie_data', APIEditMovie),
    ('/upload_poster', UploadAndCacheImage),
    ('/reset_counter', ResetCounter),
    ('/api_get_nowshowing', GetNowShowing),
    ('/api_get_comingsoon', GetComingSoon),
], debug=True)















