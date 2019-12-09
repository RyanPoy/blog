#coding: utf8
from .base import *
from .tag import *
from .series import *


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
