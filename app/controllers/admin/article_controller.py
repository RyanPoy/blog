#coding: utf8
from app.controllers import BaseController
from app.models import *
from app.libs import *


class ArticleController(BaseController):

    def get(self):
        return self.end(data={ 
            'articles': [ a.to_dict() for a in Article.select().order_by(Article.id.desc()) ]
        })

    @atomic()
    def post(self):
        d = json.loads(self.request.body)
        a = Article.new(
            title=d.get('title', ''), 
            content=d.get('content', '').strip(), 
            keywords=d.get('keywords', '').strip(), 
            view_number=toi_gte0(d.get('view_number', 0))
        )
        a.series = Series.get_or_none(Series.id == toi(d.get('series_id', 0)))
        if not a.is_valid():
            return self.end(code=-1, err_str=a.first_err())
        a.save()
        a.add_tags(d.get('tag_ids', []))

        return self.end(data={
            'article': a.to_dict()
        })

    @atomic()
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')

        a = self.get_object_or_404(Article, id=_id)
        a.title = d.get('title', '')
        a.view_number = toi_gte0(d.get('view_number', 0))
        a.content = d.get('content', '').strip()
        a.keywords = d.get('keywords', '').strip()
        a.series = Series.get_or_none(Series.id == toi(d.get('series_id', 0)))
        if not a.is_valid():
            return self.end(code=-1, err_str=a.first_err())
        a.save()
        a.update_tags(d.get('tag_ids', []))
        return self.end(data={
            'article': a.to_dict()
        })
    
    @atomic()
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        a = self.get_object_or_404(Article, id=_id)
        a.remove()
        return self.end(data=a.to_dict())
