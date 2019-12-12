#coding: utf8
from app.controllers import BaseController
from app.models import *
from app.libs import *


class LinkController(BaseController):

    def get(self):
        return self.end(data={ 
            'links': [ t.to_dict() for t in Link.select() ]
        })

    @atomic()
    def post(self):
        d = json.loads(self.request.body)
        link = Link.new(
            name=d.get('name', ''), 
            url=d.get('url', ''), 
            seq=toi(d.get('seq', '0'))
        )
        if not link.is_valid():
            return self.end(code=-1, err_str=link.first_err())

        link.save()
        return self.end(data={
            'link': link.to_dict()
        })

    @atomic()
    def put(self):
        d = json.loads(self.request.body)
        link = self.get_object_or_404(Link, id=d.get('id', ''))
        link.name = d.get('name', '')
        link.url = d.get('url', '')
        link.seq = toi(d.get('seq', '0'))

        if not link.is_valid():
            return self.end(code=-1, err_str=link.first_err())
        
        link.save()
        return self.end(data={
            'link': link.to_dict()
        })

    @atomic()
    def delete(self):
        d = json.loads(self.request.body)
        link = self.get_object_or_404(Link, id=d.get('id', ''))
        link.remove()
        return self.end(data=link.to_dict())
