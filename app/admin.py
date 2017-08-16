#coding: utf8
from django.contrib import admin
from django.utils.html import mark_safe
from django.db.models import F
from .models import *

# Register your models here.

class TagAdmin(admin.ModelAdmin):

    search_fields = ['name']
    list_display = ['id', 'name', 'article_number', 'created_at', 'updated_at']


class ImageAdmin(admin.ModelAdmin):

    search_fields = ['name', 'url']
    list_display = ['id', 'img', 'name', 'size', 'url', 'created_at', 'updated_at']

    def size(self, obj):
        return '%.2f KB' % (obj.pic.size / 1024.0)
    size.short_description = '大小'

    def name(self, obj):
        return obj.pic.name

    def img(self, obj):
        return mark_safe("<img src='{}' style='height:64px;' />".format(obj.pic.url))
    img.short_description = '图片'

    def url(self, obj):
        return obj.pic.url
    url.short_description = 'URL'


class ArticleAdmin(admin.ModelAdmin):

    search_fields = ['name']
    list_display = [
        'id', 'title', 'author', 'keywords', 'view_number', 
        'pretty_tags', 'created_at', 'updated_at'
    ]
    list_filter = ['tags', 'author']
    
    def pretty_tags(self, obj):
        return obj.pretty_tags
    pretty_tags.short_description = '标签'

    def save_model(self, request, obj, form, change):
        '''新建/编辑 文章'''
        is_editing = bool(obj.id)
        obj.author = request.user
        old_tags = None

        # 保存原有标签
        if is_editing:
            old_tags = set(Article.objects.get(id=obj.id).tags.values_list('id', flat=True))

        # 因为要在保存post和tag的关系之后处理tag计数，所以hook掉form的save_m2m
        _save_m2m = form.save_m2m
        def after_save():
            _save_m2m()
            if is_editing:
                new_tags = set(obj.tags.values_list('id', flat=True))
                # 得到需要增减计数的标签列表
                decr_tags = old_tags - new_tags
                incr_tags = new_tags - old_tags
                if incr_tags:
                    Tag.objects.incr_article_number(incr_tags)
                if decr_tags:
                    Tag.objects.decr_article_number(decr_tags)
            else:
                # 新文章，直接更新tags计数
                obj.tags.all().update(article_number=F('article_number') + 1)
        form.save_m2m = after_save
        return super(ArticleAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        '''删除文章'''
        tags = obj.tags.values_list('id', flat=True)
        # 减少标签计数
        if tags:
            Tag.objects.decr_article_number(tags)
        ret = super(ArticleAdmin, self).delete_model(request, obj)


admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Article, ArticleAdmin)
