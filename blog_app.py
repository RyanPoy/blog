#coding: utf8
############import django
import os

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
get_wsgi_application()

from tornado import options, httputil
from settings import *
from app.urls import urls
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.util import unicode_type
import logging


def utf8(value):
    """Converts a string argument to a byte string.

    If the argument is already a byte string or None, it is returned unchanged.
    Otherwise it must be a unicode string and is encoded as utf8.
    """
    if value is None or value == 'None':
        value = ""
    if isinstance(value, tornado.escape._UTF8_TYPES):
        return value
    if not isinstance(value, unicode_type):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.encode("utf-8")
tornado.escape.utf8 = utf8

options.define('port', default=8001, type=int, help=u'抢票系统监听端口，默认：8001')
options.define('debug', default='true', type=str, help=u'是否是调试模式，默认：true')
options.define('tmpl', default='default', type=str, help=u'模板，默认：default')

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


def ping_db():
    from app.models import Tag
    Tag.objects.first()
    print '*'*10, 'ping db'


def main():
    options.parse_command_line()
    
    address, port = '0.0.0.0', options.options.port
    debug = options.options.debug == 'true'
    tmpl = options.options.tmpl

    tornado_env = builder_tornado_env(tmpl)
    tornado_env['debug'] = debug

    ioloop = tornado.ioloop.IOLoop.instance()
    application = tornado.web.Application(urls, **tornado_env)

    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(port, address)
    print 'server run on (%s:%s)，tmpl is "%s"' % (address, port, tmpl)

    tornado.ioloop.PeriodicCallback(ping_db, int(db_ping_seconds * 1000)).start()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        ioloop.stop()


if __name__ == '__main__':
    main()
