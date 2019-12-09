#coding: utf8
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .libs import Paginator
from django.db import transaction, connection
from django.db.models import Q
from tornado.util import unicode_type
from pprint import pprint
import tornado.web
import functools
import settings
from .models import *
from datetime import datetime
import json
import re
import app.ui as ui
import math


def toi(v):
    try:
        return int(v)
    except:
        return 0


class BaseController(tornado.web.RequestHandler):

    LOGIN_USER_COOKIE_NAME = 'cu'

    SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS \
                        + ("INDEX", 'LIST', 'SHOW')
    
    def pp(self, obj):
        pprint(obj)

    def initialize(self, *args, **kwargs):
        # if self.request.method.lower() == 'post':
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


class IndexController(BaseController):

    def get(self):
        return self.redirect('/blogs')


class ArticleIndexController(BaseController):

    def get(self):
        articles = self.paginator(Article.select().order_by(Article.id.desc()))
        return self.render_view('article_list.html', articles=articles)


class TagArticleController(BaseController):

    def get(self, tagid):
        tag = Tag.objects.filter(id=tagid).first()
        if not tag: # tag 不存在
            return self.redirect("/blogs")

        articles = self.paginator(Article.objects.order_by('-id').filter(tags__id=tagid))
        return self.render_view('article_list.html', articles=articles)


class SeriesArticleController(BaseController):

    def get(self, series_id):
        series = Series.objects.filter(id=series_id).first()
        if not series: # series 不存在
            return self.redirect("/blogs")

        articles = self.paginator(Article.objects.order_by('-id').filter(series__id=series_id))
        return self.render_view('article_list.html', articles=articles)


class ArticleShowController(BaseController):

    def get(self, _id):
        article = self.get_object_or_404(Article, id=_id)
        article.view_number += 1
        article.save()

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

    show_post_p = re.compile(r'^/post/(?P<pid>\d+)[/]?')
    list_tag_p = re.compile(r'^/tag/(?P<name>.+)[/]?$')
    feed_p = re.compile(r'^/feed[/]?$')

    def match_old_url_mode(self, uri):
        """ 为了兼容旧版的格式
        """
        r = self.show_post_p.match(uri)
        if r:
            pid = r.groupdict().get('pid')
            return '/blogs/%s' % pid

        r = self.list_tag_p.match(uri)
        if r:
            name = r.groupdict().get('name')
            tag = Tag.objects.filter(name=name).first()
            if tag:
                return '/blogs/tags/%s' % tag.id

        r = self.feed_p.match(uri)
        if r:
            return '/rss'

        return None

    def get(self):
        uri = self.request.uri
        if uri and uri[-1] == '/':
            uri = uri[:-1]
        
        r = self.match_old_url_mode(uri)
        if r:
            return self.redirect(r)

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

        self.set_header("Content-Type", "application/rss+xml; charset=utf-8")
        self.write('\n'.join(buff))

        return self.finish()


#####################################################
# API 
#####################################################
class ApiLeftNavController(BaseController):

    def get(self):
        # op = self.current_user
        menus = [ m for m in ui.left_menus() ]
        return self.end(data={ 'menus': menus } )


class ApiTagController(BaseController):

    def get(self):
        return self.end(data={ 
            'tags': [ t.to_dict() for t in Tag.objects.all() ]
        })

    @transaction.atomic
    def post(self):
        d = json.loads(self.request.body)
        name = d.get('name', '')
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Tag.objects.filter(name=name).first():
            return self.end(code=-1, err_str='存在同名tag')

        t = Tag(name=name)
        t.save()
        return self.end(data={
            'tag': t.to_dict()
        })

    @transaction.atomic
    def put(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_tag = self.get_object_or_404(Tag, id=_id)
        
        name = t.get('name', '')
        
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Tag.objects.filter(name=name).filter(~Q(id=_id)).first():
            return self.end(code=-1, err_str='存在同名tag')
        
        db_tag.name = t['name']
        db_tag.save()
        return self.end(data={
            'tag': db_tag.to_dict()
        })

    @transaction.atomic
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_tag = self.get_object_or_404(Tag, id=_id)
        if db_tag:
            db_tag.delete()
            return self.end(data=db_tag.to_dict())

            
class ApiLinkController(BaseController):

    def get(self):
        return self.end(data={ 
            'links': [ t.to_dict() for t in Link.objects.all() ]
        })

    @transaction.atomic
    def post(self):
        d = json.loads(self.request.body)
        name = d.get('name', '')
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Link.objects.filter(name=name).first():
            return self.end(code=-1, err_str='存在同名友链')

        url = d.get('url', '')
        if not url:
            return self.end(code=-1, err_str='链接地址不能为空')
        if Link.objects.filter(url=url).first():
            return self.end(code=-1, err_str='存在同名友链')

        l = Link(name=name, url=url, seq=toi(d.get('seq', '0')))
        l.save()
        return self.end(data={
            'link': l.to_dict()
        })

    @transaction.atomic
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')
        db_link = self.get_object_or_404(Link, id=_id)
        
        name = d.get('name', '')
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Link.objects.filter(name=name).filter(~Q(id=_id)).first():
            return self.end(code=-1, err_str='存在同名友链')

        url = d.get('url', '')
        if not url:
            return self.end(code=-1, err_str='链接地址不能为空')
        if Link.objects.filter(url=url).filter(~Q(id=_id)).first():
            return self.end(code=-1, err_str='存在同名友链')

        db_link.name = d['name']
        db_link.url = d['url']
        db_link.seq = toi(d.get('seq', '0'))

        db_link.save()
        return self.end(data={
            'link': db_link.to_dict()
        })

    @transaction.atomic
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_link = self.get_object_or_404(Link, id=_id)
        if db_link:
            db_link.delete()
            return self.end(data=db_link.to_dict())


class ApiSeriesController(BaseController):

    def get(self):
        return self.end(data={ 
            'series': [ t.to_dict() for t in Series.objects.all() ]
        })

    @transaction.atomic
    def post(self):
        d = json.loads(self.request.body)
        name = d.get('name', '')
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Series.objects.filter(name=name).first():
            return self.end(code=-1, err_str='存在同名系列')

        s = Series(name=name, seq=toi(d.get('seq', '0')))
        s.save()
        return self.end(data={
            'series': s.to_dict()
        })

    @transaction.atomic
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')
        db_series = self.get_object_or_404(Series, id=_id)
        
        name = d.get('name', '')
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Series.objects.filter(name=name).filter(~Q(id=_id)).first():
            return self.end(code=-1, err_str='存在同名系列')

        db_series.name = d['name']
        db_series.seq = toi(d.get('seq', '0'))

        db_series.save()
        return self.end(data={
            'link': db_series.to_dict()
        })

    @transaction.atomic
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_series = self.get_object_or_404(Series, id=_id)
        if db_series:
            db_series.delete()
            return self.end(data=db_series.to_dict())


class ApiImageController(BaseController):

    SUPPORT_IMAGE_TYPES = ('image/jpg', 'image/png', 'image/gif', 'image/jpeg')
    SUPPORT_IMAGE_MAX_SIZE = 500<<10

    def get(self):
        return self.end(data={ 
            'images': [ t.to_dict() for t in Image.objects.all() ]
        })

    @transaction.atomic
    def post(self):
        if 'images' not in self.request.files:
            return self.end(code=-1, err_str='请上传图片')

        for f in self.request.files['images']:
            fname, content_type, fbody = f['filename'], f['content_type'], f['body']
            if content_type.lower() not in self.SUPPORT_IMAGE_TYPES:
                return self.end(code=-1, err_str="只支持JPG、PNG、GIF 图片格式")
            if len(fbody) > self.SUPPORT_IMAGE_MAX_SIZE:
                return self.end(code=-1, err_str="最大支持512KB")
            img = Image.my_save(fname, fbody)
            return self.end(data={
                'image': img.to_dict()
            })

    @transaction.atomic
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_image = self.get_object_or_404(Image, id=_id)
        if db_image:
            db_image.delete()
            try:
                os.remove(db_image.abspath)
            except:
                raise
            return self.end(data=db_image.to_dict())


class ApiPageController(BaseController):

    def get(self):
        return self.end(data={ 
            'pages': [ p.to_dict() for p in Page.objects.all() ]
        })

    @transaction.atomic
    def post(self):
        d = json.loads(self.request.body)
        title = d.get('title', '')
        if not title:
            return self.end(code=-1, err_str='名称不能为空')
        if Page.objects.filter(title=title).first():
            return self.end(code=-1, err_str='存在同名页面')

        uri = d.get('uri', '')
        if not uri:
            return self.end(code=-1, err_str='链接地址不能为空')

        content = d.get('content', '')
        if not content:
            return self.end(code=-1, err_str='内容不能为空')
        if len(content) < 4:
            return self.end(code=-1, err_str='正文长度不能少于4个字')

        p = Page(title=title, seq=toi(d.get('seq', '0')), content=content, uri=uri)
        p.save()
        return self.end(data={
            'page': p.to_dict()
        })

    @transaction.atomic
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')
        db_page = self.get_object_or_404(Page, id=_id)
        
        title = d.get('title', '')
        if not title:
            return self.end(code=-1, err_str='名称不能为空')
        if Page.objects.filter(title=title).filter(~Q(id=_id)).first():
            return self.end(code=-1, err_str='存在同名页面')

        content = d.get('content', '')
        if not content:
            return self.end(code=-1, err_str='内容不能为空')
        if len(content) < 4:
            return self.end(code=-1, err_str='正文长度不能少于4个字')

        uri = d.get('uri', '')
        if not uri:
            return self.end(code=-1, err_str='链接地址不能为空')

        db_page.title = title
        db_page.uri = uri
        db_page.seq = toi(d.get('seq', '0'))
        db_page.content = content
        db_page.save()
        return self.end(data={
            'page': db_page.to_dict()
        })

    @transaction.atomic
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_page = self.get_object_or_404(Page, id=_id)
        if db_page:
            db_page.delete()
            return self.end(data=db_page.to_dict())


class ApiArticleController(BaseController):

    def get(self):
        return self.end(data={ 
            'articles': [ a.to_dict() for a in Article.objects.order_by('-id').all() ]
        })

    @transaction.atomic
    def post(self):
        d = json.loads(self.request.body)

        title = d.get('title', '')
        if not title:
            return self.end(code=-1, err_str='请填写标题')
        if Article.objects.filter(title=title).first():
            return self.end(code=-1, err_str='存在同标题文章')

        view_number = toi(d.get('view_number', 0))
        if view_number < 0:
            view_number = 0

        tag_ids = d.get('tag_ids', [])
        if tag_ids: # 去除无效的 tag
            tag_ids = [ t for t in Tag.objects.filter(id__in=tag_ids).all() ]

        keywords = d.get('keywords', '').strip()
        series = d.get('series_id', 0)
        if series:
            series = Series.objects.filter(id=series).first()
            if not series:
                return self.end(code=-1, err_str='请选择正确的系列')

        content = d.get('content', '').strip()
        if not content:
            return self.end(code=-1, err_str='内容不能为空')
        if len(content) < 4:
            return self.end(code=-1, err_str='正文长度不能少于4个字')

        a = Article(title=title, content=content, keywords=keywords, view_number=view_number)
        if series:
            a.series = series
        # for t in tag_ids:
        a.save()
        a.tags.add(*tag_ids)
        a.save()

        return self.end(data={
            'article': a.to_dict()
        })

    @transaction.atomic
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')

        db_article = self.get_object_or_404(Article, id=_id)

        title = d.get('title', '')
        if not title:
            return self.end(code=-1, err_str='请填写标题')
        if Article.objects.filter(title=title).filter(~Q(id=db_article.id)).first():
            return self.end(code=-1, err_str='存在同标题文章')

        view_number = toi(d.get('view_number', 0))
        if view_number < 0:
            view_number = 0

        tag_ids = d.get('tag_ids', [])
        if tag_ids: # 去除无效的 tag
            tag_ids = [ t for t in Tag.objects.filter(id__in=tag_ids).all() ]

        keywords = d.get('keywords', '').strip()
        series = d.get('series_id', 0)
        if series:
            series = Series.objects.filter(id=series).first()
            if not series:
                return self.end(code=-1, err_str='请选择正确的系列')

        content = d.get('content', '').strip()
        if not content:
            return self.end(code=-1, err_str='内容不能为空')
        if len(content) < 4:
            return self.end(code=-1, err_str='正文长度不能少于4个字')

        db_article.title = title
        db_article.content = content
        db_article.keywords = keywords
        db_article.view_number = view_number
        if series:
            db_article.series = series

        if tag_ids:
            pretty_tagid_tags_mapping = { t.id:t for t in tag_ids }

            db_tags = db_article.tags
            db_tagid_tags_mapping = { t.id:t for t in db_tags}

            should_add_tags = [ t for t in tag_ids if t.id not in db_tagid_tags_mapping ]
            should_delete_tags = [ t for t in db_tags if t.id not in pretty_tagid_tags_mapping ]
            
            db_article.tags.add(*should_add_tags)
            db_article.tags.remove(*should_delete_tags)

        db_article.save()
        return self.end(data={
            'article': db_article.to_dict()
        })
    
    @transaction.atomic
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_article = self.get_object_or_404(Article, id=_id)
        if db_article:
            db_article.delete()
            return self.end(data=db_article.to_dict())


class ApiSigninController(BaseController):

    def post(self):
        d = json.loads(self.request.body)

        signinname = d.get('signinname', '').strip()
        if not signinname:
            return self.end(code=-1, err_str='请填写登录名')

        password = d.get('password', '')
        if not password:
            return self.end(code=-1, err_str='请填写密码')

        u = User.objects.filter(signinname=signinname).filter(password=password).first()
        print (signinname, password)
        if not u:
            return self.end(code=-1, err_str='用户名或密码错误')

        self.set_user_to_cookie(u)
        return self.end()

    def delete(self):
        self.rm_user_cookie()
        return self.end()
