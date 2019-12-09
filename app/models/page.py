#coding: utf8
from .base import *


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
