import request from '../utils/request';

export function createPNTG(data: {
    tg_name: string;
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

export function updatePNTG(tgId: number, data: {
    tg_name: string;
    bot_token: string;
    chat_id: string;
    url: string;
}) {
    return request({
        url: `/api/pntg/update/${tgId}`,
        method: 'post',
        data
    })
}

export function getPNTGByTgId(tgId: number) {
    return request({
        url: `/api/pntg/get/${tgId}`,
        method: 'get'
    })
}

export function deletePNTG(tgId: number) {
    return request({
        url: `/api/pntg/delete/${tgId}`,
        method: 'delete'
    })
}

export function getTgList() {
    return request({
        url: '/api/pntg/list',
        method: 'get'
    })
} 