+++
title = "mysql的loaddata加载数据的方式"
date = 2008-09-21

categories = ["Tech"]
tags = ["MySQL"]
+++

经常先进入mysql的命令行，然后用source命令导入内容。当数据量达到一定程度，就会变得很慢。所以，采用了loaddata这种方式。

进入数据库，敲入：
```sql
load data local infile 'd:\loaddata.txt' into table detail fields terminated by ',' LINES terminated by '\n';
```

- 'd:\loaddata.txt'：表示 loaddata.txt 的绝对路径
- ','： 表示字段之间按照','分割。
- '\n'：表示记录之间以'\n'分割。即：1行1条记录

