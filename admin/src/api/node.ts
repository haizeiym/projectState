import request from '../utils/request'

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
        method: 'put',
        data
    })
}

export function deleteNode(nodeId: number) {
    return request({
        url: `/api/node/delete/${nodeId}`,
        method: 'delete'
    })
}

export function getNodeById(nodeId: number) {
    return request({
        url: `/api/node/get/${nodeId}`,
        method: 'get'
    })
}

export function getNodeTree(nodeId: number) {
    return request({
        url: `/api/node/tree/${nodeId}`,
        method: 'get'
    })
}

export function batchUpdateNodes(data: any) {
    return request({
        url: '/api/node/batch_update',
        method: 'post',
        data
    })
} 