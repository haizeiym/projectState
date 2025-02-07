import request from '../utils/request';

export function createPNTG(data: {
    tg_name: string;
    bot_token: string;
    chat_id: string;
    url: string;
    state_code: string;
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
    state_code: string;
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

export function sendMessage(botToken: string, chatId: string, openUrl: string, message: string) {
    const url = `https://api.telegram.org/bot${botToken}/sendMessage`
    const payload = {
        chat_id: chatId,
        text: message,
        parse_mode: 'Markdown',
        reply_markup: {
            inline_keyboard: [[{ text: "打开查看", url: openUrl }]]
        }
    }

    return request({
        url,
        method: 'post',
        data: payload
    })
}