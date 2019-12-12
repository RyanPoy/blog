#coding: utf8
from app.controllers import BaseController
from app.models import *
from app.libs import *


class PageController(BaseController):

    def get(self):
        return self.end(data={ 
            'pages': [ p.to_dict() for p in Page.select() ]
        })

    @atomic()
    def post(self):
        d = json.loads(self.request.body)
        p = Page.new(
            title=d.get('title', ''), 
            seq=toi(d.get('seq', '0')), 
            uri=d.get('uri', ''),
            content=d.get('content', ''),
        )
        if not p.is_valid():
            return self.end(code=-1, err_str=p.first_err())

        p.save()
        return self.end(data={
            'page': p.to_dict()
        })

    @atomic()
    def put(self):
        d = json.loads(self.request.body)
        p = self.get_object_or_404(Page, id=d.get('id', ''))
        p.title = d.get('title', '')
        p.seq = toi(d.get('seq', '0'))
        p.uri = d.get('uri', '')
        p.content = d.get('content', '')
        if not p.is_valid():
            return self.end(code=-1, err_str=p.first_err())
        p.save()
        return self.end(data={
            'page': p.to_dict()
        })

    @atomic()
    def delete(self):
        t = json.loads(self.request.body)
        p = self.get_object_or_404(Page, id=t.get('id', ''))
        p.remove()
        return self.end(data=p.to_dict())
