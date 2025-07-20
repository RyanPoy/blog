---
title: mysql的loaddata加载数据的方式
date: 2008-09-21

category: Tech
tags: [MySQL]
---

LOAD DATA 是 MySQL 中用于 高效批量导入数据 的命令，适合把 CSV 或 TSV 文件中的数据直接加载到表中，速度远远高于逐条插入（INSERT）。

<!---->

进入数据库，敲入：
```sql
load data local infile 'd:\loaddata.txt' into table detail fields terminated by ',' LINES terminated by '\n';
```

- 'd:\loaddata.txt'：表示 loaddata.txt 的绝对路径
- ','： 表示字段之间按照','分割。
- '\n'：表示记录之间以'\n'分割。即：1行1条记录

