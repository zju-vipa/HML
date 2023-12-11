import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import './assets/css/global.css'

Vue.config.productionTip = false
Vue.config.silent = true

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
