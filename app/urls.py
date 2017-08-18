#coding: utf8
from .controllers import *

urls = [
    (r'^/$', IndexController),
    (r'^/blogs[/]?$', ArticleIndexController),
    (r'^/blogs/(\d+)[/]?$', ArticleShowController),
    (r'^/blogs/tags/(\d+)[/]?$', ArticleListController),
    (r'^/archives[/]?$', ArchiveController),
    (r'/.*', ErrorController),
]