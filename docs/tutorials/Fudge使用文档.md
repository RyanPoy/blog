---
title: Fudge使用文档
date: 2012-10-20

category: Tutorials
tags: [Python, Fudge]
---

fudge是一个python的mock框架，我非常喜欢它。决定把使用文档翻译出来。

<!--more-->

## Fudging a Web Service
当测试一个使用web服务的代码时，你可能想快速的设置一个不依赖于真实的在互联网上的web服务。这是一个使用mock对象的好的方式。假设你又一个Twitter的机器人，看起来像这样：

```Python
>>> import oauthtwitter
>>> def post_msg_to_twitter(msg):
...     api = oauthtwitter.OAuthApi(
...         '<consumer_key>', '<consumer_secret>',
...         '<oauth_token>', '<oauth_token_secret>'
...     )
...     api.UpdateStatus(msg)
...     print "Sent: %s" % msg
>>>
```

因为[oauthtwitter][1]是独立维护的，你的代码只要调用了正确的方法，就能正常工作。

## A Simple TestCase
你可以使用一个假的声明的期望的class来代替OAuthApi的class，它这样用：

```python
>>> import fudge
>>> @fudge.patch('oauthtwitter.OAuthApi')
... def test(FakeOAuthApi):
...     (FakeOAuthApi.expects_call()
...                  .with_args('<consumer_key>', '<consumer_secret>',
...                             '<oauth_token>', '<oauth_token_secret>')
...                  .returns_fake()
...                  .expects('UpdateStatus').with_arg_count(1))
...
...     post_msg_to_twitter("hey there fellow testing freaks!")
>>>
```

让我们来分解一下：
1. 测试阶段，patch装饰器将用一个假的对象临时的打一个补丁。并且使它作为一个参数，传入到测试方法中。这允许你添加你所想要的东西。
1. 这里你看到的这个fake对象，期望有一个方法被调用，这个方法使用4个指定的字符串作为参数。它返回了一个对象实例(一个新的fake对象)，它希望你使用一个参数调用fake_oauth.UpdateStatus()
1. 最后, post_msg_to_twitter() 被调用。让我们运行测试！

```python
>>> test()
Sent: hey there fellow testing freaks!
```
很高兴，它通过了。

Fudge让你声明了你想要的或松散或紧密的期望(expectations)。如果你不关心确切的参数，你可以不调用fudge.Fake.with_args()。如果你不关心方法是不是真的被调用，你可以用fudge.Fake.provides()来代替fudge.Fake.expects()。同样的，当你不想为真实的参数值而操心，可以使用fudge.Fake.with_arg_count()。在其它方面有检测者，检测参数的值。
  
  [1]: http://code.google.com/p/oauth-python-twitter/

## Fake objects without patches (dependency injection)
如果你不需要任何补丁，你可以使用fudge.test()装饰器。这将捕获任何一个被抛出的非预期的异常。这是一个例子：

```python
>>> def send_msg(api):
...     if False: # a mistake
...         api.UpdateStatus('hello')
...
>>> @fudge.test
... def test_msg():
...     FakeOAuthApi = (fudge.Fake('OAuthApi')
...                          .is_callable()
...                          .expects('UpdateStatus'))
...     api = FakeOAuthApi()
...     send_msg(api)
...
>>> test_msg()
Traceback (most recent call last):
...
AssertionError: fake:OAuthApi.UpdateStatus() was not called
```

## Stubs Without Expectations
如果你想要一个fake对象，可以被调用但是它不是一定被调用，除了用Fake.provides()代替Fake.expects()外，代码完全一样。这是一个调用is_logged_in()永远返回True的例子：

```python
>>> def show_secret_word():
...     import auth
...     user = auth.current_user()
...     if user.is_logged_in():
...         print "Bird is the word"
...     else:
...         print "Access denied"
...
>>> @fudge.patch('auth.current_user')
... def test_secret_word(current_user):
...     user = current_user.expects_call().returns_fake()
...     user = user.provides('is_logged_in').returns(True)
...     show_secret_word()
...
>>> test_secret_word()
Bird is the word
```
注意，如果user.is_logged_in()没有被调用，不会有任何的异常被抛出。因为它是'提供'(provided)，不是'期望'(expected)。

## Replacing A Method
有时候，返回一个静态的值不是完全足够的。你真正需要运行一些代码。你可以使用Fake.calls()，就像这样：

```python
>>> auth = fudge.Fake()
>>> def check_user(username):
...     if username=='bert':
...         print "Bird is the word"
...     else:
...         print "Access denied"
...
>>> auth = auth.provides('show_secret_word_for_user').call(check_user)
>>> # Now, the check_user function gets called instead:
>>> auth.show_secret_word_for_user("bert")
Bird is the word
>>> auth.show_secret_word_for_user("ernie")
Access denied
```

## Cascading Objects
你可能想让一些对象用长的链式的工作。这有一个使用fudging [SQLAlchemy级联查询][1]的例子。注意 Fake.returns_fake() 指定于session.query(User)返回一个新的对象。同样注意因为query()返回一个迭代器，它设置返回一个fake用户对象的列表。

```python
>>> import fudge
>>> session = fudge.Fake('session')
>>> query = (session.provides('query')
...                 .returns_fake()
...                 .provides('order_by')
...                 .returns(
...                     [fudge.Fake('User').has_attr(name='Al', lastname='Capone')]
...                 )
... )
>>> from models import User
>>> for instance in session.query(User).order_by(User.id):
...     print instance.name, instance.lastname
...
Al Capone
```

## Multiple Return Values
我们说，你想测试需要调用多次和返回多个结果的代码。到现在，你仅仅看到Fake.returns()方法将返回一个无穷值(value infinitely)。要改变它，调用To change that, 调用Fake.next_call()可以指定调用顺序。这是一个购物车场景的例子:

```python
>>> cart = (fudge.Fake('cart')
...              .provides('add')
...              .with_args('book')
...              .returns({'contents': ['book']})
...              .next_call()
...              .with_args('dvd')
...              .returns({'contents': ['book', 'dvd']}))
>>> cart.add('book')
{'contents': ['book']}
>>> cart.add('dvd')
{'contents': ['book', 'dvd']}
>>> cart.add('monkey')
Traceback (most recent call last):
...
AssertionError: This attribute of fake:cart can only be called 2 time(s).
```

## Expecting A Specific Call Order
你可能需要测试一个对象，预计它在一个特定的顺序中作为一个方法被调用。仅仅在调用fudge.Fake.expects()之前带使用fudge.Fake.remember_order()，就像这样:

```python
>>> import fudge
>>> session = (fudge.Fake("session").remember_order()
...                                 .expects("get_count").returns(0)
...                                 .expects("set_count").with_args(5)
...                                 .expects("get_count").returns(5))
...
>>> session.get_count()
0
>>> session.set_count(5)
>>> session.get_count()
5
>>> fudge.verify()
```

如果你没有按照顺序调用，讲输出一个描述性的错误。

```python
>>> session.set_count(5)
Traceback (most recent call last):
...
AssertionError: Call #1 was fake:session.set_count(5); Expected: #1 fake:session.get_count()[0], #2 fake:session.set_count(5), #3 fake:session.get_count()[1], end
```
  [1]: http://www.sqlalchemy.org/docs/05/ormtutorial.html#querying

## Allowing any call or attribute (a complete stub)

如果你需要一个对象，延迟提供任何调用或者任何属性，你可以声明fudge.Fake.is_a_stub()。任何被请求的方法或者属性将永远返回一个新的fudge.Fake实例，使其更加容易的工作在复杂的对象上。这有一个例子：

```python
>>> Server = fudge.Fake('xmlrpclib.Server').is_a_stub()
>>> pypi = Server('http://pypi.python.org/pypi')
>>> pypi.list_packages()
fake:xmlrpclib.Server().list_packages()
>>> pypi.package_releases()
fake:xmlrpclib.Server().package_releases()
```
Stubs像这样无限的进行。

```python
>>> f = fudge.Fake('base').is_a_stub()
>>> f.one.two.three().four
fake:base.one.two.three().four
```
> 注意当使用fudge.Fake.is_a_stub()，你不能延迟访问任何有相同名字的属性或者方法，像returns()或者with_args()。你需要直接使用fudge.expects()等，来声明一个预期。


## Working with Arguments
fudge.Fake.with_args() 方法可以随意的允许你声明怎样传递参数到你的对象的预期。对于一个预期的确定的参数值，它通常就足够了。但是有时候你需要为动态的参数值使用fudge.inspector方法。

这有一个短的例子：

```python
>>> import fudge
>>> from fudge.inspector import arg
>>> image = (fudge.Fake("image")
...               .expects("save")
...               .with_args("JPEG", arg.endswith(".jpg"), resolution=arg.any())
... )
```

这个声明十分的灵活；它允许下面这样的调用：

```python
>>> image.save("JPEG", "/tmp/unicorns-and-rainbows.jpg", resolution=72)
>>> image.save("JPEG", "/tmp/me-being-serious.jpg", resolution=96)
```

这就是Fudge！更多的细节请看fudge的API：

- [fudge][1]
- [fudge.inspector][2]
- [fudge.patcher][3]

  [1]: http://farmdev.com/projects/fudge/api/fudge.html
  [2]: http://farmdev.com/projects/fudge/api/fudge.inspector.html
  [3]: http://farmdev.com/projects/fudge/api/fudge.patcher.html
