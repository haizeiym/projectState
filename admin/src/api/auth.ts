import request from '../utils/request'

export function login(data: any) {
    return request({
        url: '/admin/auth/login/',
        method: 'post',
        data,
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

export function logout() {
    return request({
        url: '/admin/auth/logout/',
        method: 'post'
    })
}

export function getCSRFToken() {
    return request({
        url: '/api/csrf-token/',
        method: 'get'
    })
}

export function getInfo() {
    return request({
        url: '/api/user/info',
        method: 'get'
    })
}

export function register(data: any) {
    return request({
        url: '/admin/auth/register/',
        method: 'post',
        data: {
            username: data.username,
            password: data.password,
            captcha: data.captcha
        }
    })
} 