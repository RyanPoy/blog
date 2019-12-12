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


class PageController(BaseController):

    def get(self):
        return self.end(data={ 
            'pages': [ p.to_dict() for p in Page.select() ]
        })

    @atomic()
    def post(self):
        d = json.loads(self.request.body)
        title = d.get('title', '')
        if not title:
            return self.end(code=-1, err_str='名称不能为空')
        if Page.get_or_none(Page.title == title):
            return self.end(code=-1, err_str='存在同名页面')

        uri = d.get('uri', '')
        if not uri:
            return self.end(code=-1, err_str='链接地址不能为空')

        content = d.get('content', '')
        if not content:
            return self.end(code=-1, err_str='内容不能为空')
        if len(content) < 4:
            return self.end(code=-1, err_str='正文长度不能少于4个字')

        p = Page(title=title, seq=toi(d.get('seq', '0')), content=content, uri=uri)
        p.save()
        return self.end(data={
            'page': p.to_dict()
        })

    @atomic()
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')
        db_page = self.get_object_or_404(Page, id=_id)
        
        title = d.get('title', '')
        if not title:
            return self.end(code=-1, err_str='名称不能为空')
        if Page.get_or_none(
            (Page.title == title) & (Page.id != _id)
        ):
            return self.end(code=-1, err_str='存在同名页面')

        content = d.get('content', '')
        if not content:
            return self.end(code=-1, err_str='内容不能为空')
        if len(content) < 4:
            return self.end(code=-1, err_str='正文长度不能少于4个字')

        uri = d.get('uri', '')
        if not uri:
            return self.end(code=-1, err_str='链接地址不能为空')

        db_page.title = title
        db_page.uri = uri
        db_page.seq = toi(d.get('seq', '0'))
        db_page.content = content
        db_page.save()
        return self.end(data={
            'page': db_page.to_dict()
        })

    @atomic()
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_page = self.get_object_or_404(Page, id=_id)
        if db_page:
            Page.delete().where(Page.id == _id).execute()
            return self.end(data=db_page.to_dict())


class ArticleController(BaseController):

    def get(self):
        return self.end(data={ 
            'articles': [ a.to_dict() for a in Article.select().order_by(Article.id.desc()) ]
        })

    @atomic()
    def post(self):
        d = json.loads(self.request.body)

        title = d.get('title', '')
        if not title:
            return self.end(code=-1, err_str='请填写标题')
        if Article.get_or_none(Article.title == title):
            return self.end(code=-1, err_str='存在同标题文章')

        view_number = toi(d.get('view_number', 0))
        if view_number < 0:
            view_number = 0

        tags = []
        tag_ids = d.get('tag_ids', [])
        if tag_ids: # 去除无效的 tag
            tags = Tag.select().where(Tag.id.in_(tag_ids))

        keywords = d.get('keywords', '').strip()
        series = d.get('series_id', 0)
        if series:
            series = Series.get_or_none(Series.id == series)
            if not series:
                return self.end(code=-1, err_str='请选择正确的系列')

        content = d.get('content', '').strip()
        if not content:
            return self.end(code=-1, err_str='内容不能为空')
        if len(content) < 4:
            return self.end(code=-1, err_str='正文长度不能少于4个字')

        a = Article(title=title, content=content, keywords=keywords, view_number=view_number)
        if series:
            a.series = series
        a.save()

        if tags:
            a.tags.add(tags)
        for t in tags:
            t.article_number += 1
            t.save()
        a.save()

        return self.end(data={
            'article': a.to_dict()
        })

    @atomic()
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')

        db_article = self.get_object_or_404(Article, id=_id)

        title = d.get('title', '')
        if not title:
            return self.end(code=-1, err_str='请填写标题')
        if Article.get_or_none(
            (Article.title == title) & (Article.id != db_article.id)
        ):
            return self.end(code=-1, err_str='存在同标题文章')

        view_number = toi(d.get('view_number', 0))
        if view_number < 0:
            view_number = 0

        tags = []
        tag_ids = d.get('tag_ids', [])
        if tag_ids: # 去除无效的 tag
            tags = Tag.select().where(Tag.id.in_(tag_ids))

        keywords = d.get('keywords', '').strip()
        series = d.get('series_id', 0)
        if series:
            series = Series.get_or_none(Series.id == series)
            if not series:
                return self.end(code=-1, err_str='请选择正确的系列')

        content = d.get('content', '').strip()
        if not content:
            return self.end(code=-1, err_str='内容不能为空')
        if len(content) < 4:
            return self.end(code=-1, err_str='正文长度不能少于4个字')

        db_article.title = title
        db_article.content = content
        db_article.keywords = keywords
        db_article.view_number = view_number
        if series:
            db_article.series = series

        if tags:
            pretty_tagid_tags_mapping = { t.id:t for t in tags }

            db_tags = db_article.tags
            db_tagid_tags_mapping = { t.id:t for t in db_tags}

            should_add_tags = [ t for t in tags if t.id not in db_tagid_tags_mapping ]
            should_delete_tags = [ t for t in db_tags if t.id not in pretty_tagid_tags_mapping ]
            
            db_article.tags.add(should_add_tags)
            db_article.tags.remove(should_delete_tags)

            for t in should_add_tags:
                t.article_number += 1
                t.save()

            for t in should_delete_tags:
                t.article_number -= 1
                if t.article_number < 0:
                    t.article_number == 0
                t.save()

        db_article.save()
        return self.end(data={
            'article': db_article.to_dict()
        })
    
    @atomic()
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_article = self.get_object_or_404(Article, id=_id)
        if db_article:
            db_tags = db_article.tags
            for t in db_tags:
                t.article_number -= 1
                if t.article_number < 0:
                    t.article_number == 0
                t.save()
            db_article.tags.clear()
            Article.delete().where(Article.id == _id).execute()
            return self.end(data=db_article.to_dict())


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
