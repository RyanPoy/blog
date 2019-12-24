#coding: utf8
import peewee as pw
from .base import *
from .user import User


class Commend(BaseModel):

    user    = pw.ForeignKeyField(User, verbose_name="用户", backref="commends", null=False, on_deleted=True)
    content = pw.CharField(verbose_name="内容", max_length=200, null=False, default="")
    parent  = pw.ForeignKeyField('self', backref="children", on_deleted=True, null=True)

    
    class Meta:
        table_name = 'commends'
