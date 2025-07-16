+++
title = "python奇技淫巧"
date = 2009-09-11

categories = ["Tech"]
tags = ["Python", "Tricks"]
+++

在Python中，有一些常见不常用又很有用的方法。本次主要讲一下`__getattr__`,`__getattribute__`, `__setattr__`, `with ... as ...`

<!--more-->

## __getattribute__
先上代码
```python
class Foo(object):
    
    def __init__(self):
        self.value = '1'*10
    
    def __getattribute__(self, name):
        print 'in get attribute'
        return super(Foo, self).__getattribute__(name)

    def hello(self):
        return 'hello'

f = Foo()
print f.value
```

打印出：
```shell
>>> in get attribute
>>> 1111111111
>>> in get attribute
>>> hello
```

可见 当调用一个Instance.attr 或者 Instance.method的时候，实际上是调用了`__getattribute__`
注意不要在__getattribute__的方法里面写Intance.xx，否则会进入死递归，直到溢出


## __getattr__

上代码：
```python
#coding: utf-8

class Foo(object):
    
    def __init__(self):
        self.value = '1'*10
    
    def __getattribute__(self, name):
        print 'in get attribute'
        return super(Foo, self).__getattribute__(name)
    
    def __getattr__(self, name):
        print 'in get attr'

    
    def hello(self):
        return 'hello'

f = Foo()
print f.value
print f.hello()
print f.value1
```

打印出：
```shell
>>> in get attribute
>>> 1111111111
>>> in get attribute
>>> hello
>>> in get attribute
>>> in get attr
>>> None
```
可见 当调用一个Instance.attr 或者 Instance.method的时候，实际上先调用了`__getattribute__`，当没有找到的时候，

再调用`__getattr__`方法。

利用上面的方法，其实类似于rails里面的missing_method在Python中也可以实现

## __setattr__
上代码：
```python
#coding: utf-8

class Foo(object):
    
    def __init__(self):
        pass
    
    def __setattribute__(self, name, value):
        self.__dict__[name] = value
        print 'in set attribute'
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        print 'in set attr'

f = Foo()
f.value = '1'*10
f.hello = lambda: 'hello'
print f.value
print f.hello()
```

打印出：
```shell
>>> in set attr
>>> in set attr
>>> 1111111111
>>> hello
```
可见
```python
Instance.attr = value
Instance.method = xxx
```
都是调用的`__setattr__`方法，注意不要在`__setattr__`里面再调用Instance.xx = yy或者 setattr的方法，否则会进行死递归，直到溢出


## with ... as ...
python2.6中有一个特殊的用法：`with...as...`  ；  在2.5中需要`import __feature__`;

先来说说他的用法，先看看一般我们如何打开并且读取一个文件的：
```python
f = None
try:
    f = open('/etc/hosts', 'r')
    print f.readlines()
except:
    raise
finally:
    if f:
        try:
            f.close()
        except:
            pass
        finally:
            f = None
```
一个简单的文件操作，但是对于文件的打开和关闭我们做了太多的处理。那么如果减少这些资源的打开和释放的代码呢？请看下面：
```python
    with open('/etc/hosts', 'r') as f:
        print f.readlines()
```
实现了同样的功能，但是文件的关闭在哪里呢？这个就是with ... as ... 的作用了。它最大的好处就是自动释放一些资源。那么原理是怎么样的呢？看看下面的代码吧：
```python
class Foo(object):
    
    def __enter__(self):
        print 'in enter' 
    
    def __exit__(self, exc_type, exc_value, traceback):
        print 'exit'    

with Foo() as f:
    pass
```

打印出：
```shell
>>> in enter
>>> exit
```

可见 `with ... as ...` 的时候，嗲用了 `__enter__` 的方法，当跳出with 代码段的时候，自动调用了 `__exit__`的方法。对于高版本的python来说，可以直接用contextmanager来进行相同的工作。而我们可以利用这个写出很多有意思的代码，例如在操作数据库的时候，假设有一个User的ORM。

那么对于事务的处理，我们完全可以写成：
```python
class Transaction(object):
 
    def __init__(self, db):
        self._conn = db
        self._conn._db.autocommit(False)
        
    def commit(self):
        if self._conn._db:
            self._conn._db.commit()
            self._conn._db.autocommit(True)
        
    def rollback(self):
        if self._conn._db:
            self._conn._db.rollback()
            self._conn._db.autocommit(True)


class User(object):
    
    @classmethod
    @contextmanager
    def transaction(cls):
        t = Transaction(db)
        try:
            yield None
        except Exception, ex:
            t.rollback()
            raise
        else:
            t.commit()

with User.transaction():
    # do sth.
```
