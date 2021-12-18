import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Axios from './config-axios'
import vuetify from './plugins/vuetify'
import VueDadata from 'vue-dadata'

import VueCompositionApi from '@vue/composition-api'

Vue.use(VueCompositionApi)
Vue.use(VueDadata)

Vue.prototype.$http = Axios

const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = 'token ' + token
}
Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
