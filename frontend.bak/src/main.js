// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import ElementUI from 'element-ui'
import { Message } from 'element-ui'
import './assets/theme/element-black/index.css'
// import 'element-ui/lib/theme-chalk/index.css'

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(ElementUI)


// http response 拦截器
axios.interceptors.response.use(
  response => {
    return response;
  }, error => {
    if (error.response) {
      if (error.response.status == 401) {
        router.replace({
            path: '/signin',
            query: {redirect: router.currentRoute.fullPath}
        })
      } else {
        Message.error({
          message: '加载失败'
        })
      }
    }
    return Promise.reject(error)
  }
);

/* eslint-disable no-new */
// new Vue({
//   el: '#app',
//   router,
//   template: '<App/>',
//   components: { App }
// })


new Vue({
  router,
  // store,
  render: h => h(App)
}).$mount('#app')
