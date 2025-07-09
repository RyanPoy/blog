+++
title = "mac下面用brew安装nginx-full"
date = 2018-12-05
categories = ["Tech"]
tags = ["环境安装"]
+++

最近有一个项目，使用了jquery-upload进行文件上传。而nginx需要试用nginx-upload-module 和 nginx-upload-progress-module 来提供上传进度，以保证良好的用户体验；

在服务端还好，因为nginx是编译安装的，所以，直接编译的时候加入这两个module就ok了。

但本地是mac环境。用brew安装的nginx。所以，安装对应的module比较麻烦。

查了一下，可以用brew install nginx-full 来解决。但实际执行的时候，是有问题的。因为nginx-full不存在

为了解决它，又去github上找。终于找到了解决方案。

    brew tap denji/nginx

    brew install nginx-full --with-upload-module --with-upload-progress-module

[具体可以点击这里](https://github.com/denji/homebrew-nginx)
