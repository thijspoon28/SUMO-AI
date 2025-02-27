import './assets/index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { initializeApiClient } from './api/api'

const app = createApp(App)

app.use(createPinia())
app.use(router)

initializeApiClient()

app.mount('#app')
