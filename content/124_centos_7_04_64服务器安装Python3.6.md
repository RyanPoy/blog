+++
title = "centos_7_04_64服务器安装Python3.6"
date = 2018-12-05
categories = ["Tech"]
tags = ["Python", "环境安装"]
+++

大概在6月份，使用了阿里云的ECS。安装的是  centos_7_04_64。
在执行了

    yum upgrade 

之后，再执行

    yum search python3 

只能看到python34的东西，当时没有多想。就直接安装了python34；

但今天发现了一个问题，代码如下：

    Python 3.4.8 (default, Mar 23 2018, 10:04:27)
    
    [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
    
    Type "help", "copyright", "credits" or "license" for more information.
       
        >>> import json
       
        >>> s = b'{}'
       
        >>> s = b'{"a": 1, "b": 2}'
       
        >>> json.loads(s)
    
    Traceback (most recent call last):
        
        File "<stdin>", line 1, in <module>
        
        File "/usr/lib64/python3.4/json/__init__.py", line 312, in loads
        
        s.__class__.__name__))
    
    TypeError: the JSON object must be str, not 'bytes'

但在自己的电脑下面执行没有问题。看了一下环境，本机是python36，所以环境要升级。但是yum的源没有python36。只能添加源了

    #安装EPEL依赖
    sudo yum install epel-release

    #安装IUS软件源
    sudo yum install https://centos7.iuscommunity.org/ius-release.rpm

    #安装python36
    sudo yum install python36u

剩下的就是安装pip3，然后安装依赖了
