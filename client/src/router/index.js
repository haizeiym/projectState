import { createRouter, createWebHistory } from 'vue-router'
import ProjectDetails from '../views/ProjectDetails.vue'
import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:8000'  // 假设后端运行在 8000 端口
axios.defaults.withCredentials = true  // 允许跨域请求携带凭证


const routes = [
    {
        path: '/',
        name: 'ProjectDetails',
        component: ProjectDetails
    }
    // Add more routes here as needed
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
export { axios }  // 导出配置好的 axios 实例