#coding: utf8
from . import BaseController
from app.models import *
from app.libs import *
import app.ui as ui


class LeftNavController(BaseController):

    def get(self):
        # op = self.current_user
        menus = [ m for m in ui.left_menus() ]
        return self.end(data={ 'menus': menus } )





class SigninController(BaseController):

    def post(self):
        d = json.loads(self.request.body)

        signinname = d.get('signinname', '').strip()
        if not signinname:
            return self.end(code=-1, err_str='请填写登录名')

        password = d.get('password', '')
        if not password:
            return self.end(code=-1, err_str='请填写密码')

        u = User.get_or_none(
            (User.signinname == signinname) & (User.password == password)
        )
        if not u:
            return self.end(code=-1, err_str='用户名或密码错误')

        self.set_user_to_cookie(u)
        return self.end()

    def delete(self):
        self.rm_user_cookie()
        return self.end()
