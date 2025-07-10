+++
title = "ubuntu9.04编译安装libmemcache1.4.0.rc"
date = 2009-06-15

[taxonomies]
categories = ["Tech"]
tags = ["Ubuntu"]
+++

在python下面使用memcached确实为难了我一阵子。

原以为有过java下面使用memcached的经验，会很快。不过，我确实想错了。

我来说说吧。


- 安装memcached，这个没有什么好说的。直接下载，然后./configrue &amp;&amp; make, 再make install 就好了。这里主要要说的是memcache的客户端安装。目前，python世界中使用的比价多的是，python-memcached和cmemcache

- 使用python-memcached，这个由于使用纯的Python编写。所以，下载后直接python setup.py install就可以了。这个也不是重点。重点是下面这个。

- 使用cmemcache, 为什么用它，原因是他使用了c来封装，然后由py来调用。据网上的评测文章，cmemcache的速度是python-memcached的2倍之多。所以，我打算用它。这个库依赖于libmemcache。就是这个东西难到了我。


下面具体说说：

- 下载libmemcache和cmemcache，直接安装，发现没有任何问题。但是，一旦在python中调用：

    import cmemcache

 就会出现如下错误：

    undefined symbol: mcm_buf_len

查了很多文章，原来需要为libmemecache1.4打patch

- 后来，找到一个 patch 后，放到libmemcache目录下执行:

    patch -p1 < libmemcache.patch

patch后，在执行 ./configure && make，这时候，会发现libmemcache无法make。原来是automake的问题。于是，又安装automake1.9。
 
- 接着make。又出来了问题。

    libtool: compile: cannot determine name of library object from `': not found

于是又执行：

    autoreconf -fiv

然后再make，终于通过了。然后在make install安装好。
 
这个东西把我郁闷坏了。
 
后来问同事。才发现，现在已经有一个libmemcache2了。可是，我在网上没有找到。用aptitude search也没有找到。可是，同事那确实能找到。估计是apt-source的问题了。这个就不再追究了。
 
接下来，我得看看，这两者的效率比较。网上的自我感觉还是不靠普。c的和python的代码只有2倍的差距？

 
