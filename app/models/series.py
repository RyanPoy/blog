#coding: utf8
import peewee as pw
from .base import *


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
        table_name = 'app_series'

