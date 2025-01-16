import request from '../utils/request'

export function getProjectList() {
    return request({
        url: '/api/project/list',
        method: 'get'
    })
}

export function deleteProject(projectId: number) {
    return request({
        url: `/api/project/delete/${projectId}`,
        method: 'delete'
    })
}

export function updateProject(projectId: number, data: any) {
    return request({
        url: `/api/project/update/${projectId}`,
        method: 'put',
        data
    })
} 