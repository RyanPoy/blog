#coding: utf8
import json
import settings
from urllib import request
from collections import OrderedDict
from urllib.parse import urlparse, urljoin, urlencode


def get_oauth2_url(state='STATE#weibo_redirect'):
    """https://api.weibo.com/oauth2/authorize?
            client_id=client_id
            &response_type=code
            &redirect_uri=http%3A//www.ryanpoy.com/login-weibo
    """
    base_url = 'https://api.weibo.com/oauth2/authorize'
    params = urlencode(OrderedDict([
        ('client_id', settings.weibo_app_key),
        ('redirect_uri', settings.weibo_login_callback),
        ('response_type', 'code'),
        ('state', state)
    ]))
    url = "{0}?{1}".format(base_url, params)
    return url


def get_userid_and_accesstoken(code):
    """ https://api.weibo.com/oauth2/access_token
    """
    base_url = "https://api.weibo.com/oauth2/access_token"
    params = urlencode(OrderedDict([
        ('client_id', settings.weibo_app_key),
        ('client_secret', settings.weibo_app_secret),
        ('grant_type', 'authorization_code'),
        ('code', code),
        ('redirect_uri', 'http://www.ryanpoy.com/signin/weibo/callback'),
    ])).encode("UTF8")
    response = request.urlopen(base_url, params).read()
    # response 格式：
    # {
    #    "access_token": "ACCESS_TOKEN",
    #    "expires_in": 1234,
    #    "remind_in":"798114",
    #    "uid":"12341234"
    # }
    d = json.loads(response)
    return d.get('uid', ''), d.get('access_token', '')


def get_user_detail(uid, access_token):
    base_url = "https://api.weibo.com/2/users/show.json"
    params = urlencode(OrderedDict([
        ('access_token', access_token),
        ('uid', uid)
    ]))
    url = "{0}?{1}".format(base_url, params)
    response = request.urlopen(url).read()
    return json.loads(response)
