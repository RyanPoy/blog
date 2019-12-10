#coding: utf8
# from .controllers import web_controller, admin_controller
import app.controllers.web_controller as web_controller
import app.controllers.admin_controller as admin_controller


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
    (r'/api/tags[/]?$', admin_controller.TagController),
    (r'/api/links[/]?$', admin_controller.LinkController),
    (r'/api/series[/]?$', admin_controller.SeriesController),
    (r'/api/images[/]?$', admin_controller.ImageController),
    (r'/api/pages[/]?$', admin_controller.PageController),
    (r'/api/articles[/]?$', admin_controller.ArticleController),

    (r'/.*', web_controller.Error),
]