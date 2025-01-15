import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

// 创建应用实例
const app = createApp(App)

// 创建 Pinia 实例
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// 安装插件
app.use(pinia)  // 确保 Pinia 最先安装
app.use(ElementPlus)
app.use(router)

// 挂载应用
app.mount('#app')

// 导出 pinia 实例供外部使用
export { pinia }