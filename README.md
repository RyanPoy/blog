# 是什么
这是一个个人博客的开源项目

# 依赖什么
- python3.6
- django
- tornado
- Pillow
- uvloop，因为tornado的异步处理能力远远比不上uvloop，所以用uvloop代替了tornado的ioloop
- 搜狐畅言，因为本站的评论系统直接用了搜狐畅言，具体看：https://changyan.kuaizhan.com
- 百度站内搜索，因为本站的站内搜索采用了百度的站内搜索，具体看：http://http://zn.baidu.com

# 作用
某天突然发现自己没有了好奇心。感觉世界都没有意思了。我意识到自己要做点什么，用来拜托这个局面。想到之前有一个blog。用了别人的东西。那么不如自己来写一个吧。所以，便有了它。

这个项目是沿用了tornado+django的模式。用了tornado的web相关。用了django的orm。恰好，对于一个blog又没有太多的业务。所以，django-admin也就能支撑起用户的后台了。


# 示例
[彭一的blog](http://www.pengyi.info)


# 执行步骤

- 创建数据库
  - create database blog default charset utf8
- 执行migration
  - python3 manage.py makemigrations
  - python3 manage.py migrate
- 创建超级管理员
  - python3 manage.py createsuperuser
- 启动
  - 执行 python3 blog_app.py。具体参数有：
    -  --admin-port                     Admin监听端口，默认：8001 (default 0)
    -  --debug                          是否是调试模式，默认：true (default true)
    -  --port                           系统监听端口，默认：8001 (default 8001)
    -  --tmpl                           模板，默认：default (default default)

    ```具体参看源代码 blog_app.py```
