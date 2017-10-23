import Vue from 'vue'
import Router from 'vue-router'
import AdminTag from '@/components/page/AdminTag'
import AdminLink from '@/components/page/AdminLink'
import AdminSeries from '@/components/page/AdminSeries'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/admin/tags', name: 'AdminTag', component: AdminTag },
    { path: '/admin/links', name: 'AdminLink', component: AdminLink },
    { path: '/admin/series', name: 'AdminSeries', component: AdminSeries }
  ]
})
