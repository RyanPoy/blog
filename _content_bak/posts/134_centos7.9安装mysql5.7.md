+++
title = "centos7.9安装mysql5.7"
date = 2021-12-30

categories = ["Tech"]
tags = ["MySQL", "环境安装"]
+++

最近在一台centos7.9的服务器上装mysql。现在记录下来，方便以后查找。

## yum更新mysql源
  
因为yum默认是mariadb，所以，需要更新yum的mysql源

具体如下：

- `wget https://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm`

- `yum install -y mysql57-community-release-el7-10.noarch.rpm`

## yum 安装并启动mysql
 
- `yum install mysql`

- `systemctl start mysqld`

## 更新mysql的root密码

mysql安装完毕后，会给一个随机密码，具体可以通过执行 `grep 'password' /var/log/mysqld.log` 可以看到。

通过mysql -uroot -p 登录成功后，执行 `alter user root@'localhost' identified by 'new-password';` 就修改新的root密码了

## 重新指定mysql的数据库位置

下面我们需要重新制定mysql数据库的位置。因为默认mysql数据库是在 /var/lib/mysql 目录下面 。而服务器的/var/lib/mysql一般没有多大空间。所以，我们把数据库位置放到 /data/lib/mysql上来。
- 关闭mysql：`systemctl stop mysqld`

- 创建目标目录：`mkdir /data/lib`

- 把mysql目录转移到目标目录：`mv /var/lib/mysql /data/lib`

- 修改mysql配置：`vim /etc/my.cnf`，把里面的/var/lib/mysql 修改为 /data/lib/mysql

## 进一步排查错误

按道理说该修改的都完成了，但是当我们重新启动mysql时候： systemctl start mysqld ，系统报错：

Job for mysqld.service failed because the control process exited with error code. See "systemctl status mysqld.service" and "journalctl -xe" for details.

如果使用如下命令查看

service mysqld  status

会得到如下错误信息

Redirecting to /bin/systemctl status  mysqld.service

这个时候，我们需要做下面的步骤来进行对应的修改：

`vim /etc/selinux/config`。并修改 selinux=disabled，重新启动系统。

## 再重启mysql

systemctl start mysqld

这时候就发现启动成功了
