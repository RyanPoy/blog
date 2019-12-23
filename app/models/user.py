#coding: utf8
from .base import *
from collections import namedtuple


class User(BaseModel):

    ROLES = namedtuple('Roles', ['ADMIN', 'NORMAL'])._make([10000, 100])

    signinname = pw.CharField(verbose_name='登录名', max_length=255, null=False, index=True)
    username   = pw.CharField(verbose_name='用户名', max_length=255, null=False)
    password   = pw.CharField(verbose_name='密码', max_length=255, null=False, index=True)
    avatar_url = pw.CharField(verbose_name='头像', max_length=255, null=False)
    weibo_openid = pw.CharField(verbose_name="微博id", max_length=64, null=True, index=True)
    role       = pw.IntegerField(verbose_name='权限', default=ROLES.NORMAL, null=False, index=True)

    def to_cookie_str(self):
        return '%s|%s|%s' % (self.signinname, self.username, self.id)

    @classmethod
    def from_cookie_str(cls, cookie_str):
        if not cookie_str or not cookie_str.strip():
            return None

        vs = cookie_str.strip().split('|')
        if len(vs) != 3:
            return None

        return cls.get_or_none(
            (cls.id == vs[2]) & (cls.signinname == vs[0]) & (cls.username == vs[1])
        )

    def is_admin(self):
        return str(self.role) == str(self.ROLES.ADMIN)

    def is_normal(self):
        return str(self.role) == str(self.ROLES.NORMAL)

    class Meta:
        table_name = 'users'

