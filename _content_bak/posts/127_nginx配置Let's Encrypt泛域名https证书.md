+++
title = "nginx配置Let's Encrypt泛域名https证书"
date = 2019-12-05

[taxonomies]
categories = ["Tech"]
tags = ["环境安装", "https", "http"]
+++

# 初衷
全球对于WEB的安全要求越来越高，所以需要把HTTP修改为HTTPS的支持。如果不支持HTTPS访问，IOS的APP就没法正常工作。同时，浏览器页会在地址栏上面标识一个『不安全的访问』的显示。为此，我也把blog网站升级了HTTPS。

# HTTPS
什么是HTTPS呢？简单的可以认为是 HTTP + SSL的组合。其工作原理如图（此图来源于网络）：
![https简单工作原理图](/static/media/https简单工作原理图.jpeg)

从上图可以看出HTTPS是有加密传输的，从而保证网络的传输数据不会倍篡改。所以，它相对HTTP是安全的。
另外从图上可以看出，请求1）https连接的时候，服务端会返回一个证书。我们把这个证书简称为https证书，而这个也就是今天要讲的重点了。

# 免费证书
HTTPS证书因为之前都是为企业而使用，所以几乎都是需要收费的。但是由于目前的安全趋势要求普及HTTPS。所以，个人HTTPS证书的需求量就陡增。但为了个人HTTPS证书，而交一笔费用是不划算的，更何况每次证书过期后得再重交。所以，免费的https证书对于个人而言，就变得很重要的。

# 泛域名支持
大家都知道，一个站点很多情况下，都会使用多个独立域名。例如：

- 搜狐主站：www.sohu.com
- 搜狐汽车：auto.sohu.com
- 搜狐邮箱：mail.sohu.com

其目的有很多。其中有一个重要的目的是为了更加方便的维护和管理站点。

但这种形式，使得每个域名需要申请1个HTTPS证书，从而需要申请多个HTTPS证书。于是，成本就高了。

那么我们来看一下，就会发现 上述域名遵循着一个规律：*.sohu.com。而这个，就是泛域名了。

是的，聪明的你，应该已经想到了，只要有一个支持泛域名的https证书，就能解决成本问题了。

于是，我们的诉求变成了寻找1个**免费+泛域名支持**的https证书

# 免费+泛域名支持
https证书服务提供商有很多，但综合来看，目前流行的是：

1. Let's Encrypt SSL 证书
2. Symantec DV SSL 证书

至于国内的各种云，例如：阿里云，腾讯云，七牛云，其实都是代理的 Symantec DV SSL 证书。本质上来说，就是2道贩子。

本着要**免费+泛域名支持**。所以，最后选择了 Let's Encrypt SSL 证书。但是有效期是90天。不过还好，实在不行就写1个crontab，每月更新一下就OK了。

# 安装 Let's Encrypt SSL 证书
Let's Encrypt 提供了一套完整的脚本服务。只要服务器安装了python即可。一般说来，都会安装的。

步骤如下：

### 1. 获取 Let's Encrypt 客户端

```
wget -c https://dl.eff.org/certbot-auto -P /usr/local/bin/
```

这个命令执行完毕后，你就能执行**certbot-auto**命令了。但是我嫌名字太长，所以做了一个软链

```
ln -s /usr/local/bin/certbot-auto /usr/local/bin/certbot 
```
这样，就可以使用 **certbot** 命令


### 2. 申请证书

```
certbot certonly  -d *.ryanpoy.com --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```

会给出下面的提示：

```
Bootstrapping dependencies for RedHat-based OSes... (you can skip this with --no-bootstrap)
yum 是 /bin/yum
yum 已被哈希 (/bin/yum)
已加载插件：fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirrors.cloud.aliyuncs.com
 * extras: mirrors.cloud.aliyuncs.com
 * updates: mirrors.cloud.aliyuncs.com
软件包 gcc-4.8.5-39.el7.x86_64 已安装并且是最新版本
软件包 augeas-libs-1.4.0-9.el7.x86_64 已安装并且是最新版本
软件包 1:openssl-1.0.2k-19.el7.x86_64 已安装并且是最新版本
软件包 1:openssl-devel-1.0.2k-19.el7.x86_64 已安装并且是最新版本
软件包 libffi-devel-3.0.13-18.el7.x86_64 已安装并且是最新版本
软件包 redhat-rpm-config-9.1.0-88.el7.centos.noarch 已安装并且是最新版本
软件包 ca-certificates-2018.2.22-70.0.el7_5.noarch 已安装并且是最新版本
软件包 python-devel-2.7.5-86.el7.x86_64 已安装并且是最新版本
软件包 python-virtualenv-15.1.0-2.el7.noarch 已安装并且是最新版本
软件包 python-tools-2.7.5-86.el7.x86_64 已安装并且是最新版本
软件包 python2-pip-8.1.2-10.el7.noarch 已安装并且是最新版本
无须任何处理
Creating virtual environment...
Installing Python packages...
Installation succeeded.
```
上述提示取决于额certbot和python的版本，不一定都会出来。

再接下来，就会进入关键环节了。

```
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator manual, Installer None
Enter email address (used for urgent renewal and security notices) (Enter 'c' to
cancel): ryanpoy@163.com # 用户安全以及续订证书的邮箱地址

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
agree in order to register with the ACME server at
https://acme-v02.api.letsencrypt.org/directory
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(A)gree/(C)ancel: A # 是否同意相关协议

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing to share your email address with the Electronic Frontier
Foundation, a founding partner of the Let's Encrypt project and the non-profit
organization that develops Certbot? We'd like to send you email about our work
encrypting the web, EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: N  # 是否订阅相关通知
Obtaining a new certificate
Performing the following challenges:
dns-01 challenge for ryanpoy.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NOTE: The IP of this machine will be publicly logged as having requested this
certificate. If you're running certbot in manual mode on a machine that is not
your server, please ensure you're okay with that.

Are you OK with your IP being logged?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Y  # 是否对域名和机器IP进行绑定
```

以上的全部选择完毕后，会提示：

```
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please deploy a DNS TXT record under the name
_acme-challenge.ryanpoy.com with the following value:

muLig-mZWAKM-FG7bRe1r9W5DZKVAP6ygsEHjFJrwl4

Before continuing, verify the record is deployed.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Press Enter to Continue
```
意思是要配置1条DNS的TXT解析记录，把 **_acme-challenge.ryanpoy.com** 解析为 **muLig-mZWAKM-FG7bRe1r9W5DZKVAP6ygsEHjFJrwl4**

>
> 这里需要注意：
> 再次DNS的TXT解析没有生效前，不要有任何操作。

然后去域名商的管理系统里面，进行对应的DNS配置。并直到生效。当生效后，可以敲下回车了。然后给出对应的提示：

```
Waiting for verification...
Challenge failed for domain ryanpoy.com
dns-01 challenge for ryanpoy.com
Cleaning up challenges
Some challenges have failed.

IMPORTANT NOTES:
 - The following errors were reported by the server:

   Domain: ryanpoy.com
   Type:   dns
   Detail: DNS problem: NXDOMAIN looking up TXT for
   _acme-challenge.ryanpoy.com
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
```

此时证书已经申请完毕。

### 3. Nginx配置
由于我一直用Nginx做负载均衡。所以，还需要对Nginx进行对应的配置，让其支持Https。

这个也简单，因为 Let's Encrypt 同样提供了命令。具体为：

```
certbot install --nginx --nginx-server-root /etc/nginx --nginx-ctl /usr/sbin/nginx
```
>注意
> 
> /etc/nginx 是nginx配置目录
> 
> /usr/sbin/nginx  是nginx的2进制执行文件位置
 

然后就按照提示一步一步来就OK了。这里比较简单，大致就是

- 选择要走https的域名
- 是否把80(http)端口强制跳转到443(https)

具体的步骤我就不写了。当你按照提示一步一步的执行后，nginx的配置文件会自动被修改。完毕后，重启nginx即可支持HTTPS了。

> 注意
> 
> nginx重启后，还需要修改服务器的防火墙设置，保证443端口是能被访问的
> 

### 自动更新证书

由于证书的有效期是90天，为了避免每次都需要人肉更新。所以，采用了crontab来进行自动化处理。主要就是执行
```
certbot renew --cert-name ryanpoy.com 
```
不过这里有一个问题，每次更新后，都需要重新设置dns的解析。如果你的域名提供商不支持自动设置dns规则，那么就必须手动操作了。恰好，阿里云就不支持。后续我会写1个关于阿里云自动化更新证书的方式。
