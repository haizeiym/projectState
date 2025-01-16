import request from '../utils/request'

export function createPNTG(data: any) {
    return request({
        url: '/api/pntg/create',
        method: 'post',
        data
    })
}

export function updatePNTG(projectId: number, data: any) {
    return request({
        url: `/api/pntg/update/${projectId}`,
        method: 'put',
        data
    })
}

export function getPNTGByProjectId(projectId: number) {
    return request({
        url: `/api/pntg/get/${projectId}`,
        method: 'get'
    })
} 