import request from '../utils/request'

export function login(data: any) {
    return request({
        url: '/admin/login/',
        method: 'post',
        data
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
        url: '/admin/logout/',
        method: 'post'
    })
}

export function register(data: any) {
    return request({
        url: '/admin/register/',
        method: 'post',
        data
    })
}

export function getCSRFToken() {
    return request({
        url: '/api/csrf-token/',
        method: 'get'
    })
} 