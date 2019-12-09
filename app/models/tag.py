#coding: utf8
from .base import *


class Tag(BaseModel):
    name = pw.CharField(verbose_name='名字', max_length=255, index=True, null=False, unique=True)
    article_number = pw.IntegerField(verbose_name='文章数量', default=0)

    def to_dict(self):
        d = super().to_dict()
        d['name'] = self.name
        d['article_number'] = self.article_number
        return d

    def __str__(self):
        return self.name

    class Meta:
        table_name = 'app_tag'

