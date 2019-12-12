#coding: utf8
from app.controllers import BaseController
from app.models import *
from app.libs import *


class TagController(BaseController):

    def get(self):
        return self.end(data={
            'tags': [ t.to_dict() for t in Tag.select() ]
        })

    @atomic()
    def post(self):
        d = json.loads(self.request.body)
        name = d.get('name', '')
        t = Tag.new(name=name)
        if not t.is_valid():
            return self.end(code=-1, err_str=t.first_err())
        t.save()
        return self.end(data={ 'tag': t.to_dict() })

    @atomic()
    def put(self):
        d = json.loads(self.request.body)
        t = self.get_object_or_404(Tag, id=d.get('id', ''))
        t.name = d.get('name', '')
        if not t.is_valid():
            return self.end(code=-1, err_str=t.first_err())
        t.save()
        return self.end(data={
            'tag': t.to_dict()
        })        

    @atomic()
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_tag = self.get_object_or_404(Tag, id=_id)
        db_tag.remove()
        return self.end(data=db_tag.to_dict())
