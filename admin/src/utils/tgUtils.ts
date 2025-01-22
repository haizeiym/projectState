import { getTgList } from '../api/pntg'

export interface TgConfig {
    tg_id: number
    tg_name: string
    bot_token?: string
    chat_id?: string
    url?: string
}

let tgConfigCache: TgConfig[] = []
let isInitialized = false

// 初始化缓存
export async function initTgConfigCache() {
    if (!isInitialized) {
        try {
            const data: any = await getTgList()
            tgConfigCache = data
            isInitialized = true
        } catch (error) {
            console.error('Failed to initialize TG config cache:', error)
            throw error
        }
    }
}

// 获取所有配置
export async function getAllTgConfigs(): Promise<TgConfig[]> {
    if (!isInitialized) {
        await initTgConfigCache()
    }
    return tgConfigCache
}

// 根据ID获取配置
export async function getTgConfigById(tgId: number): Promise<TgConfig | undefined> {
    if (!isInitialized) {
        await initTgConfigCache()
    }
    return tgConfigCache.find(config => config.tg_id === tgId)
}

// 添加配置到缓存
export function addTgConfigToCache(config: TgConfig) {
    const index = tgConfigCache.findIndex(item => item.tg_id === config.tg_id)
    if (index === -1) {
        tgConfigCache.push(config)
    }
}

// 更新缓存中的配置
export function updateTgConfigInCache(config: TgConfig) {
    const index = tgConfigCache.findIndex(item => item.tg_id === config.tg_id)
    if (index !== -1) {
        tgConfigCache[index] = { ...tgConfigCache[index], ...config }
    }
}

// 从缓存中删除配置
export function deleteTgConfigFromCache(tgId: number) {
    const index = tgConfigCache.findIndex(item => item.tg_id === tgId)
    if (index !== -1) {
        tgConfigCache.splice(index, 1)
    }
}

// 重置缓存
export function resetTgConfigCache() {
    tgConfigCache = []
    isInitialized = false
}

// 获取配置名称
export async function getTgConfigName(tgId: number): Promise<string> {
    if (!isInitialized) {
        await initTgConfigCache()
    }
    const config = tgConfigCache.find(item => item.tg_id === tgId)
    return config ? config.tg_name : '未知配置'
} 