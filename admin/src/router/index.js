import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import ProjectList from '../views/ProjectList.vue'
import ProjectAdd from '../views/ProjectAdd.vue'
import NodeAdd from '../views/NodeAdd.vue'

// 设置 axios 默认配置
axios.defaults.baseURL = 'http://localhost:8000'  // 假设后端运行在 8000 端口
axios.defaults.withCredentials = true  // 允许跨域请求携带凭证

const routes = [
    {
        path: '/',
        redirect: '/projects'
    },
    {
        path: '/projects',
        name: 'ProjectList',
        component: ProjectList
    },
    {
        path: '/project/add',
        name: 'ProjectAdd',
        component: ProjectAdd
    },
    {
        path: '/node/add',
        name: 'NodeAdd',
        component: NodeAdd
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
export { axios }  // 导出配置好的 axios 实例