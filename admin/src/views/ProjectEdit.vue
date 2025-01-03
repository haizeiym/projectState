<template>
    <PageLayout title="修改项目">
        <el-form :model="form" label-width="120px">
            <el-form-item label="状态">
                <StateTag :modelValue="form.state" />
            </el-form-item>
            <el-form-item label="项目名称">
                <el-input v-model="form.project_name" />
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.description" type="textarea" />
            </el-form-item>
            <el-form-item label="Bot Token">
                <el-input v-model="form.bot_token" />
            </el-form-item>
            <el-form-item label="Chat ID">
                <el-input v-model="form.chat_id" />
            </el-form-item>
            <el-form-item label="URL">
                <el-input v-model="form.url" />
            </el-form-item>
            <el-form-item label="发送消息状态码">
                <el-select v-model="selectedStateCodes" multiple placeholder="选择状态码">
                    <el-option v-for="value in Object.keys(stateOptions)" :key="value" :label="stateOptions[value]"
                        :value="Number(value)">
                        <el-tag :type="getStateType(Number(value))">{{ stateOptions[value] }}</el-tag>
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button-group>
                    <el-button type="primary" @click="handleSubmit">保存</el-button>
                    <el-button @click="handleCancel">取消</el-button>
                </el-button-group>
            </el-form-item>
        </el-form>
    </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import StateTag from '../components/StateTag.vue'
import PageLayout from '../components/PageLayout.vue'
import { getStateCache, getStateType } from '../utils/stateUtils'

const route = useRoute()
const router = useRouter()
const form = ref({
    project_name: '',
    description: '',
    state: 0,
    node_id: 0,
    bot_token: '',
    chat_id: '',
    url: '',
    state_codes: ''
})

const selectedStateCodes = ref([])
const stateOptions = ref({})

// 获取项目信息
const fetchProject = async () => {
    try {
        const response = await axios.get(`/api/project/get/${route.params.projectId}`)
        form.value = response.data

        // 获取 PNTG 信息
        const pntgResponse = await axios.get(`/api/pntg/get/${route.params.projectId}`)
        Object.assign(form.value, pntgResponse.data)

        // Initialize selectedStateCodes from form.state_codes
        selectedStateCodes.value = form.value.state_codes.split(',').map(Number)
    } catch (error) {
        ElMessage.error('获取项目信息失败')
    }
}

// 提交表单
const handleSubmit = async () => {
    try {
        // Update form.state_codes with selectedStateCodes
        form.value.state_codes = selectedStateCodes.value.join(',')

        // 创建一个新的对象，去除 state 字段
        const { state, ...formData } = form.value

        await axios.post(`/api/project/update/${route.params.projectId}`, formData)

        // 更新 PNTG 记录
        await axios.post(`/api/pntg/update/${route.params.projectId}`, {
            bot_token: form.value.bot_token,
            chat_id: form.value.chat_id,
            url: form.value.url,
            state_codes: form.value.state_codes
        })

        ElMessage.success('修改成功')
        router.push('/projects')
    } catch (error) {
        ElMessage.error('修改失败')
    }
}

// 取消
const handleCancel = () => {
    router.push('/projects')
}

// Fetch state options on component mount
onMounted(async () => {
    stateOptions.value = await getStateCache()
    fetchProject()
})
</script>

<style scoped>
:deep(.el-input.is-disabled .el-input__wrapper) {
    background-color: var(--el-fill-color-light);
}

:deep(.el-input-group__append) {
    padding: 0 8px;
    color: var(--el-text-color-secondary);
}
</style>