---
title: Webpy使用教程
date: 2011-08-18

category: Tutorials
tags: [Python, Webpy]
---

Web.py 是一个轻量级的 Python Web 框架，它以简单、直接而闻名，旨在让 Web 应用开发变得快速而容易。Web.py的核心代码库非常小巧，只提供构建 Web 应用所需的基本功能，如 URL 路由、请求/响应处理、模板渲染等。这让它非常容易学习和上手。

<!--more-->

来[搜狐](https://sohu.com)后，这里做的系统几乎都是 webpy + twsited 写的。所以，有必要好好学习一下这两个东西了。从今天开始介绍Web.py。

## Server

**安装**
```shell
sudo pip install web.py
```

**第一个demo**
```python
#coding: utf-8    
import web

urls = (
    '/', 'Index'
)

class Index:

    def GET(self):
        return 'Hello, world ! GET \n'

    def POST(self):
        return 'Hello, world ! POST \n'


def start():
    app = web.application(urls, globals())
    app.run()


if __name__ == '__main__':
    start()
```

**启动**
```shell
python webpy_test.py 0.0.0.0:4321
```

**GET 测试**
```shell
>>> curl http://localhost:4321
>>> Hello, world ! GET
```

**POST 测试**
```shell
>>> curl http://localhost:4321 -d't=1'
>>> Hello, world ! POST
```

**总结**
1. url 简单的就是字符串，和django很类似
2. 对于Controller而言，get请求执行GET方法，post请求执行POST方法，估计PUT和DELETE等也是一样的


## Template
公司直接用的jinja。jinja和django template的太相似了。说说如果在webpy中使用jinja。

**webpy_jinja.py**
```python
#coding: utf-8

import web
from web.contrib.template import render_jinja

urls = (
    '/', 'hello'
)

app = web.application(urls, globals())

render = render_jinja(
    'templates',           # 模板位置.
    encoding = 'utf-8',    # 编码.
)


class Hello:

    def GET(self):
        return render.hello(value='hello, World! GET')

    def POST(self):
        return web.seeother('/')


if __name__ == "__main__":
    app.run()
```

**hello.html**
```python
{{value}}
```

**跳转**
- Hello 的 GET 请求就是直接的服务器渲染页面，发送给客户端(一般是browser)
- Hello 的 POST 就是服务器端返回给客户端http code，然后客户端直接进行跳转，再次跳转到Hello的GET上

## 数据库操作

**得到连接**
```python
db = web.database(dbn='postgres', db='mydata', user='dbuser', pw='')
```

**简单查询**
```python
db.select(
    'table_name',                   # 表名
    vars  = {'name'='py'},          # 用来填充查询条件, 这个例子中对应的就是where的$name
    where = 'username=$name',       # 查询条件
    what  = 'id, username',         # 表示你要查询的field是哪些，默认为*。这个例子中表示查询id和username字段
    order = 'age DESC',             # 排序方式，表示按照年龄的倒排
    group = 'gender',               # 表示按照gender分组
    limit = 10,                     # 查询10条
    offset = 10,                    # 表示从第10条开始
    _test  = True/False             # 日志打印出查询语句，True表示打印，False表示不打印。一般debug环境设置为True
)
```

**高级查询**
```python
db.query("SELECT COUNT(*) AS total_users FROM users")

# 有sql注入，可以修改为下面的
db.query("SELECT * FROM user WHERE user.id = %s" % 10) 

# 没有sql注入
db.query("SELECT * FROM user WHERE user.id = $id", vars = {'id': 10 }) 
```

**更新**
```python
# 把id=10的记录的username修改为pengyi
db.update('table_name', where="id = 10", username = "pengyi") 
```

**插入**
```python
db.insert('table_name', username="Poy") # 插入一条记录，设置username=Poy
```

**删除**
```python
db.delete('table_name', where="id = 10") # 删除id=10的记录
```

**事务**
```python
with db.transaction():
    db.insert('table_name', name='py')
    db.insert('table_name', name='pengyi')
```
部署就不用说太多。直接fastcgi

### cgi配置

**安装flug**
```shell
sudo pip install flup
```

**webpy启动代码中写**
```python
def run_cgi(func, addr):
    return flups.WSGIServer(func, multiplexed=False, bindAddress=addr).run()

def start_fcgi():
    app = web.application(urls, globals())
    web.wsgi.runwsgi = lambda func, addr = None: flups.WSGIServer(func, multiplexed=False, bindAddress=addr).run()
    app.run()
```

### 性能测试

webpy的性能真的是不敢恭维啊

代码如下：
```python
#coding: utf-8    
import web

urls = (
    '/', 'Index'
)

class Index:
    def GET(self):
        return 'Hello, world !\n'

def start():
    app = web.application(urls, globals())
    app.run()

if __name__ == '__main__':
    start()
```

利用apache 的ab进行压力测试，10并发1000次请求：
```shell
>>> ab -c 10 -n 1000 http://192.168.95.222:4321/
>>> 
>>> This is ApacheBench, Version 2.3 <$Revision: 655654 $>
>>> Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
>>> Licensed to The Apache Software Foundation, http://www.apache.org/
>>> 
>>> Benchmarking 192.168.95.222 (be patient)
>>> Completed 100 requests
>>> Completed 200 requests
>>> Completed 300 requests
>>> Completed 400 requests
>>> Completed 500 requests
>>> Completed 600 requests
>>> Completed 700 requests
>>> Completed 800 requests
>>> Completed 900 requests
>>> Completed 1000 requests
>>> Finished 1000 requests
>>> 
>>> Server Software:        CherryPy/3.1.2
>>> Server Hostname:        192.168.95.222
>>> Server Port:            4321
>>> 
>>> Document Path:          /
>>> Document Length:        16 bytes
>>> 
>>> Concurrency Level:      10
>>> Time taken for tests:   6.269 seconds
>>> Complete requests:      1000
>>> Failed requests:        0
>>> Write errors:           0
>>> Total transferred:      108000 bytes
>>> HTML transferred:       16000 bytes
>>> Requests per second:    159.51 [#/sec] (mean)
>>> Time per request:       62.691 [ms] (mean)
>>> Time per request:       6.269 [ms] (mean, across all concurrent requests)
>>> Transfer rate:          16.82 [Kbytes/sec] received
>>> 
>>> Connection Times (ms)
>>>               min  mean[+/-sd] median   max
>>> Connect:        1    1   0.3      1       5
>>> Processing:    29   61  14.7     61     373
>>> Waiting:       29   61  14.7     61     372
>>> Total:         30   62  14.7     62     374
>>> 
>>> Percentage of the requests served within a certain time (ms)
>>>   50%     62
>>>   66%     64
>>>   75%     65
>>>   80%     66
>>>   90%     68
>>>   95%     70
>>>   98%     71
>>>   99%     73
>>>  100%    374 (longest request)
```

平均每秒只能在160s，太低了。

**再来看 100并发，2000请求**
```shell
>>> ab -c 100 -n 2000 http://192.168.95.222:4321/
>>> 
>>> This is ApacheBench, Version 2.3 <$Revision: 655654 $>
>>> Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
>>> Licensed to The Apache Software Foundation, http://www.apache.org/
>>> 
>>> Benchmarking 192.168.95.222 (be patient)
>>> Completed 200 requests
>>> Completed 400 requests
>>> Completed 600 requests
>>> Completed 800 requests
>>> Completed 1000 requests
>>> Completed 1200 requests
>>> Completed 1400 requests
>>> Completed 1600 requests
>>> Completed 1800 requests
>>> Completed 2000 requests
>>> Finished 2000 requests
>>> 
>>> 
>>> Server Software:        CherryPy/3.1.2
>>> Server Hostname:        192.168.95.222
>>> Server Port:            4321
>>> 
>>> Document Path:          /
>>> Document Length:        20 bytes
>>> 
>>> Concurrency Level:      100
>>> Time taken for tests:   15.158 seconds
>>> Complete requests:      2000
>>> Failed requests:        0
>>> Write errors:           0
>>> Total transferred:      224000 bytes
>>> HTML transferred:       40000 bytes
>>> Requests per second:    131.94 [#/sec] (mean)
>>> Time per request:       757.902 [ms] (mean)
>>> Time per request:       7.579 [ms] (mean, across all concurrent requests)
>>> Transfer rate:          14.43 [Kbytes/sec] received
>>> 
>>> Connection Times (ms)
>>>               min  mean[+/-sd] median   max
>>> Connect:        1   37 203.5      1    1207
>>> Processing:    58  707 915.3    640    6597
>>> Waiting:       57  707 915.3    639    6596
>>> Total:         61  744 1076.6    641    7802
>>> 
>>> Percentage of the requests served within a certain time (ms)
>>>   50%    641
>>>   66%    647
>>>   75%    650
>>>   80%    652
>>>   90%    667
>>>   95%   2641
>>>   98%   7173
>>>   99%   7674
>>>  100%   7802 (longest request)
```
每秒：131个请求，响应时间是：757ms左右。无法忍受了。
