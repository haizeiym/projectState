import request from '../utils/request'

export function createProject(data: any) {
    return request({
        url: '/api/project/create',
        method: 'post',
        data
    })
}

export function updateProject(projectId: number, data: any) {
    return request({
        url: `/api/project/update/${projectId}`,
        method: 'post',
        data
    })
}

export function deleteProject(projectId: number) {
    return request({
        url: `/api/project/delete/${projectId}`,
        method: 'delete'
    })
}

export function getProjectById(projectId: number) {
    return request({
        url: `/api/project/get/${projectId}`,
        method: 'get'
    })
}

export function getProjectList(projectIds: number[]) {
    return request({
        url: '/api/project/list',
        method: 'get',
        params: {
            project_ids: JSON.stringify(projectIds)
        }
    })
} 