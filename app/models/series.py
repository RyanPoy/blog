#coding: utf8
import peewee as pw
from .base import *


class Series(BaseModel):
    name = pw.CharField(verbose_name='名称', max_length=255)
    seq = pw.IntegerField(verbose_name='排序', default=0, index=True)

    def validate(self):
        if not self.name:
            self.add_err('name', '名称不能为空')

        if self.is_persistent():
            if Series.get_or_none( (Series.name == self.name) & (Series.id != self.id) ):
                self.add_err('name', '存在同名系列')
        else:
            if Series.get_or_none(Series.name == self.name):
                self.add_err('name', '存在同名系列')

    def remove(self):
        Article.update(series_id=None).where(Article.series_id == _id).execute()
        super().remove()

    class Meta:
        table_name = 'app_series'

