#coding: utf8
from app.controllers import BaseController
from app.models import *
from app.libs import *


class SeriesController(BaseController):

    def get(self):
        return self.end(data={ 
            'series': [ t.to_dict() for t in Series.select() ]
        })

    @atomic()
    def post(self):
        d = json.loads(self.request.body)
        s = Series.new(
            name=d.get('name', ''), 
            seq=toi(d.get('seq', '0'))
        )
        if not s.is_valid():
            return self.end(code=-1, err_str=s.first_err())

        s.save()
        return self.end(data={
            'series': s.to_dict()
        })

    @atomic()
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')
        s = self.get_object_or_404(Series, id=_id)
        s.name = d.get('name', '')
        s.seq = toi(d.get('seq', '0'))

        if not s.is_valid():
            return self.end(code=-1, err_str=s.first_err())

        s.save()
        return self.end(data={
            'series': s.to_dict()
        })

    @atomic()
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_series = self.get_object_or_404(Series, id=_id)
        if db_series:
            Article.update(series_id=None).where(Article.series_id == _id).execute()
            Series.delete().where(Series.id == _id).execute()
            return self.end(data=db_series.to_dict())

