#coding: utf8
from .base import *


class Page(AbsArticle):
    """ 单页面，直接显示在导航栏上 """
    seq = pw.IntegerField(verbose_name='排序', default=0, index=True)
    uri = pw.CharField(verbose_name='跳转地址', null=False, max_length=255, index=True)

    def validate(self):
        if not self.title:
            self.add_err('title', '名称不能为空')
        if not self.uri:
            self.add_err('uri', '链接地址不能为空')
        if not self.content:
            self.add_err('content', '内容不能为空')
        elif len(self.content) < 4:
            self.add_err('content', '内容长度不能少于4个字')

        if self.is_persistent():
            if Page.get_or_none( (Page.title == self.title) & (Page.id != self.id) ):
                self.add_err('title', '存在同名页面')
            if Page.get_or_none( (Page.uri == self.uri) & (Page.id != self.id) ):
                self.add_err('uri', '存在同链接地址的页面')
        else:
            if Page.get_or_none(Page.title == self.title):
                self.add_err('title', '存在同名页面')
            if Page.get_or_none(Page.uri == self.uri):
                self.add_err('uri', '存在同链接地址的页面')

    class Meta:
        table_name = 'app_page'
