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
                    component: () => import('../views/project/list.vue'),
                    name: 'Projects',
                    meta: { title: '项目列表', icon: 'list' }
                },
                {
                    path: 'project/add',
                    component: () => import('../views/project/add.vue'),
                    name: 'ProjectAdd',
                    meta: { title: '添加项目', icon: 'plus' },
                },  
                {
                    path: 'project/edit/:id',
                    component: () => import('../views/project/edit.vue'),
                    name: 'ProjectEdit',
                    meta: { title: '编辑项目', icon: 'edit' },
                },
                {
                    path: 'node/tree/:nodeId',
                    component: () => import('../views/node/tree.vue'),
                    name: 'NodeTree',
                    meta: { title: '节点管理', icon: 'tree' }
                },
                {
                    path: 'node/add/:nodeId',
                    component: () => import('../views/node/add.vue'),
                    name: 'NodeAdd',
                    meta: { title: '添加节点', icon: 'plus' }
                },
                {
                    path: 'node/edit/:nodeId',
                    component: () => import('../views/node/edit.vue'),
                    name: 'NodeEdit',
                    meta: { title: '编辑节点', icon: 'edit' }
                },
                {
                    path: 'state/add',
                    component: () => import('../views/state/Add.vue'),
                    name: 'StateAdd',
                    meta: { title: '添加状态', icon: 'plus' }
                },
                {
                    path: 'state/edit/:stateId',
                    component: () => import('../views/state/Edit.vue'),
                    name: 'StateEdit',
                    meta: { title: '编辑状态', icon: 'edit' }
                },
                {
                    path: 'state/management',
                    component: () => import('../views/state/Management.vue'),
                    name: 'StateManagement',
                    meta: { title: '状态管理', icon: 'edit' }
                },
                {
                    path: 'tg/management',
                    component: () => import('../views/tg/Management.vue'),
                    name: 'TgManagement',
                    meta: { title: 'Telegram 管理', icon: 'edit' }
                },
                {
                    path: 'tg/add',
                    component: () => import('../views/tg/Add.vue'),
                    name: 'TgAdd',
                    meta: { title: '添加 Telegram', icon: 'plus' }
                },
                {
                    path: 'tg/edit/:tgId',
                    component: () => import('../views/tg/Edit.vue'),
                    name: 'TgEdit',
                    meta: { title: '编辑 Telegram', icon: 'edit' }
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