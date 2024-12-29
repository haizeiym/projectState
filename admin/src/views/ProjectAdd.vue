<template>
    <div class="project-add">
        <h2>添加项目</h2>
        <el-form :model="form" label-width="120px">
            <el-form-item label="项目名称">
                <el-input v-model="form.name" />
            </el-form-item>
            <!-- 根据ProjectModel添加更多表单项 -->

            <el-form-item>
                <el-button type="primary" @click="submitForm">创建项目</el-button>
                <el-button @click="$router.push('/projects')">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const form = ref({
    name: '',
    // 根据ProjectModel添加更多字段
})

const submitForm = async () => {
    try {
        // 从 localStorage 获取 token
        const token = localStorage.getItem('token')
        await axios.post('/api/project/create', form.value, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        router.push('/projects')
    } catch (error) {
        console.error('Error creating project:', error)
        // 添加错误提示
        ElMessage.error('创建项目失败：' + (error.response?.data?.message || error.message))
    }
}
</script>
