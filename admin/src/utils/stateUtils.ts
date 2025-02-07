import { getStateList, createState, updateState, deleteState, getStateById } from '../api/state'

export interface StateCode {
    state_code: number
    state_name: string
}

// 状态码缓存
let stateCache: Record<number, string> | null = null

// 获取状态码列表
export async function getStateListData() {
    if (!stateCache) {
        const response = await getStateList()
        if (response && Array.isArray(response)) {
            stateCache = response.reduce(function(acc: Record<number, string>, item: StateCode) {
                acc[item.state_code] = item.state_name
                return acc
            }, {})
        } else {
            console.error('Invalid state codes data:', response)
            stateCache = {}
        }
    }
    return stateCache
}


export function getStateEntries(cache: Record<number, string>):any[] {
    const entries: [number, string][] = []
    for (const key in cache) {
        if (cache.hasOwnProperty(key)) {
            entries.push([Number(key), cache[key]])
        }
    }
    return entries
}

// 获取状态标签
export async function getStateLabel(state: number) {
    const cache = await getStateListData()
    if (!cache || Object.keys(cache).length === 0) {
        console.warn('State cache is empty')
        return '未知状态'
    }
    return cache[state] || '未知状态'
}

// 清除状态码缓存
export function clearStateCache() {
    stateCache = null
}

// 其他 API 函数
export async function addState(data: {
    state_code: number
    state_name: string
}) {
    const response = await createState(data)
    clearStateCache() // 清除缓存
    await getStateListData() // 重新获取最新状态列表
    return response
}

export async function updateStateData(stateCode: number, data: {
    state_name: string
}) {
    const response = await updateState(stateCode, data)
    clearStateCache() // 清除缓存
    await getStateListData() // 重新获取最新状态列表
    return response
}

export async function deleteStateData(stateCode: number) {
    const response = await deleteState(stateCode)
    clearStateCache() // 清除缓存
    await getStateListData() // 重新获取最新状态列表
    return response
}

export async function getStateByIdData(stateCode: number) {
    return getStateById(stateCode)
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

// 获取状态表情
export function getStateEmoji(state: number) {
    if (state > 0 && state < 2000) {
        return '🔴' // 进行中
    } else if (state >= 2000 && state < 3000) {
        return '🟡' // 警告
    } else if (state >= 3000 && state < 4000) {
        return '✅' // 成功
    } else if (state >= 4000 && state < 5000) {
        return '❌' // 错误
    }
    return '❓' // 未知状态
}