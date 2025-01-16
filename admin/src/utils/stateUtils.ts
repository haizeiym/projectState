import request from './request'

export interface StateCode {
    state_code: number
    state_name: string
    description: string
}

// 状态码缓存
let stateCache: Record<number, string> | null = null

// 获取状态码列表
export async function getStateList() {
    return request({
        url: '/api/statecode/list',
        method: 'get'
    })
}

// 获取状态标签
export async function getStateLabel(state: number) {
    const cache = await getStateCache()
    if (!cache) return '未知状态'
    return cache[state] || '未知状态'
}

// 获取状态码缓存
export async function getStateCache() {
    if (!stateCache) {
        try {
            const response = await getStateList()
            if (Array.isArray(response.data)) {
                stateCache = response.data.reduce((acc: Record<number, string>, item: StateCode) => {
                    acc[item.state_code] = item.state_name
                    return acc
                }, {})
            } else {
                console.error('Invalid state codes data:', response.data)
                stateCache = {}
            }
        } catch (error) {
            console.error('Failed to get state codes:', error)
            stateCache = {}
        }
    }
    return stateCache
}

// 清除状态码缓存
export function clearStateCache() {
    stateCache = null
}

// 其他 API 函数
export async function addState(data: {
    state_code: number
    state_name: string
    description: string
}) {
    const response = await request({
        url: '/api/statecode/create',
        method: 'post',
        data
    })
    clearStateCache()
    return response
}

export async function updateState(stateCode: number, data: {
    state_name: string
    description: string
}) {
    const response = await request({
        url: `/api/statecode/update/${stateCode}`,
        method: 'put',
        data
    })
    clearStateCache()
    return response
}

export async function deleteState(stateCode: number) {
    const response = await request({
        url: `/api/statecode/delete/${stateCode}`,
        method: 'delete'
    })
    clearStateCache()
    return response
}

export async function getStateById(stateCode: number) {
    return request({
        url: `/api/statecode/get/${stateCode}`,
        method: 'get'
    })
}

// 状态码颜色映射
export const stateColorMap: { [key: number]: string } = {
    0: 'success',   // 正常
    1: 'warning',   // 警告
    2: 'danger',    // 错误
    3: 'info'       // 其他
}

// 获取状态颜色
export function getStateColor(stateCode: number) {
    return stateColorMap[stateCode] || 'info'
}

// 获取状态类型
export function getStateType(state: number) {
    if (typeof state === 'string') {
        state = Number(state)
    }
    if (state >= 1000 && state < 2000) {
        return 'info'
    } else if (state >= 2000 && state < 3000) {
        return 'warning'
    } else if (state >= 3000 && state < 4000) {
        return 'success'
    } else if (state >= 4000 && state < 5000) {
        return 'danger'
    }
    return 'info'
}