import request from '../utils/request';

export function createPNTG(data: {
    project_id: number;
    bot_token: string;
    chat_id: string;
    url: string;
}) {
    return request({
        url: '/api/pntg/create',
        method: 'post',
        data
    })
}

export function updatePNTG(projectId: number, data: {
    bot_token: string;
    chat_id: string;
    url: string;
}) {
    return request({
        url: `/api/pntg/update/${projectId}`,
        method: 'post',
        data
    })
}

export function getPNTGByProjectId(projectId: number) {
    return request({
        url: `/api/pntg/get/${projectId}`,
        method: 'get'
    })
}

export function deletePNTG(projectId: number) {
    return request({
        url: `/api/pntg/delete/${projectId}`,
        method: 'delete'
    })
} 