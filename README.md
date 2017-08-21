# 是什么
这是一个个人博客的开源项目

# 依赖什么
- python3.6
- django
- tornado
- Pillow

# 作用
某天突然发现自己没有了好奇心。感觉世界都没有意思了。我意识到自己要做点什么，用来拜托这个局面。想到之前有一个blog。用了别人的东西。那么不如自己来写一个吧。所以，便有了它。

这个项目是沿用了tornado+django的模式。用了tornado的web相关。用了django的orm。恰好，对于一个blog又没有太多的业务。所以，django-admin也就能支撑起用户的后台了。

# 示例
[彭一的blog](http://www.pengyi.info)


# 简单说明
启动的时候，执行 python3 blog_app.py。具体参数有：

-  --admin-port                     Admin监听端口，默认：8001 (default 0)
-  --debug                          是否是调试模式，默认：true (default true)
-  --port                           系统监听端口，默认：8001 (default 8001)
-  --tmpl                           模板，默认：default (default default)

具体参看源代码 blog_app.py
