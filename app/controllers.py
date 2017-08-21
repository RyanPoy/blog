#coding: utf8
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, connection
from tornado.util import unicode_type
from pprint import pprint
import tornado.web
import functools
import settings
from .models import *
from datetime import datetime


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
        return self.request.uri or '/'

    def __before_render_view_or_ajax(self, kwargs):
        if 'recent_articles' not in kwargs:
            kwargs['recent_articles'] = Article.objects.recents(5)
        if 'all_pages' not in kwargs:
            kwargs['all_pages'] = Page.objects.order_by('seq').all()
        if 'all_tags' not in kwargs:
            kwargs['all_tags'] = Tag.objects.all()
        if 'all_links' not in kwargs:
            kwargs['all_links'] = Link.objects.order_by('-seq').all()
        if 'active_css' not in kwargs:
            kwargs['active_css'] = lambda v: 'active' if self.full_uri == v else ''
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
        pagination_objects.count = paginator.count
        return pagination_objects

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With', '').upper() == 'XMLHTTPREQUEST'

    def write_error(self, status_code, *args, **kwargs):
        if settings.DEBUG:
            # from web.py
            # in debug mode, try to send a traceback
            return super(BaseController, self).write_error(status_code, *args, **kwargs)
        else:
            print (status_code)
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


class ArticleListController(BaseController):

    def get(self, tagid):
        tag = Tag.objects.filter(id=tagid).first()
        if not tag: # tag 不存在
            return self.redirect("/blogs")

        articles = self.paginator(Article.objects.order_by('-id').filter(tags__id=tagid))
        return self.render_view('article_list.html', articles=articles)    


class ArticleShowController(BaseController):

    def get(self, _id):
        article = self.get_object_or_404(Article, id=_id)
        return self.render_view('article_show.html', article=article)


class ArchiveController(BaseController):

    def get(self):
        article_dict = {}
        for d in Article.objects.values('id', 'title', 'created_at'):
            year = datetime.strftime(d['created_at'], '%Y')
            a = Article(**d)
            article_dict.setdefault(year, []).append(a)

        article_groups = [ (y, article_dict.get(y)) for y in sorted(article_dict.keys(), reverse=True) ]
        return self.render_view('archive_index.html', article_groups=article_groups)


class ErrorController(BaseController):

    def get(self):
        uri = self.request.uri
        if uri and uri[-1] == '/':
            uri = uri[:-1]
        p = Page.objects.filter(uri=uri).first()
        if not p:
            raise tornado.web.HTTPError(404)
        return self.render_view('page_show.html', page=p)


class RssController(BaseController):

    def get(self):

        articles = [ Article(**a) for a in Article.objects.order_by('-id').values('id', 'title', 'created_at', 'content') ]

        buff = []
        buff.append('<?xml version="1.0" encoding="utf-8" ?>')
        buff.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
        buff.append('    <channel>')
        buff.append('        <title><![CDATA[彭一的博客]]></title>')
        buff.append('        <link>http://pengyi.info</link>')
        buff.append('        <description><![CDATA[彭一的个人网站]]></description>')
        buff.append('        <atom:link href="http://pengyi.info/rss/" rel="self"/>')
        buff.append('        <language>zh-cn</language>')
        if articles:
            buff.append('    <lastBuildDate>%s</lastBuildDate>' % articles[0].created_at)
            for a in articles:
                buff.append('<item>')
                buff.append('    <title><![CDATA[%s]]></title>' % a.title)
                buff.append('    <link>http://pengyi.info/blogs/%s</link>' % a.id)
                buff.append('    <description><![CDATA[%s]]></description>' % a.limit_content(200))
                buff.append('    <guid>http://pengyi.info/blogs/%s</guid>' % a.id)
                buff.append('</item>')
        buff.append('''  </channel>''')
        buff.append('''</rss>''')
        self.write('\n'.join(buff))
        self.set_header("Content-Type", "application/rss+xml")
        return self.finish()

