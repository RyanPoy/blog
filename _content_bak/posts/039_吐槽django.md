+++
title = "吐槽django"
date = 2010-09-06

categories = ["Tech"]
tags = ["Django"]
+++

__form__

1. 很鸡肋，简单的还行，但是复杂的很难写好。

2. 这东西本来就是页面上的，应该是html来写，非要服务器端生成，这就是画蛇添足

__model__

1. 无法migration，虽然有south，但是也经常出错

2. 对于动态语言的model，可以rich domain的。但是，django中确不是一个好的做法。

3. 对于model的更多的操作，倾向于写在ModelMananger里面

4. 由于 form 的存在，使得 model 的地位下降的，不符合 Domain Driven Development

__template__

1. 太简单，连 {% elif %} 的标签都没有，严重吐槽

2. 到处充斥了filter

3. 性能确实一般

4. 总体说来，考虑用jinja代替

__view__

1. 简单的function，连class都不是，情何以堪

__url__

1. 简单的tuple映射，无法像rails那样做到智能化

__总结__

Django做为一个一站式解决方案，要走的路还很长，希望它能更快，更好的发展下去



