import Vue from 'vue'
import App from './App.vue'
import {initRouter} from './router'
import './theme/index.less'
import Antd from 'ant-design-vue'
import '@/mock'
import store from './store'
import 'animate.css/source/animate.css'
import Plugins from '@/plugins'
import {initI18n} from '@/utils/i18n'
import bootstrap from '@/bootstrap'
import moment from 'moment'
import VeLine from 'v-charts/lib/line.common'

const router = initRouter(store.state.setting.asyncRoutes)
const i18n = initI18n('CN', 'US')

Vue.use(Antd)
Vue.config.productionTip = false
Vue.use(Plugins)
Vue.filter('dayFormat', function(dataStr, pattern='YYYY-MM-DD'){
	return moment(dataStr).format(pattern)
})
Vue.filter('secFormat', function(dataStr, pattern='YYYY-MM-DD HH:mm:ss'){
	return moment(dataStr).format(pattern)
})
Vue.component(VeLine.name, VeLine)

bootstrap({router, store, i18n, message: Vue.prototype.$message})

new Vue({
  router,
  store,
  i18n,
  render: h => h(App),
}).$mount('#app')
