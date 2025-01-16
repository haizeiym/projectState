import request from '../utils/request'

export function createState(data: any) {
    return request({
        url: '/api/statecode/create',
        method: 'post',
        data
    })
}

export function updateState(stateCode: number, data: any) {
    return request({
        url: `/api/statecode/update/${stateCode}`,
        method: 'put',
        data
    })
}

export function deleteState(stateCode: number) {
    return request({
        url: `/api/statecode/delete/${stateCode}`,
        method: 'delete'
    })
}

export function getStateList() {
    return request({
        url: '/api/statecode/list',
        method: 'get'
    })
}

export function getStateById(stateCode: number) {
    return request({
        url: `/api/statecode/get/${stateCode}`,
        method: 'get'
    })
} 