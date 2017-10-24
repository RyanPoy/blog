import Vue from 'vue'
import Router from 'vue-router'
import AdminTag from '@/components/page/AdminTag'
import AdminLink from '@/components/page/AdminLink'
import AdminSeries from '@/components/page/AdminSeries'
import AdminImage from '@/components/page/AdminImage'
import AdminPage from '@/components/page/AdminPage'
import AdminArticle from '@/components/page/AdminArticle'


Vue.use(Router)

export default new Router({
  routes: [
    { path: '/admin/tags', name: 'AdminTag', component: AdminTag },
    { path: '/admin/links', name: 'AdminLink', component: AdminLink },
    { path: '/admin/series', name: 'AdminSeries', component: AdminSeries },
    { path: '/admin/images', name: 'AdminImage', component: AdminImage },
    { path: '/admin/pages', name: 'AdminPage', component: AdminPage },
    { path: '/admin/articles', name: 'AdminArticle', component: AdminArticle }
  ]
})
