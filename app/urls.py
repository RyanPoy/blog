#coding: utf8
from .controllers import *

urls = [
    (r'^/$', IndexController),
    (r'^/blogs[/]?$', ArticleIndexController),
    (r'^/blogs/(\d+)[/]?$', ArticleShowController),
    (r'^/blogs/tags/(\d+)[/]?$', TagArticleController),
    (r'^/blogs/series/(\d+)[/]?$', SeriesArticleController),
    (r'^/archives[/]?$', ArchiveController),
    (r'^/rss[/]?$', RssController),
    
    (r'/api/tags[/]?$', ApiTagController),
    (r'/api/links[/]?$', ApiLinkController),
    (r'/api/series[/]?$', ApiSeriesController),
    (r'/api/images[/]?$', ApiImageController),

    (r'/.*', ErrorController),
]