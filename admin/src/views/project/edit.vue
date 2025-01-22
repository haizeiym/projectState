<template>
    <div class="edit-container">
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
            <el-form-item label="项目名称" prop="project_name">
                <el-input v-model="form.project_name" placeholder="请输入项目名称" />
            </el-form-item>
            <el-form-item label="项目描述" prop="description">
                <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入项目描述" />
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
import { getProjectById, updateProject } from '../../api/project'
const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref({
    project_name: '',
    description: '',
})

const rules = {
    project_name: [
        { required: true, message: '请输入项目名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ],
    description: [
        { required: true, message: '请输入项目描述', trigger: 'blur' },
        { max: 500, message: '最多 500 个字符', trigger: 'blur' }
    ]
}

const fetchProject = async () => {
    try {
        const projectId = Number(route.params.id)
        const data: any = await getProjectById(projectId)
        if (data) {
            form.value = {
                project_name: data.project_name,
                description: data.description,
            }
        }
    } catch (error: any) {
        ElMessage.error('获取项目信息失败')
    }
}

const handleSubmit = async () => {
    if (!formRef.value) return

    try {
        await formRef.value.validate()
        loading.value = true

        const projectId = Number(route.params.id)
        await updateProject(projectId, form.value)
        ElMessage.success('更新成功')
        router.push('/main/projects')
    } catch (error: any) {
        ElMessage.error(error.message || '保存失败')
    } finally {
        loading.value = false
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
.edit-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}
</style>