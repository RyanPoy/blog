+++
title = "pypy环境的gevent开发 (gevent on pypy)"
date = 2014-08-20
categories = ["Tech"]
tags = ["Python", "Gevent", "Pypy"]
+++

## install pypy

- wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.3.1-linux_x86_64-portable.tar.bz2
- bunzip2 pypy-2.3.1-linux_x86_64-portable.tar.bz2
- tar -xvf pypy-2.3.1-linux_x86_64-portable.tar
- mv pypy3-2.3.1-linux_x86_64-portable pypy-2.3.1
- ln -s pypy-2.3.1/bin/pypy /usr/bin/pypy

## install system enviaronment

- yum install --enablerepo=epel libev.x86_64
- yum install --enablerepo=epel libev-devel.x86_64
 
> must add --enablerepo=epel when install libev on amazon ec2，because there is not libev source in ec2's yum. 

if the libev can not install. you can make it by yourself.

## install system enviaronment by yourself

- wget http://dist.schmorp.de/libev/libev-4.15.tar.gz
- tar -xvf libev-4.15.tar.gz
- cd libev-4.15
- ./configuration
- make
- make install



## creat the pypy virtual enviaronment for development

- cd pypy-2.3.1
- bin/virtualenv-pypy ~/PypyEnv
- cd ~/PypyEnv
- source bin/activate
- pip install gevent
- pip install git+git://github.com/schmir/gevent@pypy-hacks
- pip install cffi
- pip install git+git://github.com/gevent-on-pypy/pypycore
- export GEVENT_LOOP=pypycore.loop

> If setup.py complains it can not locate ev.h it's possible the library search path isn't complete.  In that case add the directory containing ev.h to the include_dirs variable in pypycore.py (line 215). The result would look similar to example:

```

""", include_dirs=[include_dir,"/usr/include/libev"], libraries=["ev"])


## some anontations

- write the gevent code, must write the code in first line.

```

    # coding: utf8
    import sys
    import gevent
    if "__pypy__" in sys.builtin_module_names:

      def _reuse(self):
        self._sock._reuse()    
      def _drop(self):
        self._sock._drop()
      gevent.socket.socket._reuse = _reuse
      gevent.socket.socket._drop = _drop


- start the gevent server. must run it:

```

     export GEVENT_LOOP=pypycore.loop


