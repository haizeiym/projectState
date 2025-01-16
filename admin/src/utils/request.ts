import axios from 'axios'
import { ElMessage } from 'element-plus'
import config from '../config'

const service = axios.create({
    baseURL: config.API_URL,
    timeout: 5000,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
})

// 请求拦截器
service.interceptors.request.use(
    config => {
        // 从 cookie 获取 CSRF token
        const token = localStorage.getItem('Admin-Token')
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`
        }

        // 获取 CSRF token
        const csrfToken = document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1]
        
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken
        }

        return config
    },
    error => {
        console.log(error)
        return Promise.reject(error)
    }
)

// 响应拦截器
service.interceptors.response.use(
    response => {
        const res = response.data
        return res
    },
    error => {
        console.log('err' + error)
        ElMessage({
            message: error.response?.data?.error || '请求失败',
            type: 'error',
            duration: 5 * 1000
        })
        return Promise.reject(error)
    }
)

export default service 