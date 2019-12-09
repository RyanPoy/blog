#coding: utf8
import os
import json
import settings
import peewee as pw
import markdown as md
from datetime import datetime


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
