import Vue from 'vue'
import Router from 'vue-router'
import AdminTag from '@/components/page/AdminTag'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/admin/tag', name: 'AdminTag', component: AdminTag
    }
  ]
})
