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
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import StateTag from '../components/StateTag.vue'
import { getProjectById, updateProject } from '../api/project'
import { getPNTGByProjectId, updatePNTG } from '../api/pntg'

const router = useRouter()
const route = useRoute()
const projectId = Number(route.params.id)

const form = ref({
    project_name: '',
    description: '',
    state: 0,
    bot_token: '',
    chat_id: '',
    url: ''
})

const fetchProject = async () => {
    try {
        const [projectResponse, pntgResponse] = await Promise.all([
            getProjectById(projectId),
            getPNTGByProjectId(projectId)
        ])

        form.value = {
            ...projectResponse,
            ...pntgResponse
        }
    } catch (error) {
        ElMessage.error('获取项目信息失败：' + (error.response?.data?.message || error.message))
    }
}

const handleSubmit = async () => {
    try {
        // 更新项目信息
        await updateProject(projectId, {
            project_name: form.value.project_name,
            description: form.value.description,
            state: form.value.state
        })

        // 更新 PNTG 配置
        await updatePNTG(projectId, {
            bot_token: form.value.bot_token,
            chat_id: form.value.chat_id,
            url: form.value.url
        })

        ElMessage.success('更新成功')
        router.push('/main/projects')
    } catch (error) {
        ElMessage.error('更新失败：' + (error.response?.data?.message || error.message))
    }
}

const handleCancel = () => {
    router.push('/main/projects')
}

onMounted(() => {
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