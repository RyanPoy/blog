import Vue from 'vue'
import Router from 'vue-router'
import Signin from '@/components/page/Signin'
import Admin from '@/components/page/Admin'
import AdminTag from '@/components/page/AdminTag'
import AdminLink from '@/components/page/AdminLink'
import AdminSeries from '@/components/page/AdminSeries'
import AdminImage from '@/components/page/AdminImage'
import AdminPage from '@/components/page/AdminPage'
import AdminArticle from '@/components/page/AdminArticle'


Vue.use(Router)

export default new Router({
  routes: [
    { path: '/signin', name: 'Signin', component: Signin},
    {
      path: '/admin',  name: 'Admin',  component: Admin,
      children: [
        { path: 'tags', name: 'AdminTag', component: AdminTag },
        { path: 'links', name: 'AdminLink', component: AdminLink },
        { path: 'series', name: 'AdminSeries', component: AdminSeries },
        { path: 'images', name: 'AdminImage', component: AdminImage },
        { path: 'pages', name: 'AdminPage', component: AdminPage },
        { path: 'articles', name: 'AdminArticle', component: AdminArticle }
      ]
    }
  ]
})
