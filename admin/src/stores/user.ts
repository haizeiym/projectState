import { defineStore } from 'pinia'
import { login, logout, getInfo } from '../api/auth'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
    const token = ref(localStorage.getItem('Admin-Token') || '')
    const name = ref('')
    const email = ref('')
    const project_id = ref<number | null>(null)
    const roles = ref<string[]>([])

    async function loginAction(userInfo: any) {
        try {
            const response = await login(userInfo)
            if (response.id) {
                token.value = response.id.toString()
                localStorage.setItem('Admin-Token', token.value)
            }
            return response
        } catch (error) {
            console.error('Login failed:', error)
            throw error
        }
    }

    async function getInfoAction() {
        try {
            const response = await getInfo()
            name.value = response.username
            email.value = response.email
            project_id.value = response.project_id
            return response
        } catch (error) {
            console.error('Get user info failed:', error)
            throw error
        }
    }

    async function logoutAction() {
        try {
            await logout()
            token.value = ''
            name.value = ''
            email.value = ''
            project_id.value = null
            roles.value = []
            localStorage.removeItem('Admin-Token')
        } catch (error) {
            console.error('Logout failed:', error)
            throw error
        }
    }

    return {
        token,
        name,
        email,
        project_id,
        roles,
        login: loginAction,
        getInfo: getInfoAction,
        logout: logoutAction
    }
}) 