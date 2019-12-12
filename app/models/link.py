#coding: utf8
from .base import *


class Link(BaseModel):
    name = pw.CharField(verbose_name='名称', max_length=255)
    url = pw.CharField(verbose_name='链接地址', max_length=255)
    seq = pw.IntegerField(verbose_name='排序', default=0, index=True)

    def validate(self):
        if not self.name:
            self.add_err('name', '名称不能为空')

        if not self.url:
            self.add_err('name', '链接地址不能为空')

        if self.is_persistent():
            if Link.get_or_none((Link.name == self.name) & (Link.id != self.id)):
                self.add_err('name', '存在同名友链')
            if Link.get_or_none((Link.url == self.url) & (Link.id != self.id)):
                self.add_err('name', '存在同链接地址友链')
        else:
            if Link.get_or_none(Link.name == self.name):
                self.add_err('name', '存在同名友链')
            if Link.get_or_none(Link.url == self.url):
                self.add_err('name', '存在同链接地址友链')

    class Meta:
        table_name = 'links'

