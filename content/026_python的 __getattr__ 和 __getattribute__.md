+++
title = "python的 __getattr__ 和 __getattribute__"
date = 2009-09-11
categories = ["Tech"]
tags = ["Python"]
+++

`__getattrbute__`
===
先上代码

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

打印出：

    in get attribute
    1111111111
    in get attribute
    hello

可见 当调用一个Instance.attr 或者 Instance.method的时候，实际上是调用了`__getattribute__`
注意不要在__getattribute__的方法里面写Intance.xx，否则会进入死递归，直到溢出


`__getattr__`
===
上代码：

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

打印出：

    in get attribute
    1111111111
    in get attribute
    hello
    in get attribute
    in get attr
    None

可见 当调用一个Instance.attr 或者 Instance.method的时候，实际上先调用了`__getattribute__`，当没有找到的时候，

再调用`__getattr__`方法。

各位，有没有什么想法呢？

利用上面的方法，其实类似于rails里面的missing_method在Python中也可以实现


