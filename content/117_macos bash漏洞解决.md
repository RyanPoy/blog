+++
title = "macos bash漏洞解决"
date = 2014-09-29

[taxonomies]
categories = ["Tech"]
tags = ["安全"]
+++

最近炒得很火的 bash 漏洞，想必大家都知道了。

如果，你也是用bash，那么请执行：

    env VAR='() { :;}; echo Bash is vulnerable!' bash -c "echo Bash Test"

如果输出结果为：

    Bash is vulnerable!
    Bash Test

那么恭喜你，你中招了。这时候，你要做的就是干净安装补丁。对于一般的linux来说，直接用系统的包管理，升级bash就ok了。例如：

- centos: yum update
- ubuntu: apt-get update

但是，对于macos，貌似，苹果公司还没有给出补丁。所以，只能是手动升级了。

如果你使用的时brew，请执行：
    
    brew update
    brew upgrade bash

如果是系统自带的，那么请按照下面的方式执行：

    mkdir bash-fix
    cd bash-fix
    curl https://opensource.apple.com/tarballs/bash/bash-92.tar.gz | tar zxf -
    cd bash-92/bash-3.2
    curl https://ftp.gnu.org/pub/gnu/bash/bash-3.2-patches/bash32-052 | patch -p0
    cd ..
    xcodebuild
    sudo cp /bin/bash /bin/bash.origin
    sudo cp /bin/sh /bin/sh.origin
    sudo cp build/Release/bash /bin
    sudo cp build/Release/sh /bin

验证是否成功，请再次执行：

    env VAR='() { :;}; echo Bash is vulnerable!' bash -c "echo Bash Test"

如果只出现：

    Bash Test

你就安装成功了。


     
