+++
title = "python 的 with statement"
date = 2009-09-29

[taxonomies]
categories = ["Tech"]
tags = ["Python"]
+++

python2.6中有一个特殊的关键词，with...as...

在2.5中的__feature__中也有

先来说说他的用法，先看看一般我们如何打开并且读取一个文件的：

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

一个简单的文件操作，但是对于文件的打开和关闭我们做了太多的处理。
那么如果减少这些资源的打开和释放的代码呢？请看下面：

    with open('/etc/hosts', 'r') as f:
        print f.readlines()

实现了同样的功能，但是文件的关闭在哪里呢？这个就是with ... as ... 的作用了。
它最大的好处就是自动释放一些资源。那么原理是怎么样的呢 ？

看看下面的代码吧：

    class Foo(object):
        
        def __enter__(self):
            print 'in enter' 
        
        def __exit__(self, exc_type, exc_value, traceback):
            print 'exit'
        
    
    f = Foo()
    
    with Foo() as f:
        pass

打印出：

    in enter
    exit

现在明白了吧：
with ... as ... 的时候，嗲用了 `__enter__` 的方法，当跳出with 代码段的时候，自动调用了 `__exit__`的方法

对于高版本的python来说，可以直接用contextmanager来进行相同的工作。这里大家可以尝试一下。

而我们可以利用这个写出很多有意思的代码，例如在操作数据库的时候，假设有一个User的ORM。

那么对于事务的处理，我们完全可以写成：


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



