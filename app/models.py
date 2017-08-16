#coding: utf8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):

    created_at  = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at  = models.DateTimeField('修改时间', auto_now=True, db_index=True)
    show        = models.BooleanField('是否发布', default=True, db_index=True)

    class Meta:
        abstract = True

    @classmethod
    def get_table_name(cls):
        return cls.objects.model._meta.db_table

    def created_at_str(self, fmt='%Y-%m-%d %H:%M:%S'):
        return datetime.strftime(self.created_at, fmt) if self.created_at else ''

    def created_on_str(self, fmt='%Y-%m-%d'):
        dt = getattr(self, 'created_on', None) or self.created_at
        return datetime.strftime(dt, fmt) if dt else ''

    def updated_on_str(self, fmt='%Y-%m-%d'):
        dt = getattr(self, 'updated_on', None) or self.updated_at
        return datetime.strftime(dt, fmt) if dt else ''

    def updated_at_str(self, fmt='%Y-%m-%d %H:%M:%S'):
        return datetime.strftime(self.updated_at, fmt) if self.updated_at else ''

    @property
    def created_year_for_view(self):
        return datetime.strftime(self.created_at, '%Y年') if self.created_at else ''

    @property
    def created_month_for_view(self):
        return datetime.strftime(self.created_at, '%m月') if self.created_at else ''

    @property
    def created_day_for_view(self):
        return datetime.strftime(self.created_at, '%d') if self.created_at else ''


class TagManager(models.Manager):

    def reset_article_number(self, *args, **kwargs):
        '''重新统计每个tag对应的文章数，删除空标签'''
        for i in self.filter(*args, **kwargs):
            i.count_post = i.post_set.count()
            if i.count_post <= 0:
                i.delete()
            else:
                i.save()

    def decr_article_number(self, ids, delete_isolate=True):
        '''文章数减1'''
        assert all(map(lambda i:isinstance(i, (int, long)), ids))
        self.extra(where=['id in (%s)' % ','.join(map(str, ids))]).update(count_post=F('count_post') - 1)
        if delete_isolate:
            # 删除没有和文章关联的标签
            self.filter(count_post__lte=0).delete()

    def incr_article_number(self, ids):
        '''文章数减1'''
        assert all(map(lambda i:isinstance(i, (int, long)), ids))
        self.extra(where=['id in (%s)' % ','.join(map(str, ids))]).update(count_post=F('count_post') + 1)


class Tag(BaseModel):
    objects = TagManager()

    name = models.CharField('名字', max_length=255, db_index=True, null=False, unique=True)
    article_number = models.IntegerField('文章数量', default=0)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Image(BaseModel):

    pic = models.ImageField('图片', null=False)

    def __str__(self):
        return self.pic.name

    class Meta:
        verbose_name = verbose_name_plural = '图片'



class AbsArticle(BaseModel):

    title           = models.CharField('标题', max_length=255, db_index=True, unique=True)
    keywords        = models.CharField('关键词', max_length=255, null=True, default='', editable=False)
    content         = models.TextField('MarkDown内容', null=False, default='')
    author          = models.ForeignKey(User, verbose_name='作者', editable=False)

    class Meta:
        abstract = True


class ArticleManager(models.Manager):

    def recents(self, n):
        return Article.objects.all()[:n]


class Article(AbsArticle):
    objects         = ArticleManager

    view_number     = models.IntegerField('浏览次数', null=False, default=0)
    tags            = models.ManyToManyField(Tag, verbose_name='标签')
    
    @property
    def pretty_tags(self):
        return '，'.join([ t.name for t in self.tags.all() ])

    def limit_content(self, n=64):
        return obj.content[:n] if len(obj.content) < n else obj.content[:n] + '...'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'


class PageManager(models.Manager):

    def sorted(self, *args, **kwargs):
        return self.order_by('seq ASC')

class Page(AbsArticle):
    """ 单页面，直接显示在导航栏上 """
    objects = PageManager
    seq = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = verbose_name_plural = '单页面'
