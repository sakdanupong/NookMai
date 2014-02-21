# coding=utf-8
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
import re
import hashlib

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
from ratemoviemodel import *
from aboutmodel import *
from record_count_model import *
from decimal import *
from comingsoonmodel import *
from usermodel import *
from sessionmodel import *

from os import environ
from recaptcha.client import captcha
from random import randint
from google.appengine.api import search 

DEFAULT_COMMENT_NAME = 'default_user'


CAPTCHA_PUBLICE_KEY = '6LcDAO0SAAAAAIYP-BD0kxquYfqz71t1KeUbV1rp'
CAPTCHA_PRIVATE_KEY = '6LcDAO0SAAAAAM4kxOsIOBKRz8oLjj2-dHcBcui5'
CAPTCHA_PUBLICE_KEY_LOCALHOST = '6LdtC-0SAAAAAH5bs8gr19lSa896njyCiY1GE3Ti'
CAPTCHA_PRIVATE_KEY_LOCALHOST = '6LdtC-0SAAAAAKvLvewCc4m0_qb7MxuPgRhg0svA'
CAPTCHA_PUBLICE_KEY_ON_SITE = '6LeOke4SAAAAAD-1NDoSDLnYiyB6u6LFQMBTLpoI'
CAPTCHA_PRIVATE_KEY_ON_SITE = '6LeOke4SAAAAADxGWug_wOw14wdX2Ai8EEHcY28B'
BANGKOK_TIMEZONE = pytz.timezone('Asia/Bangkok')
ALL_RECORD_COUNTER_KEY = 'allRecordCounter'
REFRESH_DATA_CACHE = 'REFRESH_DATA_CACHE'
AVATAR_COUNT = 14

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

def increment_movie_comment_avatar_counter(c_key, avatar_id):
    c = db.get(c_key)
    logging.warning('!!!!!!!increment_movie_comment_avatar_counter')


    if avatar_id == 1:
        c.avatar_1_count += 1
    elif avatar_id== 2:
        c.avatar_2_count += 1
    elif avatar_id == 3:
        c.avatar_3_count += 1
    elif  avatar_id== 4:
        c.avatar_4_count += 1
    elif  avatar_id== 5:
        c.avatar_5_count += 1
    elif  avatar_id== 6:
        c.avatar_6_count += 1
    elif  avatar_id== 7:
        c.avatar_7_count += 1
    elif  avatar_id== 8:
        c.avatar_8_count += 1
    elif  avatar_id== 9:
        c.avatar_9_count += 1
    elif  avatar_id== 10:
        c.avatar_10_count += 1
    elif  avatar_id== 11:
        c.avatar_11_count += 1
    elif  avatar_id== 12:
        c.avatar_12_count += 1
    elif  avatar_id== 13:
        c.avatar_13_count += 1
    elif  avatar_id== 14:
        c.avatar_14_count += 1

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

def getNowShowing(l_offset, data_per_page):
    movie_query = MovieModel.all().filter('is_coming_soon =', 0)
    movie_query = movie_query.filter('release_time_timestamp !=', None)
    movie_query = movie_query.order('-release_time_timestamp')
    movie_list = movie_query.run(offset=l_offset, limit=data_per_page)
    list = []
    for movie in movie_list:
        movie_json = {
            'movie_id' : movie.id,
            'name_en' : movie.name_en,
            'name_th' : movie.name_th,
            'avatar_1_count' : movie.avatar_1_count,
            'avatar_2_count' : movie.avatar_2_count,
            'avatar_3_count' : movie.avatar_3_count,
            'avatar_4_count' : movie.avatar_4_count,
            'avatar_5_count' : movie.avatar_5_count,
            'avatar_6_count' : movie.avatar_6_count,
            'avatar_7_count' : movie.avatar_7_count,
            'avatar_8_count' : movie.avatar_8_count,
            'avatar_9_count' : movie.avatar_9_count,
            'avatar_10_count' : movie.avatar_10_count,
            'avatar_11_count' : movie.avatar_11_count,
            'avatar_12_count' : movie.avatar_12_count,
            'avatar_13_count' : movie.avatar_13_count,
            'avatar_14_count' : movie.avatar_14_count,
        }
        list.append(movie_json)

    r = {
        'movie_list' : list,   
    }

    return json.dumps(r)

def getComingSoon(l_offset, data_per_page):
    movie_query = MovieModel.all().filter('is_coming_soon =', 1)
    movie_query = movie_query.filter('release_time_timestamp !=', None)
    movie_query = movie_query.order('-release_time_timestamp')
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
    return json.dumps(r)

def summaryNumber(number):
    result_num = 0
    number_len = len(str(number))
    if number_len < 4:
        return str(number)
    result_num = number / 1000.0
    result_num ="%.2f" % result_num
    str_result = str(result_num) + 'k'
    return str_result

def getUserData(usermodel):
    userData = {
        'user_id' : usermodel.user_id,
        'username' : usermodel.username,
        'email' : usermodel.email,
        'session_token' : usermodel.session_token,
    }
    return userData;

def setCookie(response , request, name, value):
    localhost = request.host
    expires_date = datetime.datetime.now() + datetime.timedelta(datetime.MAXYEAR)
    response.set_cookie(name, value, expires=expires_date)
    # response.set_cookie('name', 'value', expires=datetime.datetime.now(), path='/', domain='example.com')

def getCookie(request):
    value = None
    cookies = {}
    raw_cookies = request.headers.get("Cookie")
    if raw_cookies:
        for cookie in raw_cookies.split(";"):
            name, value = cookie.split("=")
            for name, value in cookie.split("="):
                cookies[name] = value

    return cookies


def getUserModel(request):
    userData = None
    session_token = request.cookies.get("session_token")
        # logging.warning('#################### ' + session_token)
    if session_token:
        sessionModel = SessionModel.get_by_key_name(session_token)
        if not sessionModel is None:
            userData = UserModel.get_by_key_name(str(sessionModel.user_id))
    return userData


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,)
JINJA_ENVIRONMENT.filters['covertUnixTimeToStrFotmat']=covertUnixTimeToStrFotmat
JINJA_ENVIRONMENT.filters['editMovieData']=editMovieData
JINJA_ENVIRONMENT.filters['decodeHTML']=decodeHTML
JINJA_ENVIRONMENT.filters['datetime_lctimezone_format']=datetime_lctimezone_format
JINJA_ENVIRONMENT.filters['summaryNumber']=summaryNumber


NOWSHOWING_DATA_PER_PAGE = 15
COMINGSOON_PER_PAGE = 10

class MainPage(webapp2.RequestHandler):

    def get(self):
        record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
        movie_list = getNowShowing(0, NOWSHOWING_DATA_PER_PAGE)
        movie_json = json.loads(movie_list)
        movie_list = movie_json['movie_list']
        magic_number = randint(0, len(movie_list) - 1)
        random_movie = movie_list[magic_number]
        userData = getUserModel(self.request)
        template_values = {
             'random_movie' : random_movie,
             'record_object' : record_object,
             'avatar_count' : AVATAR_COUNT,
             'nowshowing_per_page' : NOWSHOWING_DATA_PER_PAGE, 
             'comingsoon_per_page' : COMINGSOON_PER_PAGE,
             'userData' : userData,

        }
        template = JINJA_ENVIRONMENT.get_template('movielist.html')
        # template = JINJA_ENVIRONMENT.get_template('test_responsive.html')
        self.response.write(template.render(template_values))
    def post(self):
        record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
        movie_list = getNowShowing(0, NOWSHOWING_DATA_PER_PAGE)
        movie_json = json.loads(movie_list)
        movie_list = movie_json['movie_list']
        magic_number = randint(0, len(movie_list) - 1)
        random_movie = movie_list[magic_number]

        scroll_to = self.request.get('scroll_to')
        userData = getUserModel(self.request)

        template_values = {
             'random_movie' : random_movie,
             'record_object' : record_object,
             'avatar_count' : AVATAR_COUNT,
             'nowshowing_per_page' : NOWSHOWING_DATA_PER_PAGE, 
             'comingsoon_per_page' : COMINGSOON_PER_PAGE,
             'scroll_to' : scroll_to,
             'userData' : userData,
        }
        template = JINJA_ENVIRONMENT.get_template('movielist.html')
        # template = JINJA_ENVIRONMENT.get_template('test_responsive.html')
        self.response.write(template.render(template_values))
        

class NowShowing(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        data_per_page = NOWSHOWING_DATA_PER_PAGE * 2
        record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
        template_values = {
             'record_object' : record_object, 
             'data_per_page' : data_per_page,
        }
        template = JINJA_ENVIRONMENT.get_template('now_showing.html')
        self.response.write(template.render(template_values))
        # self.response.write(template.render(template_values))
        

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

    def decrement_record_comingsoon_counter(self, c_key):
        c = db.get(c_key)
        c.comingsoon_count -= 1
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
                comingsoon = q[0];
                is_comingsoon = comingsoon.is_coming_soon
                if is_comingsoon:
                    db.delete(comingsoon);
                    db.run_in_transaction(self.decrement_record_comingsoon_counter, comingsoon.key())
                else:
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
            e.put()

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
                e.put()

        data = memcache.get(REFRESH_DATA_CACHE)
        if data is not None:
            memcache.delete(key=REFRESH_DATA_CACHE)

class ResetCounter(webapp2.RequestHandler):
    def get(self):
        record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
        if record_object is None:
            record_object = RecordCountModel.get_or_insert(key_name=ALL_RECORD_COUNTER_KEY)


class ImageCache(webapp2.RequestHandler):
    def showImage(self, image):
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(image)
        return image
    def get(self):
        movie_id = self.request.get('movie_id')
        image_cache_key = ''+str(movie_id)
        image = memcache.get(image_cache_key)
        if image is not None:
            self.showImage(image)
        else:
            image_query = CacheImageModel.get_or_insert(key_name=movie_id)
            if image_query.image is None:
                movie_model = MovieModel.get_by_key_name(movie_id)
                image_query.id = movie_model.id
                image_query.image = db.Blob(urlfetch.Fetch(movie_model.image).content)
                image_query.put()
            self.showImage(image_query.image)                
            memcache.add(key=image_cache_key, value=image_query.image)

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
            youtube_url = "//www.youtube.com/embed/"+item_id['videoId']
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

def get_cookies(request):
    cookies = {}
    raw_cookies = request.headers.get("Cookie")
    if raw_cookies:
        for cookie in raw_cookies.split(";"):
            name, value = cookie.split("=")
            for name, value in cookie.split("="):
                cookies[name] = value
    return cookies

class NookMaiDetailMovie(webapp2.RequestHandler):

    def get(self, movie_id):

        movie_data = MovieModel.get_or_insert(key_name=movie_id)

        detail_en = movie_data.detail_synopsis_en
        detail_th = movie_data.detail_synopsis_th
        detail_director_en = movie_data.detail_genre_en
        detail_director_th = movie_data.detail_genre_th
        detail_cast_en = movie_data.detail_cast_en
        detail_cast_th = movie_data.detail_cast_th



        if detail_th is None and detail_en is None and detail_director_en is None and detail_director_th is None and detail_cast_en is None and detail_cast_th is None:
            movie_original_id = str(movie_data.original_id)
            url = 'http://onlinepayment.majorcineplex.com/api/1.0/movie_detail?w=320&h=480&x=2&o=0&pf=iOS&mid=iPhone%20Simulator&indent=0&deflate=1&appv=2.6&rev=2&movie_id='+movie_original_id
            result = urlfetch.fetch(url)
            mJson = json.loads(result.content)
            
            movie_detail = mJson['detail']
            movie_data.detail_duration = movie_detail['duration']
            movie_data.detail_rate = movie_detail['rate']
            movie_data.detail_rateWarning = movie_detail['rateWarning']
            
            releasedate = movie_detail['releasedate']
            movie_data.detail_timestamp = releasedate['timestamp']
            movie_data.detail_text = releasedate['text']

            synopsis = movie_detail['synopsis']
            movie_data.detail_synopsis_en = synopsis['en']
            movie_data.detail_synopsis_th = synopsis['th']

            movie_data.detail_image = movie_detail['image']

            trailer = movie_detail['trailer']
            movie_data.detail_yt_id = trailer['yt_id']
            movie_data.detail_rtsp = trailer['rtsp']
            movie_data.detail_thumbnail = trailer['thumbnail']

            genre = movie_detail['genre']
            movie_data.detail_genre_en = genre['en']
            movie_data.detail_genre_th = genre['th']
            
            director = movie_detail['director']
            movie_data.detail_director_en = director['en']
            movie_data.detail_director_th = director['th']
            
            cast = movie_detail['cast']
            movie_data.detail_cast_en = cast['en']
            movie_data.detail_cast_th = cast['th']
            movie_data.put()


        #query show comment
        q = CommentModel.all()
        q.filter('movie_id =', int(movie_id))
        q.order('-date')
        comments = []
        for c in q.fetch(limit=100) :
            comments.append(c)


        # query user
        userdata = getUserModel(self.request)


        # query user rate
        r = RateMovieModel.all()
        r.filter('username =', userdata.username)
        r.filter('movie_id =', int(movie_id))

        if r.count() > 0 :
            result = r.fetch(limit=10)
            rate_data = result[0]

        # query user vote comment


        localhost = self.request.host
        key = CAPTCHA_PUBLICE_KEY
        if "localhost" in localhost.lower():
            key = CAPTCHA_PUBLICE_KEY_LOCALHOST
        elif "appspot" in localhost.lower():
            key = CAPTCHA_PUBLICE_KEY
        else:
            key = CAPTCHA_PUBLICE_KEY_ON_SITE

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
            'userdata': userdata,
            'rate_data': rate_data,
        }

        
        template = JINJA_ENVIRONMENT.get_template('movie_detail.html')
        self.response.write(template.render(template_values))



class NookMaiAbout(webapp2.RequestHandler):

    def get(self, ):

        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render())



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
        elif "appspot" in localhost.lower():
            key = CAPTCHA_PRIVATE_KEY
        else:
            key = CAPTCHA_PRIVATE_KEY_ON_SITE


        cResponse = captcha.submit(
                    challenge,
                    response,
                    key,
                    remoteip)


        if "localhost" in localhost.lower():
            cResponse.is_valid = True;

        success = 0

        if cResponse.is_valid:
            # response was valid
            # other stuff goes here
            # logging.warning('is_valid')

            content = self.request.get('content')
            # logging.warning('content1'+content)
            # logging.warning('content2'+content)

            movie_id = self.request.get('movie_id')
            author = self.request.get('author')
            avatar_review_id = self.request.get('avatar_review_id')
            # avatar_review_id = self.request.get('avatar_review_id')
            if content :
                c = CommentModel()
                c.movie_id = int(movie_id)
                c.content = cgi.escape(content).replace('\n', '<br/>')
                c.author = cgi.escape(author)
                c.avatar_review_id = int(avatar_review_id)
                # c.avatar_review_id = cgi.escape(avatar_review_id)
                movie_object = MovieModel.get_by_key_name(movie_id)
                db.run_in_transaction(increment_movie_comment_counter, movie_object.key())


                db.run_in_transaction(increment_movie_comment_avatar_counter, movie_object.key(), c.avatar_review_id)

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
            clist.append({'avatar_review_id':c.avatar_review_id ,'author':c.author ,'content':c.content ,'vote_count':c.vote_count,'comment_id':c.key().id(),'date':datetime_lctimezone_format(c.date).strftime("%B %d, %Y") ,'time_crate':datetime_lctimezone_format(c.date).strftime("%H:%M") })

        r = {'data':clist}
        self.response.out.write(json.dumps(r))


class AddRateMovie(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        logging.warning('AddRateMovie!!!!!!!!!')

        remoteip = self.request.remote_addr
        localhost = self.request.host
        success = 0

        movie_id = self.request.get('movie_id')
        user_id = self.request.get('user_id')
        username = self.request.get('username')
        rate_score = self.request.get('rate_score')

        q = RateMovieModel()
        q.movie_id = int(movie_id)
        q.user_id = int(user_id)
        q.username = cgi.escape(username)
        q.rate_score = int(rate_score)

        q.put()
        success = 1
 
        r = {'success':success}
        self.response.out.write(json.dumps(r))

 # class GetRateMoive(webapp2.RequestHandler):
 #    def get(self):
 #        self.process()
 #    def post(self):
 #        self.process()
 #    def process(self):
        # remoteip = self.request.remote_addr
        # localhost = self.request.host
        # success = 0

        # comment_id = self.request.get('comment_id')
        # user_id = self.request.get('user_id')
        # movie_id = self.request.get('movie_id')

        # q = CommentModel.all();
        # q = CommentModel.get_by_id(long(comment_id))
        # logging.warning(q)

        # if q.vote_count :
        #     q.vote_count = q.vote_count+1
        # else :
        #     q.vote_count = 1

        # q.put()
        # success = 1
 
        # r = {'success':success}
        # self.response.out.write(json.dumps(r))       

class VoteComment(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        remoteip = self.request.remote_addr
        localhost = self.request.host
        success = 0

        comment_id = self.request.get('comment_id')
        user_id = self.request.get('user_id')
        movie_id = self.request.get('movie_id')

        q = CommentModel.all();
        q = CommentModel.get_by_id(long(comment_id))
        logging.warning(q)

        if q.vote_count :
            q.vote_count = q.vote_count+1
        else :
            q.vote_count = 1

        q.put()
        success = 1
 
        r = {'success':success}
        self.response.out.write(json.dumps(r))


class UnvoteComment(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        remoteip = self.request.remote_addr
        localhost = self.request.host
        success = 0

        comment_id = self.request.get('comment_id')
        user_id = self.request.get('user_id')
        movie_id = self.request.get('movie_id')

        q = CommentModel.all();
        q = CommentModel.get_by_id(long(comment_id))
        logging.warning(q)

        if q.vote_count :
            q.vote_count = q.vote_count-1
        else :
            q.vote_count = -1

        q.put()
        success = 1
 
        r = {'success':success}
        self.response.out.write(json.dumps(r))



class AddAbout(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        remoteip = self.request.remote_addr

        localhost = self.request.host


        success = 0

            # response was valid
            # other stuff goes here
            # logging.warning('is_valid')
        description = self.request.get('description')
        name = self.request.get('name')
        email = self.request.get('email')


        if description :
            a = AboutModel()
            a.description = cgi.escape(description).replace('\n', '<br/>')
            a.name = cgi.escape(name)
            a.email = cgi.escape(email)

            a.put()
            success = 1

        r = {'success':success}
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
        data_per_page = int(self.request.get('data_per_page'))
        l_offset = page * data_per_page
        r = getNowShowing(l_offset, data_per_page)
        self.response.out.write(r)
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
        r = getComingSoon(l_offset, data_per_page)

        self.response.out.write(r)
    # movie_list = movie_query.filter('is_coming_soon =', 0).fetch(limit=datape)
class GetSeachMovie(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        word = self.request.get('word')
        movie_query = MovieModel.all().filter('name_en >=', unicode(word)).filter('name_en <',  unicode(word) + u"\ufffd").fetch(10)

        movie = movie_query[0]
        logging.warning(movie.name_en)


class Register(webapp2.RequestHandler):

    def checkUsername(self, username):
        success = 0
        user_regex = re.compile("^[A-Za-z0-9_-]{4,15}$")
        u = user_regex.search(username)
        if u:
            success = 1
        return success

    def checkEmail(self, email):
        success = 0
        if not email:
            success = 1
        else:
            email_regex = re.compile(r"[\w.-]+@[\w.-]+")
            e = email_regex.search(email)
            if e:
                success = 1
        return success

    
    def increment_user_counter(self, c_key):
        c = db.get(c_key)
        c.user_count += 1
        self.new_user_id = c.user_count
        c.put()

    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        success = 0
        reason = ""
        username = self.request.get('username')
        password = self.request.get('password')
        email = self.request.get('email')
        findUser = UserModel.all().filter("username =", username)
        userData = None
        if findUser.count() == 0:
            success = self.checkUsername(username)
            if success:
                success = self.checkEmail(email)
                if success:
                    record_object = RecordCountModel.get_by_key_name(ALL_RECORD_COUNTER_KEY)
                    db.run_in_transaction(self.increment_user_counter, record_object.key())
                    usermodel = UserModel.get_or_insert(key_name=str(self.new_user_id))
                    usermodel.username = username
                    usermodel.password = password
                    usermodel.user_id = self.new_user_id
                    usermodel.email = email
                    session_token = hashlib.md5(username+"nookmai").hexdigest()
                    usermodel.session_token = session_token
                    sessionModel = SessionModel.get_or_insert(key_name=session_token)
                    sessionModel.session_token = session_token
                    sessionModel.user_id = self.new_user_id

                    usermodel.put()
                    sessionModel.put()

                    userData = getUserData(usermodel)

                    setCookie(self.response, self.request, 'session_token', session_token)

                else:
                    reason = "Email ไม่ถูกต้อง"
            else:
                reason = "username กรุณาใช้ภาษาอังกฤษ ตัวเลข _ - และ มีตัวอักษร 4 - 15 ตัว เท่านั้น"

        else:
            reason = "มี username นี้อยู่แล้วในระบบ"


        r = {
            'success' : success,
            'reason' : reason,
            'data' : userData,
        }

        self.response.out.write(json.dumps(r))

class Login(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        success = 0
        userData = None
        reason = ""
        username = self.request.get('username')
        password = self.request.get('password')
        findUser = UserModel.all().filter("username =", username)
        if findUser.count():
            usermodel = findUser[0]
            # logging.warning('password = ' +password + ' database password = ' + usermodel.password)
            if password == usermodel.password:
                success = 1
                userData = getUserData(usermodel)
                setCookie(self.response, self.request, 'session_token', usermodel.session_token)
            else:
                reason = "Password ไม่ถูกต้อง"

        else:
            reason = "Username นี้ไม่มีอยู่ในระบบ"


        r = {
            'success' : success,
            'reason' : reason,
            'data' : userData,
        }

        self.response.out.write(json.dumps(r))

class GetUserData(webapp2.RequestHandler):
    def get(self):
        self.process()
    def post(self):
        self.process()
    def process(self):
        success = 0
        userData = None
        reason = ""
        session_token = self.request.get('session_token')
        sessionModel = SessionModel.get_by_key_name(session_token)
        if not sessionModel is None:
            usermodel = UserModel.get_by_key_name(str(sessionModel.user_id))
            if not sessionModel is None:
                success = 1
                userData = getUserData(usermodel)

        r = {
            'success' : success,
            'reason' : reason,
            'data' : userData,
        }

        self.response.out.write(json.dumps(r))

        


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', NookMai),
    ('/detail/(.*)', NookMaiDetailMovie),
    ('/about', NookMaiAbout),
    ('/refresh_data', RefreshData),
    ('/image', ImageCache),
    ('/trailer', GetTrailer),
    ('/back_office', NookMaiBackOffice),
    ('/api_add_comment', AddComment),
    ('/api_get_comment', GetComment),
    ('/api_add_rate_movie', AddRateMovie),
    # ('/api_get_rate_movie', GetRateMovie),
    ('/api_vote_comment', VoteComment),
    ('/api_unvote_comment', UnvoteComment),
    ('/api_add_about', AddAbout),
    ('/backoffice', NookMaiBackOffice),
    ('/edit_movie_data', EditMovieData),
    ('/api_edit_movie_data', APIEditMovie),
    ('/upload_poster', UploadAndCacheImage),
    ('/reset_counter', ResetCounter),
    ('/api_get_nowshowing', GetNowShowing),
    ('/api_get_comingsoon', GetComingSoon),
    ('/api_get_searchmovie', GetSeachMovie),
    ('/api_register', Register),
    ('/api_login', Login),
    ('/api_get_userdata', GetUserData),
], debug=True)















