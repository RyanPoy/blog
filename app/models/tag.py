#coding: utf8
import peewee as pw
from .base import *


class Tag(BaseModel):
    name = pw.CharField(verbose_name='名字', max_length=255, index=True, null=False, unique=True)
    article_number = pw.IntegerField(verbose_name='文章数量', default=0)

    def validate(self):
        if not self.name:
            self.add_err('name', '名称不能为空')

        if self.is_persistent():            
            if Tag.get_or_none((Tag.name == self.name) & (Tag.id != self.id)):
                self.add_err('name', '存在同名tag')
        else:
            if Tag.get_or_none(Tag.name == self.name):
                self.add_err('name', '存在同名tag')

    class Meta:
        table_name = 'app_tag'
