#coding: utf8
import settings
import tornado.web
from app.libs import *
from app.models import *
from pprint import pprint


class BaseController(tornado.web.RequestHandler):

    LOGIN_USER_COOKIE_NAME = 'cu'

    SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS \
                        + ("INDEX", 'LIST', 'SHOW')
    
    def pp(self, obj):
        pprint(obj)

    def initialize(self, *args, **kwargs):
        self.request.method = self.get_argument('_method', '').upper() or self.request.method
        self.has_except = False
        self.set_default_headers()

    def prepare(self):
        uri = self.request.uri
        if uri.startswith('/api/') and uri not in ('/api/signin', '/api/signin/') and not self.current_user:
            raise tornado.web.HTTPError(401)

    def set_user_to_cookie(self, user):
        self.set_secure_cookie(self.LOGIN_USER_COOKIE_NAME, user.to_cookie_str(), expires_days=1)
        return self

    def rm_user_cookie(self):
        self.clear_cookie(self.LOGIN_USER_COOKIE_NAME)
        return self

    def get_current_user(self):
        cookie_str = self.get_secure_cookie(self.LOGIN_USER_COOKIE_NAME)
        cookie_str = cookie_str.decode("UTF8") if cookie_str else ''

        u = User.from_cookie_str(cookie_str)
        if u:
            self.set_user_to_cookie(u)
        return u

    @property
    def nav_uri(self):
        return self.request.uri.split('/')[1] or '/'

    @property
    def full_uri(self):
        return self.request.uri or '/'

    def __before_render_view_or_ajax(self, kwargs):
        if 'recent_articles' not in kwargs:
            kwargs['recent_articles'] = Article.recents(5)
        if 'all_pages' not in kwargs:
            kwargs['all_pages'] = Page.select().order_by(Page.seq)
        if 'all_tags' not in kwargs:
            kwargs['all_tags'] = Tag.select()
        if 'all_series' not in kwargs:
            kwargs['all_series'] = Series.select().order_by(Series.seq)
        if 'all_links' not in kwargs:
            kwargs['all_links'] = Link.select().order_by(Link.seq.desc())
        if 'active_css' not in kwargs:
            kwargs['active_css'] = lambda v: 'active' if self.full_uri == v else ''
        if 'chang_yan' not in kwargs:
            kwargs['chang_yan'] = settings.chang_yan
        return self
    
    def end(self, code=0, err_str='', data={}):
        return self.finish(json.dumps({
            'code': code,
            'err_str': err_str,
            'data': data
        }))

    def render_view(self, template_name, **kwargs):
        self.__before_render_view_or_ajax(kwargs)
        return self.render(template_name, **kwargs)

    def get_object_or_404(self, clazz, id, related=False):
        obj = self.get_object_or_none(clazz, id)
        if obj:
            return obj
        raise tornado.web.HTTPError(404)

    def get_object_or_none(self, clazz, id, related=False):
        try:
            _id = int(id)
        except ValueError:
            _id = 0
        return clazz.get_or_none(clazz.id == _id)

    def int_argument(self, k, default=0):
        v = self.get_argument(k, default)
        try:
            return int(v)
        except:
            return default

    def paginator(self, objects_list, number_per_page=10, page_num=0):
        if page_num <= 0:
            page_num = self.int_argument('page')
        if page_num <= 0:
            page_num = 1
        return Paginator(objects_list, number_per_page).page(page_num)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with,authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST,GET,PUT,DELETE,OPTIONS')
        self.set_header('Access-Control-Allow-Headers:x-requested-with', 'content-type')

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With', '').upper() == 'XMLHTTPREQUEST'

    def finish(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        super().finish(*args, **kwargs)

    def write_error(self, status_code, *args, **kwargs):
        if settings.DEBUG:
            # from web.py
            # in debug mode, try to send a traceback
            return super().write_error(status_code, *args, **kwargs)
        else:
            print (status_code)
            if status_code == 500:
                return self.write('sorry, interval server error 500')
            if status_code == 404:
                return self.write('sorry, resource not found!')
            if status_code == 403:
                return self.write('sorry, request forbidden!')
            return self.write('sorry, unknow error!')