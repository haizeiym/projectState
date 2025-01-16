import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/login',
            component: () => import('../views/login/index.vue')
        },
        {
            path: '/register',
            component: () => import('../views/register/index.vue')
        },
        {
            path: '/main',
            component: () => import('../views/dashboard/index.vue'),
            children: [
                {
                    path: 'projects',
                    component: () => import('../views/ProjectList.vue')
                },
                {
                    path: 'project/add',
                    component: () => import('../views/ProjectAdd.vue')
                },
                {
                    path: 'node/:nodeId',
                    component: () => import('../views/NodeTree.vue'),
                    props: (route) => ({
                        nodeId: Number(route.params.nodeId),
                        projectId: Number(route.query.projectId)
                    })
                }
            ]
        },
        {
            path: '/',
            redirect: '/main/projects'
        }
    ]
})

// 路由守卫
router.beforeEach((to, _from, next) => {
    const token = localStorage.getItem('Admin-Token')
    if (to.path !== '/login' && to.path !== '/register' && !token) {
        next('/login')
    } else {
        next()
    }
})

export default router