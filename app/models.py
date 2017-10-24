#coding: utf8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from settings import MEDIA_ROOT
import markdown2 as md
import json
import os


# Create your models here.
class BaseModel(models.Model):

    created_at  = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at  = models.DateTimeField('修改时间', auto_now=True, db_index=True)
    show        = models.BooleanField('是否发布', default=True, db_index=True)

    class Meta:
        abstract = True

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at_str(),
            'updated_at': self.updated_at_str(),
            'show': self.show
        }

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


class TagManager(models.Manager):

    def reset_article_number(self, *args, **kwargs):
        '''重新统计每个tag对应的文章数，删除空标签'''
        for i in self.filter(*args, **kwargs):
            i.article_number = i.post_set.count()
            if i.article_number <= 0:
                i.delete()
            else:
                i.save()

    def decr_article_number(self, ids, delete_isolate=True):
        '''文章数减1'''
        assert all(map(lambda i:isinstance(i, int), ids))
        self.extra(where=['id in (%s)' % ','.join(map(str, ids))]).update(article_number=models.F('article_number') - 1)
        if delete_isolate:
            # 删除没有和文章关联的标签
            self.filter(article_number__lte=0).delete()

    def incr_article_number(self, ids):
        '''文章数减1'''
        assert all(map(lambda i:isinstance(i, int), ids))
        self.extra(where=['id in (%s)' % ','.join(map(str, ids))]).update(article_number=models.F('article_number') + 1)


class Tag(BaseModel):
    objects = TagManager()

    name = models.CharField('名字', max_length=255, db_index=True, null=False, unique=True)
    article_number = models.IntegerField('文章数量', default=0)
    
    def to_dict(self):
        d = super().to_dict()
        d['name'] = self.name
        d['article_number'] = self.article_number
        return d

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Image(BaseModel):

    pic = models.ImageField('图片', null=False)

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
        verbose_name = verbose_name_plural = '图片'



class AbsArticle(BaseModel):

    title           = models.CharField('标题', max_length=255, db_index=True, unique=True)
    keywords        = models.CharField('关键词', max_length=255, null=True, default='', editable=False)
    content         = models.TextField('MarkDown内容', null=False, default='')
    author          = models.ForeignKey(User, verbose_name='作者', editable=False, null=True, blank=True)

    def to_dict(self):
        d = super().to_dict()
        d['title'] = self.title
        d['keywords'] = self.keywords
        d['content'] = self.content
        d['author'] = self.author.username if self.author else {}
        return d

    @property
    def html_content(self):
        return md.markdown(self.content)

    class Meta:
        abstract = True


class ArticleManager(models.Manager):

    def recents(self, n):
        return self.order_by('-id').all()[:n+1]


class Article(AbsArticle):
    objects         = ArticleManager()

    view_number     = models.IntegerField('浏览次数', null=False, default=0)
    tags            = models.ManyToManyField(Tag, verbose_name='标签')
    series          = models.ForeignKey('Series', verbose_name='系列', null=True, blank=True, related_name='series_id')

    def to_dict(self):
        d = super().to_dict()
        d['view_number'] = self.view_number
        d['pretty_tags'] = self.pretty_tags
        d['series'] = self.series.to_dict() if self.series else {}
        return d

    @property
    def same_series(self):
        return Article.objects.filter(series=self.series)
        
    @property
    def pretty_tags(self):
        if self.id:
            return '，'.join([ t.name for t in self.tags.all() ])
        return ''

    def limit_content(self, n=64):
        content = self.content.replace('\n', '').replace('\r', '')
        return content[:n] if len(content) < n else content[:n] + '...'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'


class PageManager(models.Manager):

    def sorted(self, *args, **kwargs):
        return self.order_by('seq ASC')

class Page(AbsArticle):
    """ 单页面，直接显示在导航栏上 """
    objects = PageManager()
    seq = models.IntegerField('排序', default=0, db_index=True)
    uri = models.CharField('跳转地址', null=False, max_length=255, db_index=True)

    def to_dict(self):
        d = super().to_dict()
        d['seq'] = self.seq
        d['uri'] = self.uri
        return d

    class Meta:
        verbose_name = verbose_name_plural = '单页面'


class Link(BaseModel):
    name = models.CharField('名称', max_length=255)
    url = models.URLField('链接地址', max_length=255)
    seq = models.IntegerField('排序', default=0, db_index=True)

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
        verbose_name_plural = verbose_name = '链接'


class Series(BaseModel):
    name = models.CharField('名称', max_length=255)
    seq = models.IntegerField('排序', default=0, db_index=True)

    def to_dict(self):
        d = super().to_dict()
        d['name'] = self.name
        d['seq'] = self.seq
        return d

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['seq']
        verbose_name_plural = verbose_name = '系列'

