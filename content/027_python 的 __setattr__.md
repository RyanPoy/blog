+++
title = "python 的 __setattr__"
date = 2009-09-13

[taxonomies]
categories = ["Tech"]
tags = ["Python"]
+++

`__setattr__`
===
上代码：

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

打印出：

    in set attr
    in set attr
    1111111111
    hello

可见

    Instance.attr = value
    Instance.method = xxx

都是调用的`__setattr__`方法，注意不要在`__setattr__`里面再调用Instance.xx = yy或者 setattr的方法，否则会进行死递归，直到溢出




