import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import VxeUIBase from 'vxe-pc-ui'
import 'vxe-pc-ui/es/style.css'

import VxeUITable from 'vxe-table'
import 'vxe-table/es/style.css'
createApp(App).use(VxeUIBase).use(VxeUITable).mount('#app')
