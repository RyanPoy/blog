#coding: utf8
import os
import json
import settings
import peewee as pw
import markdown as md
from datetime import datetime, date
from settings import MEDIA_ROOT
from collections import namedtuple


db = pw.MySQLDatabase(**settings.db)
atomic = db.atomic


class BaseModel(pw.Model):

    created_at  = pw.DateTimeField(verbose_name='创建时间', index=True, default=datetime.now)
    updated_at  = pw.DateTimeField(verbose_name='修改时间', index=True, default=datetime.now)
    show        = pw.BooleanField(verbose_name='是否发布', default=True, index=True)

    class Meta:
        database = db

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at_str(),
            'updated_at': self.updated_at_str(),
            'show': self.show
        }

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now
        return super().save(*args, **kwargs)

    def to_json(self):
        return json.dumps(self.to_dict)

    @classmethod
    def get_table_name(cls):
        return cls.objects.model._meta.db_table

    def created_at_str(self, fmt='%Y-%m-%d %H:%M:%S'):
        return datetime.strftime(self.created_at, fmt) if self.created_at else ''

    def created_on_str(self, fmt='%Y-%m-%d'):
        dt = getattr(self, 'created_on', None) or self.created_at
        return datetime.strftime(dt, fmt) if dt else ''

    def updated_on_str(self, fmt='%Y-%m-%d'):
        dt = getattr(self, 'updated_on', None) or self.updated_at
        return datetime.strftime(dt, fmt) if dt else ''

    def updated_at_str(self, fmt='%Y-%m-%d %H:%M:%S'):
        return datetime.strftime(self.updated_at, fmt) if self.updated_at else ''

    @property
    def created_year_for_view(self):
        return datetime.strftime(self.created_at, '%Y年') if self.created_at else ''

    @property
    def created_month_for_view(self):
        return datetime.strftime(self.created_at, '%m月') if self.created_at else ''

    @property
    def created_day_for_view(self):
        return datetime.strftime(self.created_at, '%d') if self.created_at else ''


class Tag(BaseModel):
    name = pw.CharField(verbose_name='名字', max_length=255, index=True, null=False, unique=True)
    article_number = pw.IntegerField(verbose_name='文章数量', default=0)
    
    # @clasmethod
    # def reset_article_number(cls, *args, **kwargs):
    #     '''重新统计每个tag对应的文章数，删除空标签'''
    #     for i in cls.select().where(*args, **kwargs):
    #         i.article_number = i.post_set.count()
    #         if i.article_number <= 0:
    #             i.delete().execute()
    #         else:
    #             i.save()

    # def decr_article_number(self, ids, delete_isolate=True):
    #     '''文章数减1'''
    #     assert all(map(lambda i:isinstance(i, int), ids))
    #     self.extra(where=['id in (%s)' % ','.join(map(str, ids))]).update(article_number=models.F('article_number') - 1)
    #     if delete_isolate:
    #         # 删除没有和文章关联的标签
    #         self.filter(article_number__lte=0).delete().execute()

    def to_dict(self):
        d = super().to_dict()
        d['name'] = self.name
        d['article_number'] = self.article_number
        return d

    def __str__(self):
        return self.name

    class Meta:
        table_name = 'app_tag'


class Image(BaseModel):

    pic = pw.CharField(verbose_name='图片', max_length=255, null=False)

    @property
    def abspath(self):
        return os.path.join(MEDIA_ROOT, self.pic.name)

    @classmethod
    def my_save(cls, fname, fbody):
        save_name = fname
        while True:
            print(save_name)
            if Image.objects.filter(pic=save_name).first():
                save_name = '{}(1)'.format(save_name)
            else:
                break
        save_path = os.path.join(MEDIA_ROOT, save_name)
        with open(save_path, 'wb') as f:
            f.write(fbody)

        obj = cls()
        obj.pic.name = save_name
        obj.save()
        return obj

    @property
    def size(self):
        return '%.2f KB' % (self.pic.size / 1024.0)

    def to_dict(self):
        d = super().to_dict()
        if os.path.exists(self.abspath):
            d['name'] = self.pic.name
            d['size'] = self.size
            d['url'] = self.pic.url
        else:
            d['name'] = ''
            d['size'] = 0
            d['url'] = ''
        return d

    def __str__(self):
        return self.pic.name

    class Meta:
        table_name = 'app_image'


class Series(BaseModel):
    name = pw.CharField(verbose_name='名称', max_length=255)
    seq = pw.IntegerField(verbose_name='排序', default=0, index=True)

    def to_dict(self):
        d = super().to_dict()
        d['name'] = self.name
        d['seq'] = self.seq
        return d

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['seq']
        table_name = 'app_series'


class AbsArticle(BaseModel):

    title   = pw.CharField(verbose_name='标题', max_length=255, index=True, unique=True)
    keywords= pw.CharField(verbose_name='关键词', max_length=255, null=True, default='')
    content = pw.TextField(verbose_name='MarkDown内容', null=False, default='')

    def to_dict(self):
        d = super().to_dict()
        d['title'] = self.title
        d['keywords'] = self.keywords
        d['content'] = self.content
        d['limit_content'] = self.limit_content(32)
        return d

    def limit_content(self, n=64):
        content = self.content.replace('\n', '').replace('\r', '')
        return content[:n] if len(content) < n else content[:n] + '...'

    @property
    def html_content(self):
        return md.markdown(self.content, extensions=['markdown.extensions.extra'])


class Article(AbsArticle):
    view_number     = pw.IntegerField(verbose_name='浏览次数', null=False, default=0)
    tags            = pw.ManyToManyField(Tag, backref='articles') # verbose_name='标签'
    series          = pw.ForeignKeyField(Series, verbose_name='系列', backref="articles", null=True, related_name='series_id', on_delete=False)

    def to_dict(self):
        d = super().to_dict()
        d['view_number'] = self.view_number
        d['tag_names_str'] = self.tag_names_str
        d['tag_ids'] = self.tag_ids
        d['series'] = self.series.to_dict() if self.series else {}
        d['series_id'] = self.series.id if self.series else ''
        return d

    @classmethod
    def recents(cls, num):
        return cls.select().order_by(cls.id.desc()).limit(5)

    def same_series(self):
        return Article.select().where(Article.series_id == self.series_id)

    @property
    def tag_names_str(self):
        if self.id:
            return '，'.join([ t.name for t in self.tags ])
        return ''

    @property
    def tag_ids(self):
        if self.id:
            return [ t.id for t in self.tags ]
        return []

    def __str__(self):
        return self.title

    class Meta:
        table_name = 'app_article'


class Page(AbsArticle):
    """ 单页面，直接显示在导航栏上 """
    seq = pw.IntegerField(verbose_name='排序', default=0, index=True)
    uri = pw.CharField(verbose_name='跳转地址', null=False, max_length=255, index=True)

    def to_dict(self):
        d = super().to_dict()
        d['seq'] = self.seq
        d['uri'] = self.uri
        return d

    class Meta:
        table_name = 'app_page'


class Link(BaseModel):
    name = pw.CharField(verbose_name='名称', max_length=255)
    url = pw.CharField(verbose_name='链接地址', max_length=255)
    seq = pw.IntegerField(verbose_name='排序', default=0, index=True)

    def to_dict(self):
        d = super().to_dict()
        d['name'] = self.name
        d['url'] = self.url
        d['seq'] = self.seq
        return d

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['seq']
        table_name = 'app_link'


class User(BaseModel):

    ROLES = namedtuple('Roles', ['ADMIN', 'NORMAL'])._make([10000, 100])

    signinname = pw.CharField(verbose_name='登录名', max_length=255, null=False, index=True)
    username   = pw.CharField(verbose_name='用户名', max_length=255, null=False)
    password   = pw.CharField(verbose_name='密码', max_length=255, null=False, index=True)
    role       = pw.IntegerField(verbose_name='权限', default=ROLES.NORMAL, null=False, index=True)

    def to_cookie_str(self):
        return '%s|%s|%s' % (self.signinname, self.username, self.id)

    @classmethod
    def from_cookie_str(cls, cookie_str):
        if not cookie_str or not cookie_str.strip():
            return None

        vs = cookie_str.strip().split('|')
        if len(vs) != 3:
            return None
        return cls.get_or_none(
            (cls.id == vs[2]) & (cls.signinname == vs[0]) & (cls.username == vs[1])

        )

    def __str__(self):
        return self.username

    class Meta:
        table_name = 'app_user'
