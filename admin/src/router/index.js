import { createRouter, createWebHistory } from 'vue-router'
import ProjectList from '../views/ProjectList.vue'
import ProjectAdd from '../views/ProjectAdd.vue'
import NodeAdd from '../views/NodeAdd.vue'

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