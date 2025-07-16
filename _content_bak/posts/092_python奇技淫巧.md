+++
title = "python奇技淫巧"
date = 2013-01-05

categories = ["Tech"]
tags = ["Python"]
+++

- 巧用异常得到代码片段的信息

  python 有`__file__`, 但没有`__funcname__`, `__line__` 这样的东西，来描述目前执行到什么方法，哪一行。
怎么办？巧用异常，可以得到相应的信息。

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

- 基本数学

一个方法得到整数和余数

    print divmod(5, 3)

利用两个*号，求幂

    print 2**3

- 利用namedtuple代替常量的dict

dict的优势在于简单，缺点在于key可以是随意的，所以，有时候key填错了，也不容易找出来。而且，由于dict的完全对外开发性。所以，通过某些步骤后，可能内容就完全变化了。所以，当你的dict作为一个常量的时候，可以考虑用namedtuple，这样增加了代码的可读性。而且，减少了出错的概率

    from collections import namedtuple
    user = namedtuple('User', ['name', 'password'])._make(['pengyi', '888888'])
    print user.name, user.password

- 快速拉平一个list

对于一个list，里面的元素可能又是一个list或者tuple。那么有没有方式快速拉平？

    def flatten(sequnce):
        for x in sequnce:
            if isinstance(x, (list, tuple)):
                for y in flatten(x):
                    yield y
            else:
                yield x
                 
     
    for x in flatten(['a', ['b', 'c'], range(10), 'f']):
        print x


- 元素组合

组合一个集合里面的所有元素

    from itertools import combinations

    for x in combinations(range(10), 2):
        print x
    for x in combinations(range(10), 3):
        print x

- 对list进行排序

不忽略大小写

    l = ['B', 'a', 'A', 'b' ]
    l.sort()

忽略大小写

    l = ['B', 'a', 'A', 'b' ]
    l.sort(key = str.lower)

- 对字典进行排序

对于元素很多的字典可以这样：

    def sort_dict(d):
        for k in sorted(d.iterkeys()):
            yield k, d[k]

对于元素不多的字典可以这样：

    [ k, d[k] for k in sorted(d.iterkeys()) ]

- 保证字典的插入顺序

对于字典来说，key是hash算法。那么，无法保证插入顺序。但是python的标准库里面提供了一个SortedDict，用法和dict一样。

    for k, v in SortedDict(a=1, b=2, c=3, aa=4, bb=5).iteritems():
        print k, v


