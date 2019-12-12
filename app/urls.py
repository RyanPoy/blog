#coding: utf8
from app.controllers import admin
from app.controllers import web_controller


urls = [
    (r'^/$', web_controller.Index),
    (r'^/blogs[/]?$', web_controller.ArticleIndex),
    (r'^/blogs/(\d+)[/]?$', web_controller.ArticleShow),
    (r'^/blogs/tags/(\d+)[/]?$', web_controller.TagArticle),
    (r'^/blogs/series/(\d+)[/]?$', web_controller.SeriesArticle),
    (r'^/archives[/]?$', web_controller.Archive),
    (r'^/rss[/]?$', web_controller.Rss),

    (r'/api/left-nav[/]?', admin.LeftNavController),
    (r'/api/signin[/]?', admin.SessionController),
    (r'/api/tags[/]?$', admin.TagController),
    (r'/api/links[/]?$', admin.LinkController),
    (r'/api/series[/]?$', admin.SeriesController),
    (r'/api/images[/]?$', admin.ImageController),
    (r'/api/pages[/]?$', admin.PageController),
    (r'/api/articles[/]?$', admin.ArticleController),

    (r'/.*', web_controller.Error),
]