<template>
    <div class="project-add">
        <h2>添加项目</h2>
        <div class="description-text">
            <el-alert title="默认添加节点，名称，描述，状态相同" type="info" :closable="false" class="mb-20" />
        </div>
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
            <el-form-item label="项目名称" prop="project_name">
                <el-input v-model="form.project_name" />
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.description" type="textarea" />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="handleSubmit">创建</el-button>
                <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { createProject } from '../../api/project'
import { createNode } from '../../api/node'
import { updateUserProjects } from '../../api/auth'
import { userStore } from '../../stores/user'
import { getStateListData } from '../../utils/stateUtils'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref({
    project_name: '',
    description: '',
    state: 0,
})

const rules = {
    project_name: [
        { required: true, message: '请输入项目名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ]
}

const stateOptions = ref<Record<number, string> | null>(null)

const handleSubmit = async () => {
    if (!formRef.value) return

    try {
        await formRef.value.validate()
        loading.value = true

        // 创建节点
        const nodeResponse: any = await createNode({
            node_name: form.value.project_name,
            description: form.value.description,
            state: form.value.state
        })

        // 创建项目
        const projectResponse: any = await createProject({
            node_id: nodeResponse.node_id,
            project_name: form.value.project_name,
            description: form.value.description,
            state: form.value.state
        })

        // 更新用户的 project_ids
        if (userStore.userInfo.value) {
            const projectIds = userStore.userInfo.value.projectIds || []
            projectIds.push(projectResponse.project_id)
            // 更新后端数据库
            await updateUserProjects(userStore?.userInfo.value?.id || 0, projectIds)
            userStore.updateUserInfo({
                ...userStore.userInfo.value,
                projectIds
            })
        }

        ElMessage.success('项目创建成功')
        router.push('/main/projects')
    } catch (error: any) {
        ElMessage.error('项目创建失败：' + (error.response?.data?.message || error.message || '名称错误'))
    } finally {
        loading.value = false
    }
}

const handleCancel = () => {
    router.push('/main/projects')
}

onMounted(async () => {
    stateOptions.value = await getStateListData()
    const firstStateCode = Object.keys(stateOptions.value || {})[0]
    if (firstStateCode) {
        form.value.state = Number(firstStateCode)
    }
})
</script>

<style scoped>
.project-add {
    padding: 20px;
}

.description-text {
    margin-bottom: 20px;
}

.mb-20 {
    margin-bottom: 20px;
}
</style>
