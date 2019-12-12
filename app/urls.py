#coding: utf8
# from .controllers import web_controller, admin_controller
from app.controllers import web_controller
from app.controllers import admin_controller

from app.controllers import admin


urls = [
    (r'^/$', web_controller.Index),
    (r'^/blogs[/]?$', web_controller.ArticleIndex),
    (r'^/blogs/(\d+)[/]?$', web_controller.ArticleShow),
    (r'^/blogs/tags/(\d+)[/]?$', web_controller.TagArticle),
    (r'^/blogs/series/(\d+)[/]?$', web_controller.SeriesArticle),
    (r'^/archives[/]?$', web_controller.Archive),
    (r'^/rss[/]?$', web_controller.Rss),

    (r'/api/signin[/]?', admin_controller.SigninController),
    (r'/api/left-nav[/]?', admin_controller.LeftNavController),
    (r'/api/tags[/]?$', admin.TagController),
    (r'/api/links[/]?$', admin.LinkController),
    (r'/api/series[/]?$', admin.SeriesController),
    (r'/api/images[/]?$', admin.ImageController),
    (r'/api/pages[/]?$', admin.PageController),
    (r'/api/articles[/]?$', admin_controller.ArticleController),

    (r'/.*', web_controller.Error),
]