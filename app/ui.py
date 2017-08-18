#coding: utf8
from tornado.web import UIModule
from urllib.parse import urlparse


class PaginationUI(UIModule):
    """ <div class="pagination font-alt">
          <ul class="pagination">
            <li><a href="#"><i class="fa fa-angle-left"></i></a></li>
            <li><a href="#">1</a></li>
            <li class="active"><span>2</span></li>
            <li><a href="#">3</a></li>
            <li><a href="#">4</a></li>
            <li><a href="#"><i class="fa fa-angle-right"></i></a></li>
          </ul>
        </div>
    """    
    def render(self, paginator, uri):
        if paginator.paginator.num_pages == 1: # 不是只有1页
            return self.render_string('_ui_data.html', ui_data='')

        r = urlparse(uri)
        query = '&'.join([ segment for segment in r.query.split('&') if not segment.strip().startswith('page=') ])

        uri = '%s?%s' % (r.path, query)
        page_segment='&page=' if query else 'page='


        buff = []
        buff.append(u'<div class="pagination font-alt">')
        # buff.append(u'  <ul class="pagination"><span class="record-count">共<span class="number">%s</span>条记录</span>' % paginator.count)
        buff.append(u'  <ul class="pagination">')
        if paginator.has_previous():
            buff.append(u'<li>')
            buff.append(u'    <a href="%s%s%s">« </a>' % (uri, page_segment, paginator.previous_page_number()))
            buff.append(u'</li>')

        display_nums, left_nums = 5, 2
        left_begin = paginator.number - left_nums if paginator.number - left_nums >= 1 else 1
        left_end = paginator.number
        
        right_nums = display_nums - (left_end - left_begin) - 1
        if paginator.number == paginator.paginator.num_pages: # 已经是最后1页
            right_begin = right_end = paginator.number
        else:  
            right_begin = (paginator.number + 1 if paginator.number + 1 <= paginator.paginator.num_pages else paginator.paginator.num_pages)
            right_end = (paginator.number + right_nums if paginator.number + right_nums <= paginator.paginator.num_pages else paginator.paginator.num_pages) + 1
        for x in range(left_begin, left_end):
            buff.append(u'<li><a href="%s%s%s">%s</a></li>' % (uri, page_segment, x, x))
        buff.append(u'<li class="active"><a href="?page=%s">%s</a></li>' % (paginator.number, paginator.number))
        for x in range(right_begin, right_end):
            buff.append(u'<li><a href="%s%s%s">%s</a></li>' % (uri, page_segment, x, x))

        if paginator.has_next():
            buff.append(u'<li>')
            buff.append(u'    <a href="%s%s%s"> »</a>' % (uri, page_segment, paginator.next_page_number()))
            buff.append(u'</li>')

        buff.append(u'  </ul>')
        buff.append(u'</div>')
        
        return self.render_string('_ui_data.html', ui_data=''.join(buff))
