---
title: 网页解析
date: 2011-02-27

category: Tech
tags: [Python, Crawler]
---

对于crawler, parse html 是一个必不可少的工作。现阶段有很多的开源库，python中也有自己的标准库。都是为了方便的解析html的。但是，由于我们的需求可能会变得很奇怪，比方说：对于script的东西也许也要解析。对于comment的东西可能也要分析。或者，还有其它的需求。为此，我重新造个轮子。

<!--more-->

核心要求：
1. html 由 标签，内容组成
2. 标签由标签名，attr=value 的属性对组成
3. 标签可以是自关闭的，也可以显示关闭的，有些标签只有1个。有些是1对
4. 对于<!-- --> 也可以当成是特殊的标签
5. 同理，<script></script> 也是特殊的标签
6. 对于文本，其实也是一个特殊的标签，可以隐式的认为name='', attr=''
7. 所以 需要有：
  - 解析标签的工具
  - 遍历网页，找出标签的东西
  - 找出标签，并且解析后，存放解析后的数据的东西


接下来，讲讲如何进行网页里面标签块的解析。例如，我们要解析下面的内容：
```html
<a href='#' class="anavy">
```

其实就是要解析出里面的**href**和**class**分别是什么。不过，要注意下面的几点：
1. 可以检查标签是否可见，这个有利于以后的html分析，从而知道这个内容是否要显示出来
2. 支持不规范的标签，比方说只有开，没有闭；少一个空格 等等

直接上代码：
**html_util.py**
```python
#coding=utf-8
class AttributeUtil(object):

    @classmethod
    def get_attribute(cls, html_string, attribute_name):
        if html_string is None:
            return None
        
        attribute_name = attribute_name.lower()

        p = cls.__find_attribute_name(html_string, attribute_name)
        if p == -1:
            return None

        p = cls.__find_char_pos(html_string, p + len(attribute_name))
        if p == -1:
            return ''

        c = html_string[p]
        if c != '=':
            return ''

        p = cls.__find_char_pos(html_string, p + 1)
        if p == -1:
            return ''

        c = html_string[p]
        if c == "'" or c == '"':
            p1 = html_string.find(c, p + 1)
            if p1 == -1:
                return ''
            return cls.__clear_return(html_string[p + 1:p1])
        
        p1 = cls.__find_blank_pos(html_string, p + 1)
        if p1 == -1:
            return html_string[p:].strip()
        
        return cls.__clear_return(html_string[p:p1].strip())


    @classmethod
    def __clear_return(cls, str):
        if str is None:
            return None

        return str.replace('\n', '').replace('\r', '')

    @classmethod
    def __find_blank_pos(cls, html_string, p):

        for i in range(p, len(html_string)):
            c = html_string[i]
            if c.isspace() or c == '/' and i == len(html_string) - 2 or c == '>' and i == len(html_string) - 1:
                return i 

        return -1

    @classmethod
    def __find_char_pos(cls, html_string, p):
        if p < 0:
            return -1
        
        for i in range(p, len(html_string)):
            if not html_string[i].isspace():
                return i
        return -1

    @classmethod
    def __find_attribute_name(cls, html_string, attribute_name):
        p = 0
        tag_string_low = html_string.lower()
        attribute_name_length = len(attribute_name)
        while True:
            p = tag_string_low.find(attribute_name, p)
            if p == -1:
                break
            if p > 0:
                c = html_string[p - 1]
                
                if c.isspace() or c == '"' or c == "'":
                    if p + attribute_name_length == len(html_string):
                        return p
                    c = html_string[p + attribute_name_length]
                    if c.isspace() or c == '=':
                        return p
                p = p + attribute_name_length
                
            if p == 0:
                c = html_string[p + attribute_name_length]
                if c.isspace() or c == '=':
                    return p
                p += attribute_name_length

        return -1
    
    @classmethod
    def get_value_in_url(url, key):
        if url is None:
            return None
        
        p = url.find('?')
        if p == -1:
            return None
        
        lower_key = key.lower()
        params = url[p + 1:].split('&')
        for param in params:
            k, v = param.split('=')
            if k.lower() == lower_key:
                return v
        
        return None

    @classmethod
    def style_visibility(cls, value):
        """
        查看是否可见，
        @return: 如果可见返回True,否则返回False
        """
        style = cls.get_attribute(value, 'style')
        if style is None:
            return True
        style = style.lower()
        p = style.find('visibility');
        if p == -1:
            return True
        
        p1 = style.find(':', p)
        if p1 == -1:
            return True
        
        p2 = style.find(';', p1)
        
        v = style[p1 + 1:] if p2 == -1 else style[p1 + 1:p2]
        
        if v == None:
            return True
        
        v = v.strip()
        
        if v == 'hidden' or v == 'false':
            return False
        return True
```

测试代码如下：
**test_html_util.py**
```python
#coding=utf-8    
import unittest
from html_util import AttributeUtil

class AttributeAnalyzerTest(unittest.TestCase):
    
    def test_style_visibility(self):
        tag_string = "<DIV ID=\"investInfo\" STYLE=\"position:absolute; width:106px; z-index:7; visibility: hiden\" onMouseOver=\"MM_showHideLayers('newsCenter','','hide','dataCenter','','hide','viewGovernment','','hide','chengxinCenter','','hide','workHall','','hide','superviseAppeal','','hide','participateGovern','','hide','investInfo','','show','serviceGuide','','hide')\"  onMouseOut=\"MM_showHideLayers('newsCenter','','hide','dataCenter','','hide','viewGovernment','','hide','chengxinCenter','','hide','workHall','','hide','superviseAppeal','','hide','participateGovern','','hide','investInfo','','hide','serviceGuide','','hide')\">"
        visibility = AttributeUtil.style_visibility(tag_string)
        self.assertTrue(visibility)
        
    def test_get_simple_attribute(self):
        tag_string = "window.location.href='bbsShowTopic.aspx?BoardID=148&Page=182'"
        value = AttributeUtil.get_attribute(tag_string, "window.location.href")
        self.assertEquals(value, 'bbsShowTopic.aspx?BoardID=148&Page=182')
    
    def test_get_none_attribute(self):
        """
        There is an error. why the result value became #"? the last version is none
        """
        value = AttributeUtil.get_attribute("<a href=#\" class=\"anavy\">", "href")
        self.assertEquals(value, '#"')
    
    def test_get_attribute_from_no_standrand_format_html(self):
        value = AttributeUtil.get_attribute("<sdgsadg witht=\"123\"src=ddsg", "src")
        self.assertEquals(value, 'ddsg')
    
    def test_get_empty_attribute_from_no_standrand_format_html(self):
        value = AttributeUtil.get_attribute("<sdgsadg src='", "src")
        self.assertEquals('', value)
        
    def test_get_upper_attribute(self):
        value = AttributeUtil.get_attribute("<sdgsadg src='SD'", "src")
        self.assertEquals('SD', value)
        
    def test_get_no_standrand_attribute(self):
        html_string = "<A class=blue href = \"http://shanghai.sohu.com/\" target=_blank>"
        value = AttributeUtil.get_attribute(html_string, "href")
        self.assertEquals(value, 'http://shanghai.sohu.com/')
    
    def test_get_attribute_with_upper_attribute_name(self):
        value = AttributeUtil.get_attribute("<sdgsadg src='SD' <aa>", "SRC")
        self.assertEquals(value, 'SD')
        
    def test_get_none_attribute_2(self):
        value = AttributeUtil.get_attribute("<script>window.location='http://www.shang360.com'</script>", "a")
        self.assertTrue(value is None)

    def test_tuge_page_fetch(self):
        value = AttributeUtil.get_attribute("<script>window.location='http://www.shang360.com'</script>", "a")
        self.assertTrue(value is None)

    def test_img_tag_and_no_standrand_attribute(self):
        tag_string = '''<IMG alt=在纽约联合国总部安理会会议厅，中国常驻联合国代表李保东 （左二） 与其他一些国家与会代表交谈。 
src="http://photocdn.sohu.com/20100610/Img272688535.jpg" align=middle>'''
        value = AttributeUtil.get_attribute(tag_string, "src")
        self.assertEquals('http://photocdn.sohu.com/20100610/Img272688535.jpg', value)
        
if __name__ == '__main__':
    unittest.main()
```

讲明了如何解析标签。接下来，我们要做的事情就是解析html的内容了。参考以往解析xml，可以采用sax的方式。这样更加清晰，代码也更加好写。

我们的设计是有一个 HtmlHandler 和 HtmlParser。有HtmlHandler里面保留html的可见内容。而HtmlParser进行真正的解析。

**html_handler.py**
```python
#coding=utf-8

class HtmlHandler(object):
    """
    拿到标签后，进行相应处理的handler
    """
    def __init__(self, handle_comment=False, handle_text=True):
        self.handle_comment = handle_comment
        self.handle_text    = handle_text
        self.script = False
        self.style  = False
        self.html_list = []
        
    def start(self, name, value, position):
        lower_name = name.lower()
        if lower_name == 'style':
            self.style = True

        if lower_name == 'script':
            self.script = True
            
    def end(self, name, value, position):
        lower_name = name.lower()
        if lower_name == 'style':
            self.style = False

        if lower_name == 'script':
            self.script = False
            
    def comment(self, text, position):
        if not self.script and not self.style:
            self.html_list.append(text)

    def text(self, text):
        if not self.script and not self.style:
            self.html_list.append(text)

    def finish(self):
        pass
    
    def get_html_exclude_script(self, connect_mark):
        return connect_mark.join(self.html_list)
    
    def clear_memory(self):
        self.html_list = []
```

上面代码中，我们通过 handler.text 方法来text的追加。最后调用get_html_exclude_script就可以拿到网页的内容了。接下来，看html_parser的逻辑。

**html_parser.py**
```python
#coding=utf-8
import re

class HtmlParser(object):
    
    def __init__(self, handler, mask=None):
        self.handler = handler
        self.mask = mask

        self.handle_text = handler.handle_text
        self.handle_comment = handler.handle_comment
        self.is_end = False
        self.tag_name = ''

        self.replace_dict = {
          '&nbsp;': ' ',
          '&amp;': '&',
          '&lt;': '<',
          '&gt;': '>',
          '&brvbar;': '?',
          '&quot;': '"',
          '&middot;': '?',
          '&bull;': '?',
          '\n': ' ',
          '\r': ' '
    }
        self.rx = re.compile('|'.join(map(re.escape, self.replace_dict)))

    def parse(self, html):
        self.handler.clear_memory()
        self.parse_html(html)
        self.handler.finish()

    def parse_html(self, html):
      if html is None:
        return

      current_tag_begin, last_tag_end = 0, 0

      while last_tag_end != -1 and last_tag_end < len(html):
        current_tag_begin = html.find('<', last_tag_end)
        if current_tag_begin == -1:
          break

        self.text(html, last_tag_end, current_tag_begin);

        p2 = self.comment(html, current_tag_begin)  # 看是不是注释
        if (p2 > 0): # 是注释
          last_tag_end = p2
          continue

        # 当'<'后面不是注释的时候，走下面的代码片断
        last_tag_end = self.check_is_end(html, current_tag_begin + 1);
        if last_tag_end == -1:  # 表示已经结束了。
          break

        last_tag_end = self.get_tag_name_position(html, last_tag_end)
        if last_tag_end < 0: # 可能是无效字符，也可能是没有关键字
          last_tag_end = current_tag_begin + 1
          if self.handle_text:
            self.handler.text("<")
          continue

        last_tag_end = self.find_tag_end(html, last_tag_end) # 找到了会返回位置
        if (last_tag_end != -1):  # 找到
          last_tag_end += 1
          if not self.in_mask():
            continue

          str = html[current_tag_begin:last_tag_end]
          if self.isEnd:
            self.handler.end(self.keyWord, str, current_tag_begin)
          else:
            self.handler.start(self.keyWord, str, current_tag_begin)
            if not ('a' == self.keyWord or 'A' == self.tag_name) and self.is_self_closed(str):
              self.handler.end(self.keyWord, str, current_tag_begin)

      if last_tag_end == -1:
        last_tag_end = current_tag_begin

      self.text(html, last_tag_end, len(html))

    def is_self_closed(self, html):
      for i in range(len(html) - 2, 0, -1):
        c = html[i]
        if not c.isspace():
          if c == '/':
            return True
          return False

      return False

    def text(self, html, last_tag_end, current_tag_begin):
      if not self.handle_text:
        return

      begin, end = -1, current_tag_begin

      for i in range(last_tag_end, current_tag_begin):
        c = html[i] # 找到第一个不是空格的位置
        if not c.isspace():
          begin = i
          break
      if begin == -1:
        return # 全部是空格，返回

      if current_tag_begin > 0:
        for i in range(current_tag_begin - 1, begin, -1):
          if not html[i].isspace():
            end = i + 1
            break

      self.handler.text(self.html_decode(html[begin:end]))

    def html_decode(self, html):
        return self.rx.sub(lambda match: self.replace_dict[match.group(0)], html)

    def comment(self, html, p):
      if html.startswith("<!--", p):
        p1 = html.find("-->", p + 2)
        if p1 == -1:
          return -1
        p1 += 3
        if self.handle_comment:
          self.handler.comment(html[p:p1], p)
        return p1

      return -1

    def in_mask(self):
      if self.keyWord is None:
        return False
      if self.mask is None:
        return True

      for x in self.mask:
        if self.keyWord == x.upper() or self.tag_name == x.lower():
          return True
      return False

      def find_tag_end(self, html, p):
      if p == -1 or p >= len(html):
        return -1
      match = '>'
      lastIsEqual = False

      for i in range(p, len(html)):
        c = html[i]
        if c == match:
          if match == '>':
            return i
          if match == "'" or match == '"':
            match = '>'
        elif (c == "'" or c == '"') and lastIsEqual:
          if match == '>':
            match = c

        if c == '=':
          lastIsEqual = True
        elif not c.isspace():
          lastIsEqual = False

      return -1

    def get_tag_name_position(self, html, p):
      self.keyWord = None
      if p == -1 or p >= len(html):
        return -1

      for i in range(p, len(html)):
        c = html[i]

        if self.is_tag_stop_flag(c):
          self.keyWord = html[p:i].lower()
          return i;  #返回关键词的节数位置

        if not self.is_tag_name_char(c, i - p):
          return -2 # 如果是错误字符(非有效字符)。
      return -1 # 表示没有关键字

    def is_tag_name_char(self, ch, i):
      if (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z'):
        return True
      if ch == '_' or ch == ':' or ch == '.':
        return True
      if i > 0 and ch >= '0' and ch <= '9':
        return True
      if i == 0 and ch == '!':
        return True
      return False

    def check_is_end(self, html, p):
      if p >= len(html):
        return -1

      for i in range(p, len(html)):
        c= html[i]
        if not c.isspace():
          if (c == '/'):
            self.isEnd = True
            return i + 1
          else:
            self.isEnd = False
            return i
      return -1

    def is_tag_stop_flag(self, c):
      if c.isspace() or c == '>' or c == '/':
        return True
      return False
```
接下来，是测试代码：

**test_parser.py**
```python
#coding=utf-8

import unittest
from time import time
from html_handler import HtmlHandler
from html_parser import HtmlParser
from html_util import AttributeUtil

class TestHandler(HtmlHandler):
    
    def __init__(self, handle_comment=False, handle_text=True):
        super(TestHandler, self).__init__(handle_comment, handle_text)
        self.anum = 0
        self.hrefs = []
        
    def start(self, name, value, p):
        print "start:name=", name, ";value=", value, ";p=", p
        if name.lower() == 'a':
            href = AttributeUtil.get_attribute(value, 'href')
            if href:
                self.hrefs.append(href.strip())
                self.anum += 1

    def end(self, name, value, p):
        print "end:name=", name, ";value=", value, ";p=", p

    def text(self, text):
        print "text:", text

    def comment(self, c, p):
        print "comment:", c

    def finish(self):
        print 'finish'
        
    def print_hrefs(self):
        for href in set(self.hrefs):
#            print href.replace("javascript:changeCity('", "http://").replace("','')", ".city8.com")
            print href
            
class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.html = """开始的文本内容<!--这是一个注释-->
<div class="colRight">
<h2><a href="http://ent.163.com/09/0901/07/5I40E0S200031H2L.html">金越任虎年春晚总导演</a></h2>
<div class="list">
<ul>
<li><a href="http://ent.163.com/09/0901/05/5I3P9S7T00031H2L.html">曾轶可《狮子座》涉嫌抄袭纯音乐《天际》</a></li>
<li><a href="http://ent.163.com/09/0901/07/5I41RRCR00031H2L.html">金马奖报名截止 郭富城刘德华黎明争夺影帝</a></li>
<li><a href="http://ent.163.com/09/0901/04/5I3LJ0QE00031H2L.html">赵雅芝准备接演古董收藏剧 支持阿娇演白娘子</a></li>
<li><a href="http://ent.163.com/09/0901/03/5I3I031200032DGD.html">李玟:与男友前妻成了姐妹 暂时没时间结婚</a></li>
<li><a href="http://ent.163.com/09/0901/02/5I3E96TU00032KMI.html">潘粤明:已经在蜜罐里 有信心与董洁白头偕老</a></li>
</ul>
中间的文本内容
<ul class="line">
<li><a href="http://ent.163.com/09/0901/05/5I3OPHO600031H2L.html">《气喘吁吁》被批“难看” 葛优票房神话难续</a></li>
<li><a href="http://ent.163.com/09/0901/02/5I3FAUL000032KMI.html">关锦鹏：梁朝伟斗心强  张曼玉曾苦练走路</a></li>
<li><a href="http://ent.163.com/09/0901/06/5I3V00IF00031H2L.html">郁可唯成长经历揭秘 父亲:常骂得她痛哭流涕</a></li>
<li><a href="http://ent.163.com/09/0901/04/5I3NPGGT00031H2L.html">李英爱结婚后继续完成博士学业 9月初回韩国</a></li>
<li><a href="http://ent.163.com/09/0901/04/5I3NGA2F00031H2L.html">导演张元直面吸毒事件:感谢全社会的关注</a></li>
</ul>
</div>
<    script type="text/javascript"       >
<div class="more">
<span><a href="http://ent.163.com/">更多娱乐新闻</a></span>
</script>
<span style="background: transparent none repeat scroll 0% 0%; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial; color: rgb(31, 58, 135); float: left;"><a href="http://popme.163.com/link/005975_0804_8307.html">[热点:痘印难消为痘抓狂]</a></span>
</div>
</div>
"""

    def test_is_closed(self):
        p = HtmlParser(HtmlHandler())
        self.assertFalse(p.is_self_closed("<sdgsdg>"))
        self.assertTrue(p.is_self_closed("<sdgsdg/>"))
        self.assertTrue(p.is_self_closed("<sdgsdg/ >"))
        self.assertTrue(p.is_self_closed("<sdgsdg  /   >"))
    
    def test_html(self):
        handler = TestHandler(handle_comment=True, handle_text=True)
        parser = HtmlParser(handler)
        parser.parse(self.html)
        self.assertEquals(13, handler.anum)
        
    def test_remove_script(self):
        handler = HtmlHandler(handle_comment=True, handle_text=True)
        parser = HtmlParser(handler)
        parser.parse(self.html)
        connect_mark = ''
        html_removed = handler.get_html_exclude_script(connect_mark)
        self.assertEquals(html_removed, connect_mark.join([
            "开始的文本内容<!--这是一个注释-->金越任虎年春晚总导演",
            "曾轶可《狮子座》涉嫌抄袭纯音乐《天际》",
            "金马奖报名截止 郭富城刘德华黎明争夺影帝",
            "赵雅芝准备接演古董收藏剧 支持阿娇演白娘子",
            "李玟:与男友前妻成了姐妹 暂时没时间结婚",
            "潘粤明:已经在蜜罐里 有信心与董洁白头偕老",
            "中间的文本内容",
            "《气喘吁吁》被批“难看” 葛优票房神话难续",
            "关锦鹏：梁朝伟斗心强  张曼玉曾苦练走路",
            "郁可唯成长经历揭秘 父亲:常骂得她痛哭流涕",
            "李英爱结婚后继续完成博士学业 9月初回韩国",
            "导演张元直面吸毒事件:感谢全社会的关注",
            "[热点:痘印难消为痘抓狂]"
        ]))
        
def test_main():
    import urllib2
    from time import time
    urls = [
        'http://wap.sohu.com/'
#        'http://bj.3g.cn/index.aspx?cin=-67&gaid=Tm9raWE2MjMw&rd=02&sid=0',
#        'http://blog.3g.cn/',
#        'http://blog.3g.cn/commspec/0754/6years.aspx?cin=362312&gaid=Tm9raWE2MjMw&sid=0',
#        'http://bula.cn/HelpDetail.aspx?ID=7&helperID=8&sid=0',
#        'http://caipiao.3g.cn/index.aspx?cin=-80&gaid=Tm9raWE2MjMw&rd=20&sid=0',
#        'http://digi.3g.cn/index.aspx?cin=121&gaid=Tm9raWE2MjMw&rd=02&sid=0',
#        'http://down2.uc.cn/?f=chenf@moabccom&title=moabc.com&url=http%3A%2F%2Fmoabc.com',
#        'http://edu.3g.cn/index.aspx?ftp=0&k=2009%e9%ab%98%e8%80%83&nid=21336&sid=0',
#        'http://news.3g.cn/shehui.aspx?cin=366164&gaid=Tm9raWE2MjMw&sid=0',
#        'http://now.3g.cn/foryou/index.aspx?cin=-33&gaid=Tm9raWE2MjMw&rd=02&sid=0',
#        'http://qinggan.loveshafa.com/index.aspx?cin=70&sid=0',
#        'http://rdt.yicha.cn/1360',
#        'http://sj.lexun.com/man/manlist.aspx?cd=39903&cr=cb04baa21198295&forumId=8982&lxt=0&topic_page=1',
#        'http://u.yicha.cn/union/search.jsp?pageBegin=1&site=2145944277&version=1',
#        'http://wap.3g.net.cn/index.aspx',
#        'http://wapblog.people.com.cn/?chid=&fromid=201&iv=sz&sid=0&v=l&wv=1.2',
#        'http://wfne.3g.qq.com/g/s?&aid=tmark&sid=0&tips=1',
#        'http://y.easou.com/thread/barViewThread.e?barId=10007&esid=0&fr=52.1.8'
    ]
    htmls = []
    for url in urls:
        try:
            html = urllib2.urlopen(url, None, 3).read()
            html = html.strip()
            if html:
                htmls.append(html)
            else:
                print url
        except:
            print url
    print 'begin'
    handler = HtmlHandler(handle_comment=False, handle_text=True)
    parser = HtmlParser(handler)
    btime = time()
    for i in range(1):
        for html in htmls:
            parser.parse(html)
            text = handler.get_html_exclude_script()
            handler.html_list = []
            print text
    print time() - btime
    
def test_main_2():
    from time import time
    html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>三亚酒店预订列表 三亚宾馆查询订房</title>
<meta name="Description" content="三亚酒店列表宾馆查询订房" />
<meta name="Keywords" content="三亚酒店预订宾馆查询订房" />
<link href="/hotel/css/hotellist.css" rel="stylesheet" type="text/css" />
<script src="http://pic.yoyv.com/scripts/gwindow.js"></script>
<script src="http://pic.yoyv.com/scripts/stuHover.js"></script>
<script src="http://pic.yoyv.com/top/scripts/newtop.js"></script>
<script src="http://pic.yoyv.com/scripts/ajax.js"></script>
<link href="http://pic.yoyv.com/css/gwindow.css" type=text/css rel=stylesheet></link>
<link href="http://pic.yoyv.com/css/newtop.css" rel="stylesheet" type="text/css" />
<script language="javascript" src="/hotel/scripts/search.js"></script>
<script language="javascript" src="/hotel/scripts/mycal.js"></script>
</head>

<body style="margin-top:0px;" onload="init('2201',0,0,0,0)">
<div style="position:absolute; width:980px!important;width:983px; border:0px; top:0px; z-index:1000;">
    <div id="loginBox" name="loginBox" class="signin" style="position: absolute; display:none; float:right; right:0px; width:10px; height:10px; overflow: hidden;">
        <div style="margin-top:10px;">
        <div class="signintop">
        <div style="text-align:right; margin-top:-10px; margin-right:-10px; z-index:500; position:relative;"><img src="/images/close_LoginBox.gif" alt="关闭" style="cursor:pointer;" onclick="closeloginBox()"></div>
        <div class="loginword"><img src="/images/usericon.gif" align="absmiddle">游鱼会员登陆</div>
        <table width="260" border="0" cellspacing="0" cellpadding="0" style="margin-top:0px; margin-left:20px;">
            <tr>
                <td width="62" height="18"></td>
                <td width="198" id="errorLog" align="left" valign="bottom" class="errorInfo"></td>
            </tr>
            <tr>
                <td width="62" height="34" align="right" class="loginword2">用户名：</td>
                <td width="198"><input type="text" id="username_login" style="width:180px; height:17px; background-color:#FFFFFF;" /></td>
            </tr>
            <tr class="loginword2">
                <td height="39" align="right">登录密码：</td>
                <td><input type="password" id="password_login" style="width:100px; height:17px; background-color:#FFFFFF;" onkeyup="Javascript:if (event.which==13||event.keyCode==13){logOn();}"/>&nbsp;<a href="/land/getpwd.htm" rel="nofollow">忘记了密码?</a></td>
            </tr>
            <tr class="loginword3">
                <td height="30" colspan="2">还不是会员？<a href="/tour/guideintr.html" rel="nofollow">了解一下游鱼</a>或者<a href="/reg/reg.asp" rel="nofollow">立即注册</a></td>
                </tr>
            <tr class="loginword3">
                <td height="12" colspan="2"><div class="loginline1"></div><div class="loginline2"></div></td>
                </tr>
            <tr class="loginword3">
                <td height="34" colspan="2"><input name="remember" type="checkbox" hidefocus="true" value="" checked="checked"/>在这台电脑上记住我的密码。&nbsp;<img src="/images/sign_in_form_hover.gif" align="absmiddle" onclick="logOn()" alt="登录" style="cursor:pointer;"/></td>
                </tr>
        </table>
        </div>
        <div class="signinbottom"></div>
        </div>
    </div>
    <div id="progressBar" name="progressBar" class="signin" style="position: absolute; display:none; float:right; right:0px; width:310px; height:280px; overflow: hidden;">
        <div style="margin-top:10px;">
        <div class="signin">
        <div class="signintop">
        <div style="text-align:right; margin-top:-10px; margin-right:-10px; z-index:500; position:relative;"><img src="/images/close_LoginBox.gif"></div>
        <div class="loginword"><img src="/images/usericon.gif" align="absmiddle">游鱼会员登陆</div>
        <table width="260" border="0" cellspacing="0" cellpadding="0" style="margin-top:10px; margin-left:20px;">
            <tr>
                <td width="198" height="22">&nbsp;</td>
            </tr>
            <tr class="loginword2">
                <td height="40" align="center"><img src="/images/progressBar_Log.gif" width="40" /></td>
            </tr>
            
            <tr class="loginword3">
                <td height="38" align="center" valign="bottom" id="progressInfo">正在登录……</td>
                </tr>
        </table>
        </div>
        <div class="signinbottom"></div>
        </div>
        </div>
    </div>
</div>
<div class="navarea" style="background-color:#FFFFFF">
    <div class="loginarea">
        <div class="logoarea"><a href="/" title="游鱼——发现旅游！分享旅游！"><img src="/images/logo4.gif" border="0" alt="游鱼——发现旅游！分享旅游！" /></a></div>
        <div class="pagetopright">
            <div style="display:none; color:#999999;" id="loginsuc"></div>
            <div id="login" style="color:#999999;">第一次来游鱼？<img src="/images/toprightarrow.gif" align="absmiddle" /><a href="/tour/guideintr.html" rel="nofollow">了解游鱼</a>&nbsp;|&nbsp;<a href="/reg/reg.asp" rel="nofollow">注册</a>&nbsp;|&nbsp;<a href="javascript:showLoginBox1()" rel="nofollow">登陆</a></div>
            <div class="topsearch">
                <!-- Google CSE Search Box Begins  -->
                <form id="searchbox_017628897638471485970:hceobi7ukkq" action="http://www.yoyv.com/search/result.html" target="_blank" style="margin:0px">
                    <input type="hidden" value="017628897638471485970:hceobi7ukkq" name="cx" />
                    <input type="hidden" value="FORID:9" name="cof" />
                    <input size="25" name="q" align="absmiddle" class="inputarea" />
                    <input name="Input" type="image" src="/images/yoyvsearch.gif" align="absmiddle"/>
                </form>
            </div>
        </div>
    </div>
    <div style="width:928px; text-align:left; clear:both;background-color:#FFFFFF"> <span class="preload1"></span> <span class="preload2"></span>
            <ul id="nav">
                <li class="top"><a href="/" class="top_link"><span>首页</span></a></li>
                <li class="top"><a href="/guide/" rel="nofollow" class="top_link"><span class="down">旅游指南</span></a></li>
                        <ul class="sub">
                            <li><b>目的地旅游指南</b></li>
                            <li><a href="/guide/">国内旅游指南</a></li>
                            <li><a href="/continent/asia.html">亚洲旅游指南</a></li>
                            <li><a href="/continent/europe.html">欧洲旅游指南</a></li>
                            <li><a href="/continent/africa.html">非洲旅游指南</a></li>
                            <li><a href="/continent/namerica.html">北美洲旅游指南</a></li>
                            <li><a href="/continent/samerica.html">南美洲旅游指南</a></li>
                            <li><a href="/continent/oceania.html">大洋洲旅游指南</a></li>
                        </ul>
                <li class="top"><a href="/top/traveltool.html" class="top_link"><span class="down">预订查询</span></a></li>
                        <ul class="sub">
                            <li><b>旅游查询预订</b></li>
                            <li><a href="/traveltool/dflight.asp">国内航班查询</a></li>
                            <li><a href="/traveltool/iflight.asp">国际航班查询</a></li>
                            <li><a href="/traveltool/hotel.asp">国内酒店查询</a></li>
                            <li><a href="/overseas/hotelsearch.asp">海外酒店查询</a></li>
                            <li><b>分类查询工具</b></li>
                            <li><a href="/map/satellite.asp">地图搜索</a></li>
                            <li><a href="/traveltool/sightseeing.asp" class="fly">景点搜索</a>
                                    <ul>
                                        <li><a href="/traveltool/sightseeing.asp">国内景点搜索</a></li>
                                        <li><a href="/overseas/sightsearch.asp">世界景点搜索</a></li>
                                    </ul>
                            </li>
                            <li><a href="/easytour/index.asp" class="fly">旅行交通查询</a>
                                    <ul>
                                        <li><a href="/easytour/index.asp">行易通&nbsp;<img src="/guide/myview/images/good.gif" align="absmiddle" border="0" /></a></a></li>
                                        <li><a href="/traveltool/bus.asp">国内260城市公交</a></li>
                                        <li><a href="/overseas/metromap.asp">地铁路线图(全球)</a></li>
                                        <li><a href="/traveltool/train.asp">国内火车查询</a></li>
                                    </ul>
                            </li>
                            <li><a href="/traveltool/hostel.asp">旅馆招待所查询</a>
                            </li>
                            <li><a href="/traveltool/restaurant.asp" class="fly">餐饮娱乐购物</a>
                                    <ul>
                                        <li><a href="/traveltool/restaurant.asp">餐馆搜索(国内)</a></li>
                                        <li><a href="/overseas/restaurantsearch.asp">餐馆搜索(海外)</a></li>
                                        <li><a href="/traveltool/Entertainment.asp">娱乐搜索(国内)</a></li>
                                        <li><a href="/overseas/entertainmentsearch.asp">娱乐搜索(海外)</a></li>
                                        <li><a href="/traveltool/shopping.asp">购物搜索(国内)</a></li>
                                        <li><a href="/overseas/shoppingsearch.asp">购物搜索(海外)</a></li>
                                    </ul>
                            </li>
                            <li><a href="/traveltool/weather.asp">各城市天气预报</a></li>
                        </ul>
                <li class="top"><a href="/tripplanner/" class="top_link"><span>旅行计划</span></a></li>
        <li class="top" style="margin-top:8px;"><font color="#999999">|</font></li>
                <li class="top"><a href="/space/blogindex.asp" rel="nofollow" class="top_link"><span class="down">博客</span></a></li>
                        <ul class="sub">
                            <li><b>博客游记分享</b></li>
                            <li><a href="/space/blogindex.asp">博客首页</a></li>
                            <li><a href="/platter/b-list/1">博客拼盘</a></li>
                            <li><a href="/moving/blogmoving.asp">博客搬家</a></li>
                            <li><a href="/moving/synservice.asp">博客同步</a></li>
                        </ul>
                <li class="top"><a href="/Album/Index.asp" rel="nofollow" class="top_link"><span class="down">图片相册</span></a></li>
                        <ul class="sub">
                            <li><b>相册与图片分享</b></li>
                            <li><a href="/Album/Index.asp">图片相册首页</a></li>
                            <li><a href="/platter/p-list/1">图片拼盘</a></li>
                            <li><a href="/album/more_1/">最新相册列表</a></li>
                            <li><a href="/photos/calendar.asp">图片日历</a></li>
                            <li><a href="/phototype9/1.html">旅游图片分类</a></li>
                            <li><a href="/space/pkzone.asp">靓照对决</a></li>
                        </ul>
                <li class="top"><a href="/Map/" class="top_link"><span>主题地图</span></a></li>
                <li class="top"><a href="/group/" class="top_link"><span>群组</span></a></li>
        <li class="top" style="margin-top:8px;"><font color="#bbbbbb">|</font></li>
                
        <li class="top"><a href="/space/trailmap.asp" class="top_link"><span>足迹</span></a></li>
        <li class="top"><a href="/platter/" class="top_link"><span>拼盘</span></a></li>
        <li class="top"><a href="/quiz/travelquiz.asp" class="top_link"><span>竞猜</span></a></li>
        <li class="top"><a href="/vote/voteindex.asp" class="top_link"><span>投票</span></a></li>
        <li class="top"><a href="/ask/index.asp" class="top_link"><span>问答</span></a></li>
        <li class="top"><a href="/Deal/Index.asp" class="top_link"><span>交易</span></a></li>
            </ul>
    </div>
</div><script language="javascript">login();</script>

<div class="main">
  <div class="nowposition"><a href="/traveltool/hotel.asp">酒店预订</a>&nbsp;&gt;&gt;&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_1/">三亚酒店</a></div>
  <div class="leftbody">
    <div class="hotelcount">
      <div class="hotelsno">134</div>
      <div class="hotelsnointro">间三亚的酒店宾馆<br />
        符合您的搜索要求</div>
      <div class="hotelsnointro" style="margin-top:30px; font-weight:bold;">对搜索结果排序</div>
    </div>
    <div class="hotelsfliterarrow"></div>
    <div class="fliterarea">
      <div class="flitername1">酒店价格排序</div>
      <div class="flitervolum">
        <select name="orderByPrice2" class="selectmenu1" onchange="orderType('price')">
          <option value="请选择排序方式">请选择排序方式</option>
          <option value="asc">从低到高</option>
        </select>
      </div>
      <div class="flitername1">酒店星级排序</div>
      <div class="flitervolum">
        <select name="orderByStar2" class="selectmenu1" onchange="orderType('star')">
          <option value="请选择排序方式">请选择排序方式</option>
          <option value="asc">从低到高</option>
        </select>
      </div>
    </div>
    <div class="leftothersearch">
      <div class="searchvolum" onclick="show2(this)">
        <table width="168" border="0" cellspacing="0" cellpadding="0" align="center" style="margin-top:12px;">
          <tr>
            <td width="153">按商业区查看酒店</td>
            <td width="15" align="right"><img src="/hotel/images/displayarrow.gif" border="0" /></td>
          </tr>
        </table>
      </div>
            <div class="rightlist">
                <ul>
                    <li><a href="/hotel/sowntown/%C8%FD%D1%C7_%B4%F3%B6%AB%BA%A3_1/">大东海</a>(50        )</li>
                    <li><a href="/hotel/sowntown/%C8%FD%D1%C7_%C4%CF%C9%BD_1/">南山</a>(3         )</li>
                    <li><a href="/hotel/sowntown/%C8%FD%D1%C7_%C4%CF%CC%EF_1/">南田</a>(3         )</li>
                    <li><a href="/hotel/sowntown/%C8%FD%D1%C7_%C8%FD%D1%C7%CD%E5_1/">三亚湾</a>(65        )</li>
                    <li><a href="/hotel/sowntown/%C8%FD%D1%C7_%CA%D0%C4%DA_1/">市内</a>(27        )</li>
                    <li><a href="/hotel/sowntown/%C8%FD%D1%C7_%F2%DA%D6%A7%D6%DE_1/">蜈支洲</a>(1         )</li>
                    <li><a href="/hotel/sowntown/%C8%FD%D1%C7_%CE%F7%B5%BA_1/">西岛</a>(1         )</li>
                    <li><a href="/hotel/sowntown/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/">亚龙湾</a>(20        )</li>
                </ul>
            </div>
            <div class="searchvolum" onclick="show2(this)">
                <table width="168" border="0" cellspacing="0" cellpadding="0" align="center" style="margin-top:12px;">
                    <tr>
                        <td width="153">按行政区查看酒店</td>
                        <td width="15" align="right"><img src="/hotel/images/hidearrow.gif" border="0" /></td>
                    </tr>
                </table>
            </div>
            <div class="rightlist" style="display:none">
                <ul>
                    <li><a href="/hotel/district/%C8%FD%D1%C7_%B4%F3%B6%AB%BA%A3_1/">大东海</a>(14)</li>
                    <li><a href="/hotel/district/%C8%FD%D1%C7_%BA%D3%B6%AB%C7%F8_1/">河东区</a>(4)</li>
                    <li><a href="/hotel/district/%C8%FD%D1%C7_%C8%FD%D1%C7%CD%E5_1/">三亚湾</a>(25)</li>
                    <li><a href="/hotel/district/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/">亚龙湾</a>(17)</li>
                </ul>
            </div>
            <div class="searchvolum" onclick="show2(this)">
                <table width="168" border="0" cellspacing="0" cellpadding="0" align="center" style="margin-top:12px;">
                    <tr>
                        <td width="153">按星级查看酒店</td>
                        <td width="15" align="right"><img src="/hotel/images/hidearrow.gif" border="0" /></td>
                    </tr>
                </table>
            </div>
            <div class="rightlist" style="display:none">
                <ul>
                    <li><a href="/hotel/star/%C8%FD%D1%C7_5_1/">三亚五星级酒店</a></li>
                    <li><a href="/hotel/star/%C8%FD%D1%C7_4_1/">三亚四星级酒店</a></li>
                    <li><a href="/hotel/star/%C8%FD%D1%C7_3_1/">三亚三星级酒店</a></li>
                    <li><a href="/hotel/star/%C8%FD%D1%C7_2_1/">三亚二星级酒店</a></li>
                </ul>
            </div>
            <div class="searchvolum" onclick="show2(this)">
                <table width="168" border="0" cellspacing="0" cellpadding="0" align="center" style="margin-top:12px;">
                    <tr>
                        <td width="153">热门城市酒店索引</td>
                        <td width="15" align="right"><img src="/hotel/images/hidearrow.gif" border="0" /></td>
                    </tr>
                </table>
            </div>
            <div class="rightlist" style="display:none">
                <ul>
          <li><a href="/hotel/city/%B1%B1%BE%A9_1/">北京酒店</a></li>
          <li><a href="/hotel/city/%C9%CF%BA%A3_1/">上海酒店</a></li>
          <li><a href="/hotel/city/%B9%E3%D6%DD_1/">广州酒店</a></li>
          <li><a href="/hotel/city/%C9%EE%DB%DA_1/">深圳酒店</a></li>
          <li><a href="/hotel/city/%BA%BC%D6%DD_1/">杭州酒店</a></li>
          <li><a href="/hotel/city/%CE%F7%B0%B2_1/">西安酒店</a></li>
          <li><a href="/hotel/city/%CE%E4%BA%BA_1/">武汉酒店</a></li>
          <li><a href="/hotel/city/%B3%C9%B6%BC_1/">成都酒店</a></li>
          <li><a href="/hotel/city/%C4%CF%BE%A9_1/">南京酒店</a></li>
          <li><a href="/hotel/city/%C8%FD%D1%C7_1/">三亚酒店</a></li>
          <li><a href="/hotel/city/%C9%F2%D1%F4_1/">沈阳酒店</a></li>
          <li><a href="/hotel/city/%CB%D5%D6%DD_1/">苏州酒店</a></li>
          <li><a href="/hotel/city/%C7%E0%B5%BA_1/">青岛酒店</a></li>
          <li><a href="/hotel/city/%CC%EC%BD%F2_1/">天津酒店</a></li>
          <li><a href="/hotel/city/%CF%C3%C3%C5_1/">厦门酒店</a></li>
                </ul>
            </div>
            <div class="searchvolum">
                <table width="168" border="0" cellspacing="0" cellpadding="0" align="center" style="margin-top:12px;">
                    <tr>
                        <td width="153">酒店订单查询</td>
                        <td width="15" align="right"></td>
                    </tr>
                </table>
            </div>
      <div class="rightlist"><form action="/hotel/browseorder.asp" method="post" style="margin:0px;">
        <ul>
          <li style="margin-left:0px; list-style:none;"><font color="#666666">联系人姓名：</font>
              <input name="CName" type="text" />
          </li>
          <li style="margin-left:0px; list-style:none;"><font color="#666666">手机号码：</font>
              <input name="Mobile" type="text" />
          </li>
          <li style="margin-top:10px; margin-bottom:10px;margin-left:0px; list-style:none;"><input name="" type="image" src="/hotel/images/checkorder.gif" /></li>
        </ul></form>
      </div>
    </div>
  </div>
  <div class="rightbody">
    <h1>三亚酒店预订列表 三亚宾馆查询结果</h1>
    <div class="hotellistintro">您搜索的是<font color="#FF6600"><strong>2010-07-14</strong></font>至<font color="#FF6600"><strong>2010-07-16</strong></font>三亚酒店价格。这些价格是每个酒店宾馆的最低房型价格，您可以点击每个酒店右侧的“房型价格”链接来浏览该酒店的所有房型。同时您也可以选择左侧的行政区或商业区来缩小您的搜索范围。</div>
    <div class="hotellistintro" style="margin-top:20px;"><font class="changdate">变更日期重新查询：</font>&nbsp;入住日期&nbsp;<input id="InDate2" type="text" class="datefill" value="2010-07-14" onClick="event.cancelBubble=true;showCalendar('InDate2',false,'InDate2')"/>&nbsp;&nbsp;离店日期&nbsp;<input id="OutDate2" type="text" class="datefill" value="2010-07-16" onClick="event.cancelBubble=true;showCalendar('OutDate2',false,'OutDate2')"/>&nbsp;&nbsp;<a href="javascript:changeDate()"><img src="/hotel/images/searchbutton.gif" align="absmiddle" border="0" /></a>&nbsp;&nbsp;<a href="#moresearch">更多查询选项</a>&nbsp;&nbsp;<a href="/hotel/searchmap/%C8%FD%D1%C7.html" title="在三亚地图上查询酒店">使用地图查询</a></div>
    <div class="restpage">&nbsp;<font class="curpage">1</font>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_2/">2</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_3/">3</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_4/">4</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_5/">5</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_6/">6</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_7/">7</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_8/">8</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_9/">9</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_10/">10</a>&nbsp;<font color="#666666" style=" font-weight:normal;">共14页</font>&nbsp;</div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="http://static.elong.com/images/hotels/hotelimages/30/42201201_0_5_0_6.jpg" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">1.<a href="/hotel/details/8330.htm">三亚国光豪生度假酒店</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/sowntown/%C8%FD%D1%C7_%C8%FD%D1%C7%CD%E5_1/"title="位于三亚湾的酒店列表">三亚湾</a><br />
                  酒店地址：海南省三亚市三亚湾路188号<br />
                  <font style="font-weight:bold">2010/3/16-2010/5/3，酒店试行24小时入住制。</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥780</font>起<br />
                    <a href="/hotel/room/8330.htm" title="浏览三亚三亚国光豪生度假酒店的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/8330.htm" title="浏览三亚三亚国光豪生度假酒店的详细介绍及酒店设施">酒店设施</a><br />
              <a href="/hotel/traffic/8330.htm" title="三亚三亚国光豪生度假酒店的交通、位置以及电子地图">交通地图</a><br /><a href="/hotel/pic/8330.htm" title="浏览三亚三亚国光豪生度假酒店的所有图片">酒店图片</a></div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="http://static.elong.com/images/hotels/hotelimages/7/52201012_0_5_0_4.jpg" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">2.<a href="/hotel/details/173.htm">三亚天福源度假酒店</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/sowntown/%C8%FD%D1%C7_%C8%FD%D1%C7%CD%E5_1/"title="位于三亚湾的酒店列表">三亚湾</a><br />
                  酒店地址：海南省三亚市三亚湾旅游度假区<br />
                  <font style="font-weight:bold">酒店位于三亚湾海坡开发区，拥有目前三亚最大的温泉泳池，可近览海天一线的美景。</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥348</font>起<br />
                    <a href="/hotel/room/173.htm" title="浏览三亚三亚天福源度假酒店的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/173.htm" title="浏览三亚三亚天福源度假酒店的详细介绍及酒店设施">酒店设施</a><br />
              <a href="/hotel/traffic/173.htm" title="三亚三亚天福源度假酒店的交通、位置以及电子地图">交通地图</a><br /><a href="/hotel/pic/173.htm" title="浏览三亚三亚天福源度假酒店的所有图片">酒店图片</a></div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="http://static.elong.com/images/hotels/hotelimages/1/42201002_0_5_0_6.jpg" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">3.<a href="/hotel/details/4583.htm">三亚南中国大酒店</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate2.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/sowntown/%C8%FD%D1%C7_%B4%F3%B6%AB%BA%A3_1/"title="位于大东海的酒店列表">大东海</a><br />
                  酒店地址：海南省三亚市大东海旅游度假区<br />
                  <font style="font-weight:bold">从酒店步行两分钟可达大东海嬉水乐园，曾多次接待国家领导及外国元首的豪华花园酒店。</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥444</font>起<br />
                    <a href="/hotel/room/4583.htm" title="浏览三亚三亚南中国大酒店的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/4583.htm" title="浏览三亚三亚南中国大酒店的详细介绍及酒店设施">酒店设施</a><br />
              <a href="/hotel/traffic/4583.htm" title="三亚三亚南中国大酒店的交通、位置以及电子地图">交通地图</a><br /><a href="/hotel/pic/4583.htm" title="浏览三亚三亚南中国大酒店的所有图片">酒店图片</a></div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="http://static.elong.com/images/hotels/hotelimages/2/52201004_0_5_0_3.jpg" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">4.<a href="/hotel/details/184.htm">三亚亚龙湾天鸿度假村</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/district/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/" title="亚龙湾酒店列表">亚龙湾</a>，<a href="/hotel/sowntown/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/"title="位于亚龙湾的酒店列表">亚龙湾</a><br />
                  酒店地址：海南省三亚市亚龙湾国家旅游度假区<br />
                  <font style="font-weight:bold">具有热带休闲风格的别墅精品度假酒店，前瞰白沙碧海，背依湖泊青山，房间全部面海。</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥738</font>起<br />
                    <a href="/hotel/room/184.htm" title="浏览三亚三亚亚龙湾天鸿度假村的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/184.htm" title="浏览三亚三亚亚龙湾天鸿度假村的详细介绍及酒店设施">酒店设施</a><br />
              <a href="/hotel/traffic/184.htm" title="三亚三亚亚龙湾天鸿度假村的交通、位置以及电子地图">交通地图</a><br /><a href="/hotel/pic/184.htm" title="浏览三亚三亚亚龙湾天鸿度假村的所有图片">酒店图片</a></div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="http://static.elong.com/images/hotels/hotelimages/11/52201018_0_2_0_6.jpg" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">5.<a href="/hotel/details/176.htm">三亚亚龙湾红树林度假酒店</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/district/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/" title="亚龙湾酒店列表">亚龙湾</a>，<a href="/hotel/sowntown/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/"title="位于亚龙湾的酒店列表">亚龙湾</a><br />
                  酒店地址：海南省三亚市亚龙湾国家旅游度假区<br />
                  <font style="font-weight:bold">酒店位于亚龙湾国家旅游度假区，是中国唯一具有巴厘岛热带风情的纯度假酒店。</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥1240</font>起<br />
                    <a href="/hotel/room/176.htm" title="浏览三亚三亚亚龙湾红树林度假酒店的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/176.htm" title="浏览三亚三亚亚龙湾红树林度假酒店的详细介绍及酒店设施">酒店设施</a><br />
              <a href="/hotel/traffic/176.htm" title="三亚三亚亚龙湾红树林度假酒店的交通、位置以及电子地图">交通地图</a><br /><a href="/hotel/pic/176.htm" title="浏览三亚三亚亚龙湾红树林度假酒店的所有图片">酒店图片</a></div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="http://static.elong.com/images/hotels/hotelimages/11/52201017_0_5_0_4.jpg" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">6.<a href="/hotel/details/175.htm">三亚湾假日酒店</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/sowntown/%C8%FD%D1%C7_%C8%FD%D1%C7%CD%E5_1/"title="位于三亚湾的酒店列表">三亚湾</a><br />
                  酒店地址：海南省三亚市三亚湾旅游度假区<br />
                  <font style="font-weight:bold">位于海南岛海岸线最长的三亚湾海坡度假区的国际品牌酒店，与美丽的椰梦长廊相依偎。</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥700</font>起<br />
                    <a href="/hotel/room/175.htm" title="浏览三亚三亚湾假日酒店的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/175.htm" title="浏览三亚三亚湾假日酒店的详细介绍及酒店设施">酒店设施</a><br />
              <a href="/hotel/traffic/175.htm" title="三亚三亚湾假日酒店的交通、位置以及电子地图">交通地图</a><br /><a href="/hotel/pic/175.htm" title="浏览三亚三亚湾假日酒店的所有图片">酒店图片</a></div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="/hotel/ImgList/nopic.gif" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">7.<a href="/hotel/details/11835.htm">三亚大小洞天小月湾度假酒店</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/sowntown/%C8%FD%D1%C7_%C4%CF%C9%BD_1/"title="位于南山的酒店列表">南山</a><br />
                  酒店地址：三亚市崖城大小洞天旅游区<br />
                  <font style="font-weight:bold">酒店位于国家5A级景区大小洞天内，面朝南海背靠南山，滨海原生态木屋别墅，一千多米原生态的海滩。</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥598</font>起<br />
                    <a href="/hotel/room/11835.htm" title="浏览三亚三亚大小洞天小月湾度假酒店的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/11835.htm" title="浏览三亚三亚大小洞天小月湾度假酒店的详细介绍及酒店设施">酒店设施</a><br />
              <a href="/hotel/traffic/11835.htm" title="三亚三亚大小洞天小月湾度假酒店的交通、位置以及电子地图">交通地图</a><br /><a href="/hotel/pic/11835.htm" title="浏览三亚三亚大小洞天小月湾度假酒店的所有图片">酒店图片</a></div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="/hotel/images/nolistpic.gif" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">8.<a href="/hotel/details/13929.htm">三亚半山半岛洲际度假酒店</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/sowntown/%C8%FD%D1%C7_%B4%F3%B6%AB%BA%A3_1/"title="位于大东海的酒店列表">大东海</a><br />
                  酒店地址：中国海南省三亚市洲际路1号<br />
                  <font style="font-weight:bold">半山半岛间悦享洲际天</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥1690</font>起<br />
                    <a href="/hotel/room/13929.htm" title="浏览三亚三亚半山半岛洲际度假酒店的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/13929.htm" title="浏览三亚三亚半山半岛洲际度假酒店的详细介绍及酒店设施">酒店设施</a><br />
              </div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="http://static.elong.com/images/hotels/hotelimages/4/52201006_0_5_0_3.jpg" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">9.<a href="/hotel/details/186.htm">三亚亚龙湾环球城大酒店</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/district/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/" title="亚龙湾酒店列表">亚龙湾</a>，<a href="/hotel/sowntown/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/"title="位于亚龙湾的酒店列表">亚龙湾</a><br />
                  酒店地址：海南省三亚市亚龙湾国家度假区<br />
                  <font style="font-weight:bold">酒店背靠青山、西枕绿湖、面朝大海，是一家拥有山、湖、海“三合一”客房风景的酒店。</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥608</font>起<br />
                    <a href="/hotel/room/186.htm" title="浏览三亚三亚亚龙湾环球城大酒店的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/186.htm" title="浏览三亚三亚亚龙湾环球城大酒店的详细介绍及酒店设施">酒店设施</a><br />
              <a href="/hotel/traffic/186.htm" title="三亚三亚亚龙湾环球城大酒店的交通、位置以及电子地图">交通地图</a><br /><a href="/hotel/pic/186.htm" title="浏览三亚三亚亚龙湾环球城大酒店的所有图片">酒店图片</a></div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>
        <div class="hotellist">
      <div class="detailtop"></div>
      <div class="detailmid">
        <table width="727" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td width="145" valign="top"><img src="http://static.elong.com/images/hotels/hotelimages/1/32201001_0_5_0_1.jpg" width="130" border="0" onError=javascript:{this.src='http://www.yoyv.com/hotel/ImgList/nopic.gif'}></td>
            <td width="350" valign="top"><div class="hotelname">10.<a href="/hotel/details/3337.htm">三亚凯莱仙人掌度假酒店（原三亚仙人掌度假酒店）</a></div>
                <div class="hotelcontent">酒店星级：<img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' /><img src='/hotel/images/rate.gif' align='absmiddle' />&nbsp;&nbsp;所在区域：<a href="/hotel/district/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/" title="亚龙湾酒店列表">亚龙湾</a>，<a href="/hotel/sowntown/%C8%FD%D1%C7_%D1%C7%C1%FA%CD%E5_1/"title="位于亚龙湾的酒店列表">亚龙湾</a><br />
                  酒店地址：三亚市亚龙湾国家旅游度假区<br />
                  <font style="font-weight:bold">位于亚龙湾的以印地安人和海南黎、苗族等土著文化为主题具有浓郁玛雅文化的度假酒店。</font></div></td>
            <td width="232" valign="top"><div class="hotelprice"><font class="hotelprice2">￥518</font>起<br />
                    <a href="/hotel/room/3337.htm" title="浏览三亚三亚凯莱仙人掌度假酒店（原三亚仙人掌度假酒店）的所有房型及价格">房型价格</a><br />
              <a href="/hotel/details/3337.htm" title="浏览三亚三亚凯莱仙人掌度假酒店（原三亚仙人掌度假酒店）的详细介绍及酒店设施">酒店设施</a><br />
              <a href="/hotel/traffic/3337.htm" title="三亚三亚凯莱仙人掌度假酒店（原三亚仙人掌度假酒店）的交通、位置以及电子地图">交通地图</a><br /><a href="/hotel/pic/3337.htm" title="浏览三亚三亚凯莱仙人掌度假酒店（原三亚仙人掌度假酒店）的所有图片">酒店图片</a></div></td>
          </tr>
        </table>
      </div>
      <div class="detailbtm"></div>
    </div>        
    <div class="restpage" style="margin-top:15px;">&nbsp;<font class="curpage">1</font>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_2/">2</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_3/">3</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_4/">4</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_5/">5</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_6/">6</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_7/">7</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_8/">8</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_9/">9</a>&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_10/">10</a>&nbsp;<font color="#666666" style=" font-weight:normal;">共14页</font>&nbsp;</div>
    </div>
  <div class="moreinfo">
    <form name="search1" action="/hotel/search.asp" method="post" style="margin:0px 0px 0px 0px;">
    <input name="districtId" type="hidden" value="" />
    <input name="commercialId" type="hidden" value="" />
    <input name="city" type="hidden" value="三亚" />
    <input name="page" type="hidden" value="1" />
    <input name="orderByPrice" type="hidden" value="" />
    <input name="orderByStar" type="hidden" value="" />
    <div class="moresearch"><strong>酒店高级查询：<a name="moresearch" id="moresearch"></a></strong>&nbsp;选择城市&nbsp;<select name="cityId" class="selectmenu2"><script language="JavaScript" src="/hotel/scripts/hotelcityS.js" type="text/javascript"></script></select>&nbsp;&nbsp;入住日期&nbsp;<input name="InDate" type="text" class="datefill" value="2010-07-14" onClick="event.cancelBubble=true;showCalendar('InDate',false,'InDate')"/>&nbsp;&nbsp;离店日期&nbsp;<input name="OutDate" type="text" class="datefill" value="2010-07-16" onClick="event.cancelBubble=true;showCalendar('OutDate',false,'OutDate')"/>
    </div>
    <div class="moresearch" style="padding-top:10px; padding-left:347px;">酒店星级&nbsp;<select name="star" class="selectmenu2"><option value="1" selected>不限星级</option><option value="2">二星级</option><option value="3">三星级</option><option value="4">四星级</option><option value="5">五星级</option></select>&nbsp;&nbsp;酒店价格&nbsp;<select name="price" class="selectmenu2" style="width:104px;"><option value='-1'  selected>不限</option><option value='1201'>1200元以上</option><option value='1200'>801--1200元</option><option value='800'>501--800元</option><option value='500'>401--500元</option><option value='400'>301--400元</option><option value='300'>201--300元</option><option value='200'>200元以下</option></select>&nbsp;&nbsp;酒店名称&nbsp;<input name="hotelName" type="text" class="datefill" style="background-image:none;"/>&nbsp;&nbsp;<a href="javascript:newSearch()"><img src="/hotel/images/searchbtn.gif" border="0" align="absmiddle" /></a></div>
    <div class="moresearch"><strong>本地旅游资讯：</strong>&nbsp;<a href="/totimetable/309_1/">三亚航班查询</a>&nbsp;&nbsp;<a href="/guide/c/%C8%FD%D1%C7/">三亚旅游指南</a>&nbsp;&nbsp;<a href="/guide/OutLook/%C8%FD%D1%C7/">三亚旅游景点</a>&nbsp;&nbsp;<a href="/search/Bus/City/C8FDD1C7.htm">三亚公交</a>&nbsp;&nbsp;<a href="/search/train/station/C8FDD1C7.htm">三亚火车</a>&nbsp;&nbsp;<a href="/guide/Food/%C8%FD%D1%C7/">三亚餐馆</a>&nbsp;&nbsp;<a href="/city/trip/309_1/">三亚旅行计划</a></div>
  </form>
    </div>
</div>
<div class="yoyvbtm">
  <div class="btmbg">
    <div class="btmcontent">
      <div class="btmitem">关于游鱼www.yoyv.com◎</div>
      <div class="youyuintro">游鱼是一个旅游爱好者分享旅途快乐,交流旅行经验的旅游社区。<br />
        游鱼是一部涵盖目的地餐饮、住宿、交通、旅游景点、购物、娱乐等实用信息的旅行指南。</div>
    </div>
    <div class="btmcontent2" >
      <div class="btmitem">热门旅游目的地</div>
      <div class="youyuintro">
        <ul>
            <li><a href="/guide/c/%B1%B1%BE%A9/" target="_blank">北京旅游指南</a></li>
            <li><a href="/guide/c/%C9%CF%BA%A3/" target="_blank">上海旅游指南</a></li>
            <li><a href="/guide/c/%BA%BC%D6%DD/" target="_blank">杭州旅游指南</a></li>
            <li><a href="/guide/c/%C4%CF%BE%A9/" target="_blank">南京旅游指南</a></li>
            <li><a href="/guide/c/%B9%F0%C1%D6/" target="_blank">桂林旅游指南</a></li>
            <li><a href="/guide/c/%CE%F7%B0%B2/" target="_blank">西安旅游指南</a></li>
            <li><a href="/guide/c/%C8%FD%D1%C7/" target="_blank">三亚旅游指南</a></li>
            <li><a href="/guide/c/%C0%F6%BD%AD/" target="_blank">丽江旅游指南</a></li>
        </ul>
      </div>
    </div>
    <div class="btmcontent2" >
            <div class="btmitem">热门地区酒店预订</div>
            <div class="youyuintro">
                <ul>
          <li><a href="/hotel/city/%B1%B1%BE%A9_1/" target="_blank">北京酒店</a>&nbsp;&nbsp;<a href="/hotel/city/%B3%C9%B6%BC_1/" target="_blank">成都酒店</a></li>
          <li><a href="/hotel/city/%C9%CF%BA%A3_1/" target="_blank">上海酒店</a>&nbsp;&nbsp;<a href="/hotel/city/%CE%E4%BA%BA_1/" target="_blank">武汉酒店</a></li>
          <li><a href="/hotel/city/%B9%E3%D6%DD_1/" target="_blank">广州酒店</a>&nbsp;&nbsp;<a href="/hotel/city/%C4%CF%BE%A9_1/" target="_blank">南京酒店</a></li>
          <li><a href="/hotel/city/%C9%EE%DB%DA_1/" target="_blank">深圳酒店</a>&nbsp;&nbsp;<a href="/hotel/city/%C8%FD%D1%C7_1/" target="_blank">三亚酒店</a></li>
          <li><a href="/hotel/city/%BA%BC%D6%DD_1/" target="_blank">杭州酒店</a>&nbsp;&nbsp;<a href="/hotel/city/%CB%D5%D6%DD_1/" target="_blank">苏州酒店</a></li>
          <li><a href="/hotel/city/%CE%F7%B0%B2_1/" target="_blank">西安酒店</a>&nbsp;&nbsp;<a href="/hotel/city/%C0%A5%C3%F7_1/" target="_blank">昆明酒店</a></li>
          <li><a href="/hotel/city/%C7%E0%B5%BA_1/" target="_blank">青岛酒店</a>&nbsp;&nbsp;<a href="/hotel/city/%B4%F3%C1%AC_1/" target="_blank">大连酒店</a></li>
          <li><a href="/hotel/city/%CF%C3%C3%C5_1/" target="_blank">厦门酒店</a>&nbsp;&nbsp;<a href="/hotel/city/%D6%D8%C7%EC_1/" target="_blank">重庆酒店</a></li>
                </ul>
      </div>
    </div>
    <div class="btmcontent2" >
            <div class="btmitem">热门旅游景点</div>
            <div class="youyuintro">
                <ul>
                    <li><a href="/s/11796" target="_blank">故宫</a>&nbsp;&nbsp;<a href="/s/15549" target="_blank">西湖</a></li>
                    <li><a href="/s/16521" target="_blank">黄山</a>&nbsp;&nbsp;<a href="/s/22128" target="_blank">华山</a></li>
                    <li><a href="/s/17772" target="_blank">泰山</a>&nbsp;&nbsp;<a href="/s/15082" target="_blank">周庄</a></li>
                    <li><a href="/s/19604" target="_blank">阳朔</a>&nbsp;&nbsp;<a href="/s/16284" target="_blank">乌镇</a></li>
                    <li><a href="/s/11865" target="_blank">天安门</a>&nbsp;&nbsp;<a href="/s/12465" target="_blank">颐和园</a></li>
                    <li><a href="/s/15572" target="_blank">千岛湖</a>&nbsp;&nbsp;<a href="/s/20162" target="_blank">九寨沟</a></li>
                    <li><a href="/s/17942" target="_blank">少林寺</a>&nbsp;&nbsp;<a href="/s/16900" target="_blank">鼓浪屿</a></li>
                    <li><a href="/s/18950" target="_blank">凤凰古城</a>&nbsp;&nbsp;<a href="/s/21556" target="_blank">布达拉宫</a></li>
                </ul>
      </div>
    </div>
    <div class="btmcontent2" style=" border:0px;">
      <div class="btmitem">关于游鱼</div>
      <div class="youyuintro">
        <ul>
          <li><a href="/Info/help.html#d" target="_blank" rel="nofollow">关于游鱼</a></li>
          <li><a href="/Info/help.html#l" target="_blank" rel="nofollow">联系我们</a></li>
          <li><a href="/ad/index.html" target="_blank">产品服务</a></li>
          <li><a href="/Info/SiteMap.htm" target="_blank">站内导航</a></li>
          <li><a href="/group/yoyv/" target="_blank">游鱼站务论坛</a></li>
          <li><a href="http://yoyvcom.yoyv.com" target="_blank">游鱼Blog</a></li>
          <li><a href="/LeaveWord/index.asp" target="_blank" rel="nofollow">建议留言</a></li>
          <li><a href="/Info/link2.asp" target="_blank">友情链接</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="yoyvcopyright">Copright ◎2006-2010 YOYV.COM All Rights reserved <a href="http://www.miibeian.gov.cn/" rel="nofollow">陕ICP备07000041号</a></div>
    <div style="display:none;"><script language="javascript" src="http://count8.51yes.com/click.aspx?id=84597943&logo=12" charset="gb2312"></script>
</div>
</div>

</body>
</html>    """
    handler = TestHandler(handle_comment=False, handle_text=False)
    parser = HtmlParser(handler)
    btime = time()
    for i in range(1):
        parser.parse(html)
        handler.print_hrefs()
    print time() - btime
    
def test_main_3():
    html = '''
<a href="http://anshan.soufun.com/" target="_blank">ﾰﾰ￉ﾽ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://erds.soufun.com/" target="_blank">ﾶ￵ﾶ￻ﾶ￠ￋﾹ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://jn.soufun.com/" target="_blank">ﾼￃￄￏ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://nanjing.soufun.com/" target="_blank">ￄￏﾾﾩ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://tj.soufun.com/" target="_blank">ￌ￬ﾽ￲</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://yt.soufun.com/" target="_blank">￑ￌￌﾨ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><strong>B</strong></td>
        <td align="left" valign="middle" width="16%"><strong>F</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://jl.soufun.com/" target="_blank">ﾼﾪ￁ￖ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://nc.soufun.com/" target="_blank">ￄￏﾲ�</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://tz.soufun.com/" target="_blank">ￌﾨￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://yz.soufun.com/" target="_blank">￑￯ￖ￝</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://bj.soufun.com/" target="_blank">ﾱﾱﾾﾩ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://fs.soufun.com/" target="_blank">ﾷ￰￉ﾽ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://jx.soufun.com/" target="_blank">ﾼￎ￐ￋ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://nn.soufun.com/" target="_blank">ￄￏￄ￾</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://taiyuan.soufun.com/" target="_blank">ￌﾫￔﾭ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://yc.soufun.com/" target="_blank">ￒￋﾲ�</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://bt.soufun.com/" target="_blank">ﾰ￼ￍﾷ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://fz.soufun.com/" target="_blank">ﾸﾣￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://jh.soufun.com/" target="_blank">ﾽ￰ﾻﾪ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://nt.soufun.com/" target="_blank">ￄￏￍﾨ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://taizhou.soufun.com/" target="_blank">ￌﾩￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://yinchuan.soufun.com/" target="_blank">ￒ￸ﾴﾨ</a></td>
      </tr>

      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://bd.soufun.com/" target="_blank">ﾱﾣﾶﾨ</a></td>
        <td align="left" valign="middle" width="16%"><strong>G</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://jc.soufun.com/" target="_blank">ﾽ￺ﾳￇ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://nb.soufun.com/" target="_blank">ￄ￾ﾲﾨ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://ts.soufun.com/" target="_blank">ￌￆ￉ﾽ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://yl.soufun.com/" target="_blank">ￓ￱￁ￖ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://bh.soufun.com/" target="_blank">ﾱﾱﾺﾣ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://gz.soufun.com/" target="_blank">ﾹ￣ￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://jy.soufun.com/" target="_blank">ﾽﾭￒ￵</a></td>
        <td align="left" valign="middle" width="16%"><strong>Q</strong></td>

        <td align="left" valign="middle" width="16%"><a href="http://tc.soufun.com/" target="_blank">ￌﾫﾲￖ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://yk.soufun.com/" target="_blank">ￓﾪ﾿ￚ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://baoji.soufun.com/" target="_blank">ﾱﾦﾼﾦ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://gy.soufun.com" target="_blank">ﾹ￳￑￴</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://jm.soufun.com/" target="_blank">ﾽﾭￃￅ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://qd.soufun.com/" target="_blank">ￇ￠ﾵﾺ</a></td>
        <td align="left" valign="middle" width="16%"><strong>W</strong></td>
        <td align="left" valign="middle" width="16%"><strong>Z</strong></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><strong>C</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://guilin.soufun.com/" target="_blank">ﾹ￰￁ￖ</a></td>

        <td align="left" valign="middle" width="16%"><strong>K</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://qhd.soufun.com/" target="_blank">ￇ￘ﾻￊﾵﾺ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://wuhan.soufun.com/" target="_blank">ￎ￤ﾺﾺ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://zj.soufun.com/" target="_blank">ￕ﾿ﾽﾭ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://cq.soufun.com/" target="_blank">ￖ￘ￇ￬</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://ganzhou.soufun.com/" target="_blank">ﾸￓￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://km.soufun.com/" target="_blank">￀ﾥￃ￷</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://qz.soufun.com/" target="_blank">￈ﾪￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://weihai.soufun.com/" target="_blank">ￍ￾ﾺﾣ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://zhenjiang.soufun.com/" target="_blank">ￕ￲ﾽﾭ</a></td>
      </tr>

      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://cd.soufun.com/" target="_blank">ﾳ￉ﾶﾼ</a></td>
        <td align="left" valign="middle" width="16%"><strong>H</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://ks.soufun.com/" target="_blank">￀ﾥ￉ﾽ</a></td>
        <td align="left" valign="middle" width="16%"><strong>R</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://wf.soufun.com/" target="_blank">ￎﾫﾷﾻ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://zz.soufun.com/" target="_blank">ￖﾣￖ￝</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://cz.soufun.com/" target="_blank">ﾳﾣￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://hz.soufun.com/" target="_blank">ﾺﾼￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><strong>L</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://rz.soufun.com/" target="_blank">￈ￕￕￕ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://wz.soufun.com/" target="_blank">ￎￂￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://zs.soufun.com/" target="_blank">ￖ￐￉ﾽ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://changchun.soufun.com/" target="_blank">ﾳﾤﾴﾺ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://hrb.soufun.com/" target="_blank">ﾹ￾ﾶ￻ﾱ￵</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://lz.soufun.com/" target="_blank">￀ﾼￖ￝</a></td>

        <td align="left" valign="middle" width="16%"><strong>S</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://wuxi.soufun.com/" target="_blank">ￎ￞ￎ�</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://zhuzhou.soufun.com/" target="_blank">ￖ￪ￖ￞</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://cs.soufun.com/" target="_blank">ﾳﾤ￉ﾳ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://hn.soufun.com/" target="_blank">ﾺﾣￄￏ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://ls.soufun.com/" target="_blank">￀￶ￋﾮ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://sh.soufun.com/" target="_blank">￉ￏﾺﾣ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://wj.soufun.com/" target="_blank">ￎ￢ﾽﾭ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://zh.soufun.com/" target="_blank">ￖ￩ﾺﾣ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://changshu.soufun.com/" target="_blank">ﾳﾣￊ￬</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://hd.soufun.com/" target="_blank">ﾺﾪﾵﾦ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://lyg.soufun.com/" target="_blank">￁ﾬￔￆﾸￛ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://sz.soufun.com/" target="_blank">￉￮ￛￚ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://xj.soufun.com/" target="_blank">ￎￚￂﾳￄﾾￆ￫</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://zb.soufun.com/" target="_blank">ￗￍﾲﾩ</a></td>
      </tr>

      <tr>
        <td align="left" valign="middle" width="16%"><strong>D</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://hf.soufun.com" target="_blank">ﾺￏﾷￊ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://ly.soufun.com/" target="_blank">ￂ￥￑￴</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://suzhou.soufun.com/" target="_blank">ￋￕￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://wuhu.soufun.com/" target="_blank">ￎ￟ﾺ￾</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://zhoushan.soufun.com/" target="_blank">ￖￛ￉ﾽ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://dl.soufun.com/" target="_blank">ﾴ￳￁ﾬ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://huizhou.soufun.com/" target="_blank">ﾻ￝ￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://liuzhou.soufun.com/" target="_blank">￁￸ￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://sx.soufun.com/" target="_blank">￉ￜ￐ￋ</a></td>

        <td align="left" valign="middle" width="16%"><strong>X</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://zjg.soufun.com/" target="_blank">ￕￅﾼￒﾸￛ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://dg.soufun.com/" target="_blank">ﾶﾫ￝ﾸ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://nm.soufun.com/" target="_blank">ﾺ￴ﾺￍﾺￆￌ￘</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://lf.soufun.com/" target="_blank">￀￈ﾷﾻ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://sy.soufun.com/" target="_blank">￉￲￑￴</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://xian.soufun.com/" target="_blank">ￎ￷ﾰﾲ</a></td>
        <td align="left" valign="middle" width="16%"><strong>ￆ￤ￋ￻</strong></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://dy.soufun.com/" target="_blank">ﾶﾫￓﾪ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://huaian.soufun.com/" target="_blank">ﾻﾴﾰﾲ</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://lc.soufun.com/" target="_blank">￁ￄﾳￇ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://sjz.soufun.com/" target="_blank">ￊﾯﾼￒￗﾯ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://xn.soufun.com/" target="_blank">ￎ￷ￄ￾</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://www.hkproperty.com/" target="_blank">ￏ￣ﾸￛ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle" width="16%"><a href="http://dz.soufun.com/" target="_blank">ﾵￂￖ￝</a></td>

        <td align="left" valign="middle" width="16%"><a href="http://heze.soufun.com/" target="_blank">ﾺￊￔ￳</a></td>
        <td align="left" valign="middle" width="16%"><strong>M</strong></td>
        <td align="left" valign="middle" width="16%"><a href="http://st.soufun.com/" target="_blank">￉ￇￍﾷ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://xm.soufun.com/" target="_blank">ￏￃￃￅ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://www.twproperty.com.tw/" target="_blank">ￌﾨￍ￥</a></td>
      </tr>

      <tr>
        <td align="left" valign="middle" width="16%">&nbsp;</td>
        <td align="left" valign="middle" width="16%"><a href="http://huzhou.soufun.com/" target="_blank">ﾺ￾ￖ￝</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://mianyang.soufun.com/" target="_blank">ￃ￠￑￴</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://shunde.soufun.com/" target="_blank">ￋﾳﾵￂ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://xz.soufun.com/" target="_blank">￐￬ￖ￝</a></td>
        <td align="left" height="20" valign="middle" width="16%"><a href="http://www.sgproperty.com/" target="_blank">￐ￂﾼￓￆￂ</a></td>

      </tr>
      <tr>
        <td align="left" valign="middle" width="16%">&nbsp;</td>
        <td align="left" valign="middle" width="16%"><a href="http://hs.soufun.com/" target="_blank">ﾺ￢ￋﾮ</a></td>
        <td align="left" height="20" valign="middle" width="16%"><a href="http://mas.soufun.com/" target="_blank">ￂ￭ﾰﾰ￉ﾽ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://sanya.soufun.com/" target="_blank">￈�￑ￇ</a></td>
        <td align="left" valign="middle" width="16%"><a href="http://xt.soufun.com/" target="_blank">ￏ￦ￌﾶ</a></td>

        <td align="left" height="20" valign="middle" width="16%"><a href="http://vancouver.soufun.com/" target="_blank">ￎￂﾸ￧ﾻﾪ</a></td>
      </tr>
      <tr>
        <td align="left" valign="middle">&nbsp;</td>
        <td align="left" valign="middle">&nbsp;</td>
        <td align="left" height="20" valign="middle">&nbsp;</td>
        <td align="left" valign="middle"><a href="http://sq.soufun.com/" target="_blank">ￋ￞ￇﾨ</a></td>
        <td align="left" valign="middle"><a href="http://xx.soufun.com/" target="_blank">￐ￂￏ￧</a>
'''
    handler = TestHandler(handle_comment=False, handle_text=True)
    parser = HtmlParser(handler)
    parser.parse(html)
    handler.print_hrefs()
    
    

if __name__ == '__main__':
    unittest.main()
    test_main()
    test_main_2()
    test_main_3()
```