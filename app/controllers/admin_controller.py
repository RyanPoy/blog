#coding: utf8
from .base_controller import BaseController
from app.models import *
import app.ui as ui


class LeftNavController(BaseController):

    def get(self):
        # op = self.current_user
        menus = [ m for m in ui.left_menus() ]
        return self.end(data={ 'menus': menus } )


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

            
class LinkController(BaseController):

    def get(self):
        return self.end(data={ 
            'links': [ t.to_dict() for t in Link.select() ]
        })

    @atomic()
    def post(self):
        d = json.loads(self.request.body)
        name = d.get('name', '')
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Link.get_or_none(Link.name == name):
            return self.end(code=-1, err_str='存在同名友链')

        url = d.get('url', '')
        if not url:
            return self.end(code=-1, err_str='链接地址不能为空')
        if Link.get_or_none(Link.url == url):
            return self.end(code=-1, err_str='存在同链接地址友链')

        l = Link(name=name, url=url, seq=toi(d.get('seq', '0')))
        l.save()
        return self.end(data={
            'link': l.to_dict()
        })

    @atomic()
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')
        db_link = self.get_object_or_404(Link, id=_id)
        
        name = d.get('name', '')
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Link.get_or_none(
            (Link.name == name) & (Link.id != _id)
        ):
            return self.end(code=-1, err_str='存在同名友链')

        url = d.get('url', '')
        if not url:
            return self.end(code=-1, err_str='链接地址不能为空')
        if Link.get_or_none(
            (Link.url == url) & (Link.id != _id)
        ):
            return self.end(code=-1, err_str='存在同链接地址友链')

        db_link.name = d['name']
        db_link.url = d['url']
        db_link.seq = toi(d.get('seq', '0'))

        db_link.save()
        return self.end(data={
            'link': db_link.to_dict()
        })

    @atomic()
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_link = self.get_object_or_404(Link, id=_id)
        if db_link:
            Link.delete().where(Link.id == _id).execute()
            return self.end(data=db_link.to_dict())


class SeriesController(BaseController):

    def get(self):
        return self.end(data={ 
            'series': [ t.to_dict() for t in Series.select() ]
        })

    @atomic()
    def post(self):
        d = json.loads(self.request.body)
        name = d.get('name', '')
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Series.get_or_none(Series.name == name):
            return self.end(code=-1, err_str='存在同名系列')

        s = Series(name=name, seq=toi(d.get('seq', '0')))
        s.save()
        return self.end(data={
            'series': s.to_dict()
        })

    @atomic()
    def put(self):
        d = json.loads(self.request.body)
        _id = d.get('id', '')
        db_series = self.get_object_or_404(Series, id=_id)
        
        name = d.get('name', '')
        if not name:
            return self.end(code=-1, err_str='名称不能为空')
        if Series.get_or_none(
            (Series.name == name) & (Series.id != _id)
        ):
            return self.end(code=-1, err_str='存在同名系列')

        db_series.name = d['name']
        db_series.seq = toi(d.get('seq', '0'))

        db_series.save()
        return self.end(data={
            'link': db_series.to_dict()
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


class ImageController(BaseController):

    SUPPORT_IMAGE_TYPES = ('image/jpg', 'image/png', 'image/gif', 'image/jpeg')
    SUPPORT_IMAGE_MAX_SIZE = 500<<10

    def get(self):
        return self.end(data={ 
            'images': [ t.to_dict() for t in Image.select() ]
        })

    @atomic()
    def post(self):
        if 'images' not in self.request.files:
            return self.end(code=-1, err_str='请上传图片')

        for f in self.request.files['images']:
            fname, content_type, fbody = f['filename'], f['content_type'], f['body']
            if content_type.lower() not in self.SUPPORT_IMAGE_TYPES:
                return self.end(code=-1, err_str="只支持JPG、PNG、GIF 图片格式")
            if len(fbody) > self.SUPPORT_IMAGE_MAX_SIZE:
                return self.end(code=-1, err_str="最大支持512KB")
            img = Image.my_save(fname, fbody)
            return self.end(data={
                'image': img.to_dict()
            })

    @atomic()
    def delete(self):
        t = json.loads(self.request.body)
        _id = t.get('id', '')
        db_image = self.get_object_or_404(Image, id=_id)
        if db_image:
            Image.delete().where(Image.id == _id).execute()
            try:
                os.remove(db_image.abspath)
            except:
                raise
            return self.end(data=db_image.to_dict())


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
