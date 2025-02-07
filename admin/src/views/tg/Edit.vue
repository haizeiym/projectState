<template>
    <div class="edit-container">
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
            <el-form-item label="配置名称" prop="tg_name">
                <el-input v-model="form.tg_name" placeholder="请输入配置名称" />
            </el-form-item>
            <el-form-item label="Bot Token" prop="bot_token">
                <el-input v-model="form.bot_token" placeholder="请输入 Bot Token" />
            </el-form-item>
            <el-form-item label="Chat ID" prop="chat_id">
                <el-input v-model="form.chat_id" placeholder="请输入 Chat ID" />
            </el-form-item>
            <el-form-item label="URL" prop="url">
                <el-input v-model="form.url" placeholder="请输入 URL" />
            </el-form-item>
            <el-form-item label="发送状态码" prop="state_code">
                <el-radio-group v-model="form.state_code">
                    <el-radio label="0">全部状态</el-radio>
                    <el-radio v-for="[code, name] in Object.entries(stateCache || {})" :key="code" :label="code">
                        {{ name }}
                    </el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="handleSubmit" :loading="loading">保存</el-button>
                <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { updatePNTG } from '../../api/pntg'
import { getTgConfigById, updateTgConfigInCache } from '../../utils/tgUtils'
import { getStateListData } from '../../utils/stateUtils'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref({
    tg_name: '',
    bot_token: '',
    chat_id: '',
    url: '',
    state_code: ''
})

const rules = {
    tg_name: [
        { required: true, message: '请输入配置名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ],
    bot_token: [
        { required: true, message: '请输入 Bot Token', trigger: 'blur' }
    ],
    chat_id: [
        { required: true, message: '请输入 Chat ID', trigger: 'blur' }
    ],
    url: [
        { required: true, message: '请输入 URL', trigger: 'blur' }
    ]
}

const stateCache = ref<Record<number, string> | null>(null)

const fetchTgConfig = async () => {
    try {
        const tgId = Number(route.params.tgId)
        const data: any = await getTgConfigById(tgId)
        if (data) {
            form.value = {
                tg_name: data.tg_name,
                bot_token: data.bot_token || '',
                chat_id: data.chat_id || '',
                url: data.url || '',
                state_code: data.state_code || ''
            }
        }
    } catch (error: any) {
        ElMessage.error('获取配置信息失败')
    }
}

const handleSubmit = async () => {
    if (!formRef.value) return

    try {
        await formRef.value.validate()
        loading.value = true

        const tgId = Number(route.params.tgId)
        const response: any = await updatePNTG(tgId, form.value)
        updateTgConfigInCache(response)
        ElMessage.success('更新成功')
        router.push('/main/tg/management')
    } catch (error: any) {
        ElMessage.error(error.message || '保存失败')
    } finally {
        loading.value = false
    }
}

const handleCancel = () => {
    router.push('/main/tg/management')
}

onMounted(async () => {
    stateCache.value = await getStateListData()
    fetchTgConfig()
})
</script>

<style scoped>
.edit-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}
</style>