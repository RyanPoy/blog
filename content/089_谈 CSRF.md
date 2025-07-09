+++
title = "谈 CSRF"
date = 2012-12-10
categories = ["Tech"]
tags = ["安全"]
+++

###csrf是什么
csrf 简单的说就是以跨域的方式，利用你正常的cookie，修改你在website上的数据。

举一个例子：

1. 当你正常登陆www.xxx.com。xxx.com会记录一个cookie到你的client端。表示，你现在已经正常登陆过了。

2. 然后你访问一个恶意网站，www.evil.com, evil.com有一个链接，会提交一个post请求到xxx.com，修改你在xxx.com上的密码

###如果防止csrf攻击

- 验证 HTTP Referer
  
  利用HTTP Referer字段，并且进行验证，这样只允许xxx.com的referer进行修改密码修改操作。

   > 优点：简单

   > 缺点：对于一些低版本的Browser，例如：IE6。 HTTP Referer可以进行伪造。所以不安全

- 验证token
  
  要求提交上来的请求携带一个加密的token，利用这个token进行服务器端的校验。从而防止csrf攻击

   > 优点：比较安全

   > 缺点：代码有一定的变动

- 在HTTP的HEADER里面加入一个校验的token

   本质上，和第2种是一样的。但是由于在HEADER中，所以得采用AJAX
 
   > 优点：比较安全

   > 缺点：代码变化非常大


综上考虑，采用第2中方式最靠谱。但是如果你的页面全部都是AJAX请求，那么第3种更加靠谱。

不过，不管怎么样，后端都需要写一个filter，用来校验这个token


   
