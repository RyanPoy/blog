#coding: utf8
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, connection
from tornado.util import unicode_type
from pprint import pprint
import tornado.web
import functools
import settings
from .models import *


class BaseController(tornado.web.RequestHandler):

    SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS \
                        + ("INDEX", 'LIST', 'SHOW')

    def pp(self, obj):
        pprint(obj)

    def initialize(self, *args, **kwargs):
        # if self.request.method.lower() == 'post':
        self.request.method = self.get_argument('_method', '').upper() or self.request.method
        self.has_except = False

    def prepare(self):
        pass

    @property
    def nav_uri(self):
        return self.request.uri.split('/')[1] or '/'

    @property
    def full_uri(self):
        print '#'*20, self.request.uri or '/'
        return self.request.uri or '/'

    def __before_render_view_or_ajax(self, kwargs):
        # from app.article.models import ArticleCategory
        # if 'l1_product_cates' not in kwargs: kwargs['l1_product_cates'] = l1_product_cates
        # if 'rmb_of' not in kwargs: kwargs['rmb_of'] = rmb_of
        # if 'line_of_cates_for_view' not in kwargs: kwargs['line_of_cates_for_view'] = line_of_cates_for_view
        # if 'pretty_date' not in kwargs: kwargs['pretty_date'] = pretty_date_for_view
        # if 'limit' not in kwargs:       kwargs['limit'] = limit
        # if 'format' not in kwargs:      kwargs['format'] = format
        # if 'image_path' not in kwargs:  kwargs['image_path'] = image_path
        # if 'active_css' not in kwargs:  kwargs['active_css'] = functools.partial(active_css, self.nav_uri)
        # if 'left_active_css' not in kwargs:  kwargs['left_active_css'] = functools.partial(active_css, self.full_uri)
        # if 'error_css' not in kwargs:  kwargs['error_css'] = error_css
        # if 'tip_msg' not in kwargs:  kwargs['tip_msg'] = tip_msg
        # if 'join_str' not in kwargs:  kwargs['join_str'] = join_str
        # # if '_article_cates_level1' not in kwargs: kwargs['_article_cates_level1'] = ArticleCategory.level1()
        # if 'set_query_para' not in kwargs: kwargs['set_query_para'] = set_query_para
        # if 'form_for' not in kwargs: kwargs['form_for'] = form_helper.form_for
        # for key in dir(form_helper.tags):
        #     if key.endswith('_tag') and key not in kwargs:
        #         kwargs[key] = getattr(form_helper.tags, key)

        return self
    
    def render_view(self, template_name, **kwargs):
        self.__before_render_view_or_ajax(kwargs)
        return self.render(template_name, **kwargs)

    def get_object_or_404(self, clazz, id, related=False):
        try:
            _id = int(id)
            return clazz.objects.select_related().get(pk=_id) if related \
                    else clazz.objects.get(pk=_id)
        except clazz.DoesNotExist:
            raise tornado.web.HTTPError(404)
        except ValueError: # 表示_id不是整形
            raise tornado.web.HTTPError(404)

    def get_object_or_none(self, clazz, id, related=False):
        try:
            return self.get_object_or_404(clazz, id, related)
        except tornado.web.HTTPError:
            return None

    def int_argument(self, k, default=0):
        v = self.get_argument(k, default)
        try:
            return int(v)
        except:
            return default

    def paginator(self, object_list, number_per_page=10, page_num=0):
        if page_num <= 0:
            page_num = self.int_argument('page')
        if page_num <= 0:
            page_num = 1

        paginator = Paginator(object_list, number_per_page)
        try:
            pagination_objects = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pagination_objects = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pagination_objects = paginator.page(paginator.num_pages)

        #如果传入的分页索引大于总分页索引数，则返回最大分页索引数,如果传入的分页索引小于1，返回1
        all_page_nums = pagination_objects.paginator.num_pages
        if page_num > all_page_nums:
            page_num = all_page_nums
        elif page_num < 1:
            page_num = 1
        end_page = page_num + (number_per_page/2)
        start_page = page_num - (number_per_page/2)
        if start_page < 1:
            start_page = 1
        if end_page > all_page_nums:
            end_page = all_page_nums
        return pagination_objects
        # return pagination_objects, start_page, end_page, page_num

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With', '').upper() == 'XMLHTTPREQUEST'

    def write_error(self, status_code, *args, **kwargs):
        if settings.DEBUG:
            # from web.py
            # in debug mode, try to send a traceback
            return super(BaseController, self).write_error(status_code, *args, **kwargs)
        else:
            # print '?'*20, status_code
            if status_code == 500:
                return self.write('sorry, interval server error 500')
            if status_code == 404:
                return self.write('sorry, resource not found!')
            if status_code == 403:
                return self.write('sorry, request forbidden!')
            return self.write('sorry, unknow error!')


class IndexController(BaseController):

    def get(self):
        return self.redirect('/blogs')


class ArticleIndexController(BaseController):

    def get(self):
        articles = self.paginator(Article.objects.order_by('-id'))
        return self.render_view('article_list.html', articles=articles)


class ArticleShowController(BaseController):

    def get(self, _id):
        article = self.get_object_or_404(Article, id=_id)
        return self.render_view('article_show.html', article=article)

