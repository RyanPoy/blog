#coding: utf8

left_menus = lambda: [
    {
        'name': '博客管理',
        'uri': '/admin',
        'submenus': [
            { 'name': '文章', 'uri': '/articles' },
            { 'name': '标签', 'uri': '/tags' },
            { 'name': '系列', 'uri': '/series' },
            { 'name': '图片', 'uri': '/images' },
            { 'name': '单页面', 'uri': '/pages' },
            { 'name': '友链', 'uri': '/links' },
        ]
    }
]
