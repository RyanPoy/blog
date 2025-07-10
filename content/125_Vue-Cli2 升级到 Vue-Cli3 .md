+++
title = "Vue-Cli2 升级到 Vue-Cli3 "
date = 2018-12-05

[taxonomies]
categories = ["Tech"]
tags = ["Vuejs"]
+++

标题党一回。其实升级很简单，就是卸载旧的2.x版本，重装新的3.x版本。

升级之后，实测，原来在2.x下面建立的老项目跑不起来。需要修改。

我的修改方法比较呆板。例如：原来的项目ProjectName

* 备份一个 ProjectName.bak；
* 创建项目：vue create ProjectName
* 把ProjectName.bak 里面有用的部分覆盖到 ProjectName 里面去

要注意的：
> 原来的config 目录已经没有了。所以相关的配置，需要放到vue.config.js里面。但vue.config.js不是默认就存在的，需要手动创建。
> 原来做研发的时候，为了解决跨域，需要在config/dev.js 用 proxyTable，现在直接在vue.config.js叫做 proxy了。
> 关于assert打包位置，可以在 vue.config.js 里面配置 assetsDir，例如：assetsDir='static/admin'
> vue.config.js里面的productSourceMap， 可以设置为false，感觉用处不大

执行的时候，会发现报错，一般都很容易解决。只有一个问题。
```
You are using the runtime-only build of Vue where the template compiler is not available. Either pre-compile the templates into render functions, or use the compiler-included build.
```
找了一些资料，后来发现，是因为在App.vue 的 <script></script> 里面没有任何的内容，是空标签。

只需要在里面加入 ：
```
export default {}
```
最终就可以执行了。
