---
title: python奇技淫巧
date: 2009-09-11

category: Tech
tags: [Python, Tricks]
---

在Python中，有一些常见不常用又很有用的**奇技淫巧**

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

## 巧用异常得到代码片段的信息
python 有`__file__`, 但没有`__funcname__`, `__line__` 这样的东西，来描述目前执行到什么方法，哪一行。怎么办？巧用异常，可以得到相应的信息。
```python
#utf-8
import sys

def func_name_and_line():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    return f.f_code.co_name, f.f_lineno
    
def test():
    print func_name_and_line()

if __name__ == '__main__':
    test()
```

## 基本数学

**一个方法得到整数和余数**
```python
print divmod(5, 3)
```

**利用两个*号，求幂**
```python
print 2**3
```

**利用namedtuple代替常量的dict**

dict的优势在于简单，缺点在于key可以是随意的，所以，有时候key填错了，也不容易找出来。而且，由于dict的完全对外开发性。所以，通过某些步骤后，可能内容就完全变化了。所以，当你的dict作为一个常量的时候，可以考虑用namedtuple，这样增加了代码的可读性。而且，减少了出错的概率
```python
from collections import namedtuple
user = namedtuple('User', ['name', 'password'])._make(['pengyi', '888888'])
print user.name, user.password
```

**快速拉平一个list**

对于一个list，里面的元素可能又是一个list或者tuple。那么有没有方式快速拉平？
```python
def flatten(sequnce):
    for x in sequnce:
        if isinstance(x, (list, tuple)):
            for y in flatten(x):
                yield y
        else:
            yield x
 
for x in flatten(['a', ['b', 'c'], range(10), 'f']):
    print x
```

**元素组合**

组合一个集合里面的所有元素
```python
from itertools import combinations

for x in combinations(range(10), 2):
    print x
for x in combinations(range(10), 3):
    print x
```

**对list进行排序**
- 不忽略大小写
```python
l = ['B', 'a', 'A', 'b' ]
l.sort()
```

- 忽略大小写
```python
l = ['B', 'a', 'A', 'b' ]
l.sort(key = str.lower)
```

**对字典进行排序**

- 元素很多的字典：
```python
def sort_dict(d):
    for k in sorted(d.iterkeys()):
        yield k, d[k]
```

- 元素不多的字典：
```python
[ k, d[k] for k in sorted(d.iterkeys()) ]
```

***SortedDict* 保证字典的插入顺序**
对于字典来说，key是hash算法。那么，无法保证插入顺序。但是python的标准库里面提供了一个SortedDict，用法和dict一样。
```python
for k, v in SortedDict(a=1, b=2, c=3, aa=4, bb=5).iteritems():
    print k, v
```
