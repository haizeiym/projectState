<template>
    <div class="project-add">
        <h2>添加项目</h2>
        <el-form :model="form" label-width="120px">
            <el-form-item label="项目名称">
                <el-input v-model="form.project_name" />
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.description" />
            </el-form-item>
            <el-form-item label="状态">
                <el-input v-model="form.state" />
            </el-form-item>
            <el-form-item label="节点ID">
                <el-input v-model="form.node_id" />
            </el-form-item>

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
    project_name: '',
    description: '',
    state: 0,
    node_id: 0,
})

const submitForm = async () => {
    try {
        // 添加表单验证
        if (!form.value.project_name || form.value.project_name.trim() === '') {
            ElMessage.warning('请输入项目名称')
            return
        }
        const response = await axios.post('/api/project/create', form.value, {
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })

        if (response.data) {
            ElMessage.success('项目创建成功')
            router.push('/projects')
        } else {
            ElMessage.error(response.data.message || '创建失败')
        }
    } catch (error) {
        console.error('Error creating project:', error)
        if (error.response?.status === 500) {
            ElMessage.error('服务器错误，请稍后重试')
        } else if (error.response?.status === 401) {
            ElMessage.error('登录已过期，请重新登录')
            router.push('/login')
        } else {
            ElMessage.error(error.response?.data?.message || '创建项目失败，请重试')
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
</script>
