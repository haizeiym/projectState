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

export function getInfo() {
    return request({
        url: '/api/user/info',
        method: 'get'
    })
}

export function logout() {
    return request({
        url: '/admin/auth/logout/',
        method: 'post'
    })
}

export function register(data: any) {
    return request({
        url: '/admin/auth/register/',
        method: 'post',
        data,
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

export function getCSRFToken() {
    return request({
        url: '/api/csrf-token/',
        method: 'get'
    })
} 