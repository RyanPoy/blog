#coding: utf8
import uuid
import tornado.web
from uuid import uuid4
from app.models import *
from . import BaseController
from collections import OrderedDict as odict


class Index(BaseController):

    def get(self):
        return self.redirect('/blogs')


class ArticleIndex(BaseController):

    def get(self):
        articles = self.paginator(Article.select().order_by(Article.id.desc()))
        return self.render_view('article_list.html', articles=articles)


class ArticleShow(BaseController):

    def get(self, _id):
        article = self.get_object_or_404(Article, id=_id)
        article.view_number += 1
        article.save()

        return self.render_view('article_show.html', article=article)


class TagArticle(BaseController):

    def get(self, tagid):
        tag = Tag.get_or_none(Tag.id == tagid)
        if not tag: # tag 不存在
            return self.redirect("/blogs")

        through_table = Article.tags.get_through_model()
        articles = self.paginator(
            Article.select().join(through_table).where(through_table.tag_id == tagid).order_by(Article.id.desc())
        )
        return self.render_view('article_list.html', articles=articles)


class SeriesArticle(BaseController):

    def get(self, series_id):
        series = Series.get_or_none(Series.id == series_id)
        if not series: # series 不存在
            return self.redirect("/blogs")

        articles = self.paginator(
            Article.select().join(Series).where(Article.series_id == series_id).order_by(Article.id.desc())
        )
        return self.render_view('article_list.html', articles=articles)


class Archive(BaseController):

    def get(self):
        article_dict = odict()
        articles = Article.select().order_by(Article.created_at.desc())
        for a in articles:
            year = datetime.strftime(a.created_at, '%Y')
            month = datetime.strftime(a.created_at, '%m')
            article_dict.setdefault(year, odict()).setdefault(month, []).append(a)

        return self.render_view('archive_index.html', article_groups=article_dict, articles_number=len(articles))


class Error(BaseController):

    def get(self):
        uri = self.request.uri
        if uri and uri[-1] == '/':
            uri = uri[:-1]

        p = Page.get_or_none(Page.uri == uri)
        if not p:
            raise tornado.web.HTTPError(404)
        return self.render_view('page_show.html', page=p)


class Rss(BaseController):

    def get(self):

        articles = Article.select().order_by(Article.id.desc())

        buff = []
        buff.append('<?xml version="1.0" encoding="utf-8" ?>')
        buff.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
        buff.append('    <channel>')
        buff.append('        <title><![CDATA[彭一的博客]]></title>')
        buff.append('        <link>http://www.ryanpoy.com</link>')
        buff.append('        <description><![CDATA[彭一的个人网站]]></description>')
        buff.append('        <atom:link href="http://www.ryanpoy.com/rss/" rel="self"/>')
        buff.append('        <language>zh-cn</language>')
        if articles:
            buff.append('    <lastBuildDate>%s</lastBuildDate>' % articles[0].created_at)
            for a in articles:
                buff.append('<item>')
                buff.append('    <title><![CDATA[%s]]></title>' % a.title)
                buff.append('    <link>http://www.ryanpoy.com/blogs/%s</link>' % a.id)
                buff.append('    <description><![CDATA[%s]]></description>' % a.limit_content(200))
                buff.append('    <guid>http://www.ryanpoy.com/blogs/%s</guid>' % a.id)
                buff.append('</item>')
        buff.append('''  </channel>''')
        buff.append('''</rss>''')

        self.set_header("Content-Type", "application/rss+xml; charset=utf-8")
        self.write('\n'.join(buff))

        return self.finish()
