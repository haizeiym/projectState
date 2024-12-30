<template>
    <div class="project-edit">
        <h2>修改项目</h2>
        <el-form :model="form" label-width="120px">
            <el-form-item label="项目名称">
                <el-input v-model="form.project_name" />
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.description" type="textarea" />
            </el-form-item>
            <el-form-item label="状态">
                <StateSelect v-model="form.state" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="handleSubmit">保存</el-button>
                <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import StateSelect from '../components/StateSelect.vue'

const route = useRoute()
const router = useRouter()
const form = ref({
    project_name: '',
    description: '',
    state: 0
})

// 获取项目信息
const fetchProject = async () => {
    try {
        const response = await axios.get(`/api/project/get/${route.params.projectId}`)
        form.value = response.data
    } catch (error) {
        ElMessage.error('获取项目信息失败')
    }
}

// 提交表单
const handleSubmit = async () => {
    try {
        await axios.post(`/api/project/update/${route.params.projectId}`, form.value)
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

onMounted(() => {
    fetchProject()
})
</script>

<style scoped>
.project-edit {
    padding: 20px;
}
</style> 