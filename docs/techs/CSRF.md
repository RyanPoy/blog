---
title: 谈CSRF
date: 2012-12-10

category: Tech
tags: [CSRF]
---

## csrf是什么
csrf 简单的说就是以跨域的方式，利用你正常的cookie，修改你在website上的数据。举一个例子：
1. 当你正常登陆www.xxx.com。xxx.com会记录一个cookie到你的client端。表示，你现在已经正常登陆过了。
2. 然后你访问一个恶意网站，www.evil.com, evil.com有一个链接，会提交一个post请求到xxx.com，修改你在xxx.com上的密码

<!--more-->

## 如果防止csrf攻击
1. 验证HTTP Referer

利用HTTP Referer字段，并且进行验证，这样只允许xxx.com的referer进行修改密码修改操作。虽然简单，但是对于一些低版本的Browser，例如：IE6。 HTTP Referer可以进行伪造。所以不安全。

2. 验证token

  - 要求提交上来的请求携带一个加密的token，利用这个token进行服务器端的校验。从而防止csrf攻击。比较安全，但是需要变动一定的代码。

  - 在HTTP的HEADER里面加入一个校验的token。但是由于在HEADER中，所以得采用AJAX。也比较安全，但是代码变化非常大

## 结论
综上考虑，正常采用第2中方式最靠谱。不过，注意后端都需要写一个filter，用来校验这个token


   
