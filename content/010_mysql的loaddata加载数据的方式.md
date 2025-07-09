+++
title = "mysql的loaddata加载数据的方式"
date = 2008-09-21
categories = ["Tech"]
tags = ["MySQL"]
+++

此为我目前测试几个方法后的mysql添加记录的最快方式。特此记录。

之所以用到了这种方式，源于一个采集系统。每天的采集记录条数达到7kw条。1条条的加载很慢。加载速度跟不上采集速度。所以，采用了这种方式。

进入数据库，敲入：

    load data local infile 'd:\loaddata.txt' into table detail fields terminated by ',' LINES terminated by '\n';


- ''d:\loaddata.txt'  -------- 表示 loaddata.txt 的绝对路径

- ','                         -------- 表示字段之间按照','分割。

- '\n' 表示                -------- 表示记录之间以'\n'分割。即：1行1条记录

