import request from '../utils/request'

export function getNodeTree(projectId: number) {
    return request({
        url: `/api/node/tree/${projectId}`,
        method: 'get'
    })
}

export function getNodeList(projectId: number) {
    return request({
        url: `/api/node/list/${projectId}`,
        method: 'get'
    })
}

export function getNodeById(nodeId: number) {
    return request({
        url: `/api/node/get/${nodeId}`,
        method: 'get'
    })
}

export function createNode(data: any) {
    return request({
        url: '/api/node/create',
        method: 'post',
        data
    })
}

export function updateNode(nodeId: number, data: any) {
    return request({
        url: `/api/node/update/${nodeId}`,
        method: 'post',
        data
    })
}

export function batchUpdateNode(data: any) {
    return request({
        url: '/api/node/batch_update',
        method: 'post',
        data
    })
}

export function deleteNode(nodeId: number) {
    return request({
        url: `/api/node/delete/${nodeId}`,
        method: 'delete'
    })
} 