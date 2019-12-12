#coding: utf8
import os
import json
import settings
import peewee as pw
import markdown as md
from datetime import datetime
from collections import OrderedDict as odict


db = pw.MySQLDatabase(**settings.db)
atomic = db.atomic


class Errs(object):

    def __init__(self):
        self.errs = odict()

    def add(self, key, value):
        self.errs.setdefault(key, []).append(value)

    def get(self, key):
        return self.errs.get(key, [])

    def is_empty(self):
        return False if len(self.errs) else True

    def first_err(self, key=None):
        if self.is_empty():
            return None
        if key is not None:
            return self.errs(key, None)
        k = list(self.errs.keys())[0]
        return self.errs[k][0]


class BaseModel(pw.Model):

    created_at  = pw.DateTimeField(verbose_name='创建时间', index=True, default=datetime.now)
    updated_at  = pw.DateTimeField(verbose_name='修改时间', index=True, default=datetime.now)
    show        = pw.BooleanField(verbose_name='是否发布', default=True, index=True)

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now
        return super().save(*args, **kwargs)

    def to_json(self):
        return json.dumps(self.to_dict)

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

    def is_persistent(self):
        _id = self.id
        try:
            _id = int(_id)
            if _id <= 0:
                return False
        except ValueError:
            if not _id:
                return False
        return True

    @property
    def errs(self):
        if not hasattr(self, '_errs'):
            self._errs = Errs()
        return self._errs

    def add_err(self, field, msg):
        self.errs.add(field, msg)
        return self

    def first_err(self, key=None):
        return self.errs.first_err(key)

    def is_valid(self):
        self.validate()
        return self.errs.is_empty()

    def validate(self):
        pass

    @classmethod
    def new(cls, **kwargs):
        obj = cls(**kwargs)
        n = datetime.now()
        if 'created_at' not in kwargs:
            obj.created_at = n
        if 'updated_at' not in kwargs:
            obj.updated_at = n
        return obj

    def __to_dict__(self):
        return self.__dict__['__data__']

    def to_dict(self, **out_attrs):
        d = self.__to_dict__()
        for key in ('created_at', 'updated_at', 'created_on', 'updated_on'):
            if key in d:
                d.pop(key)

        d['created_at_str'] = self.created_at_str()
        d['created_on_str'] = self.created_on_str()
        d['updated_at_str'] = self.updated_at_str()
        d['updated_on_str'] = self.updated_on_str()
        if out_attrs:
            d.update(out_attrs)
        return d


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
