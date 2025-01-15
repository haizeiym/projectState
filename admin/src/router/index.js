import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import ProjectList from '../views/ProjectList.vue'
import ProjectAdd from '../views/ProjectAdd.vue'
import NodeAdd from '../views/NodeAdd.vue'
import NodeTree from '../views/NodeTree.vue'
import ProjectEdit from '../views/ProjectEdit.vue'
import StateManagement from '../views/StateManagement.vue'
import AddState from '../views/AddState.vue'
import Layout from '../components/Layout.vue'

// 设置 axios 默认配置
axios.defaults.baseURL = 'http://localhost:8000'  // 假设后端运行在 8000 端口
axios.defaults.withCredentials = true  // 允许跨域请求携带凭证

const routes = [
    {
        path: '/',
        redirect: '/login'  // 修改：重定向到登录页
    },
    // 添加：登录和注册路由
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/login/index.vue'),
        meta: {
            title: 'Login',
            requiresAuth: false
        }
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/register/index.vue'),
        meta: {
            title: 'Register',
            requiresAuth: false
        }
    },
    // 原有路由移动到 /main 下
    {
        path: '/main',
        component: Layout,
        meta: { requiresAuth: true },
        children: [
            {
                path: 'projects',
                name: 'ProjectList',
                component: ProjectList
            },
            {
                path: 'project/add',
                name: 'ProjectAdd',
                component: ProjectAdd
            },
            {
                path: 'node/add',
                name: 'NodeAdd',
                component: NodeAdd
            },
            {
                path: 'node/:nodeId',
                name: 'nodeTree',
                component: NodeTree,
                props: true
            },
            {
                path: 'project/edit/:projectId',
                name: 'ProjectEdit',
                component: ProjectEdit
            },
            {
                path: 'state-management',
                component: StateManagement
            },
            {
                path: 'add-state',
                component: AddState
            },
            // 添加：仪表盘路由
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: () => import('../views/dashboard/index.vue'),
                meta: { title: 'Dashboard', icon: 'dashboard' }
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 修改路由守卫逻辑
router.beforeEach((to, from, next) => {
    // 检查路由是否需要认证
    if (to.matched.some(record => record.meta.requiresAuth !== false)) {
        // 检查是否已登录
        const token = localStorage.getItem('Admin-Token')
        if (!token) {
            next({
                path: '/login',
                query: { redirect: to.fullPath }
            })
            return
        }
    }
    next()
})

export default router
export { axios }  // 导出配置好的 axios 实例