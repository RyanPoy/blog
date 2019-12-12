#coding: utf8
from app.controllers import BaseController
from app.models import *
from app.libs import *
from app import ui


class LeftNavController(BaseController):

    def get(self):
        # op = self.current_user
        menus = [ m for m in ui.left_menus() ]
        return self.end(data={ 'menus': menus } )

