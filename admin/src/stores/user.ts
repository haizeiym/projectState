import { login, logout, getInfo } from '../api/auth'
import { ref } from 'vue'

// 创建用户状态管理
const token = ref(localStorage.getItem('Admin-Token') || '')
const userInfo = ref<any>(null)

export const useUser = () => {
    async function loginAction(userInfo: any) {
        try {
            const response: any = await login(userInfo)
            if (response && response.id) {
                token.value = response.id.toString()
                localStorage.setItem('Admin-Token', token.value)
                return response
            }
            throw new Error('Login failed')
        } catch (error) {
            console.error('Login error:', error)
            throw error
        }
    }

    async function getInfoAction() {
        try {
            const response = await getInfo()
            userInfo.value = response
            return response
        } catch (error) {
            console.error('GetInfo error:', error)
            throw error
        }
    }

    async function logoutAction() {
        try {
            await logout()
            token.value = ''
            userInfo.value = null
            localStorage.removeItem('Admin-Token')
        } catch (error) {
            console.error('Logout error:', error)
            throw error
        }
    }

    return {
        token,
        userInfo,
        login: loginAction,
        getInfo: getInfoAction,
        logout: logoutAction
    }
}

// 导出一个全局实例
export const userStore = useUser() 