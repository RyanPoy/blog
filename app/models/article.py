#coding: utf8
from .base import *
from .tag import *
from .series import *


class Article(AbsArticle):

    view_number     = pw.IntegerField(verbose_name='浏览次数', null=False, default=0)
    tags            = pw.ManyToManyField(Tag, backref='articles') # verbose_name='标签'
    series          = pw.ForeignKeyField(Series, verbose_name='系列', backref="articles", null=True, on_delete=False)

    def to_dict(self):
        d = super().to_dict()
        d['tag_names_str'] = self.tag_names_str
        d['tag_ids'] = self.tag_ids
        d['series'] = self.series.to_dict() if self.series_id else {}
        d['series_id'] = self.series.id if self.series_id else ''
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

    def validate(self):
        if not self.title:
            self.add_err('title', '标题不能为空')
        if not self.content:
            self.add_err('uri', '内容不能为空')
        elif len(self.content) < 4:
            self.add_err('uri', '内容长度不能少于4个字')

        if self.is_persistent():
            if Article.get_or_none( (Article.title == self.title) & (Article.id != self.id) ):
                self.add_err('title', '存在相同标题文章')
        else:
            if Article.get_or_none(Article.title == self.title):
                self.add_err('title', '存在相同标题文章')

    def add_tags(self, tag_ids):
        if not tag_ids:
            return self

        tags = Tag.select().where(Tag.id.in_(tag_ids))
        if not tags:
            return self

        self.tags.add(tags)
        for t in tags:
            t.add_article_number_and_save()
        return self

    def clear_tags(self):
        tags = self.tags
        for t in tags:
            t.sub_article_number_and_save()
        tags.clear()

        return self

    def remove_tags(self, tag_ids):
        if not tag_ids:
            return self

        tags = Tag.select().where(Tag.id.in_(tag_ids))
        if not tags:
            return self

        self.tags.remove(tags)
        for t in tags:
            t.sub_article_number_and_save()

        return self

    def update_tags(self, tag_ids):
        if not tag_ids:
            return self.clear_tags()

        tags = Tag.select().where(Tag.id.in_(tag_ids))
        if not tags:
            return self.clear_tags()

        mem_tag_ids = { t.id for t in tags }
        db_tag_ids = { t.id for t in self.tags }

        should_add_tag_ids = [ tid for tid in mem_tag_ids if tid not in db_tag_ids ]
        should_remove_tag_ids = [ tid for tid in db_tag_ids if tid not in mem_tag_ids ]
        
        self.add_tags(should_add_tag_ids)
        self.remove_tags(should_remove_tag_ids)
        return self

    def remove(self):
        self.clear_tags()
        super().remove()

    class Meta:
        table_name = 'articles'
