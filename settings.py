#coding: utf8
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

MEDIA_DIR_NAME = 'media'
MEDIA_ROOT = os.path.join(BASE_DIR, "static", MEDIA_DIR_NAME)


db = {
    'host': "127.0.0.1",
    'user': "root",
    'passwd': "",
    'database': "blog",
    'charset': "utf8"
}

#tornado configuration
from app import ui
def builder_tornado_env(views_dir='admin'):
    return dict(
        template_path       = os.path.join(BASE_DIR, 'app', 'views', views_dir),
        static_path         = os.path.join(BASE_DIR, 'static'),
        xsrf_cookies        = False,
        cookie_secret       = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        autoescape          = None,
        ui_modules          = ui,
        debug               = DEBUG,
    )

db_ping_seconds = 30


import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


weibo_app_key = 'xxxxxxx'
weibo_app_secret = 'xxxxxxxxxxxxxxxxxx'
weibo_login_callback = 'xxxxxxxxxxxxxxxxxxx'


try:
    from settings_local import *
except:
    pass
