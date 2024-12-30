<template>
    <div class="project-add">
        <h2>添加项目</h2>
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
            <el-form-item label="节点ID">
                <el-input v-model="form.node_id" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="handleSubmit">创建</el-button>
                <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import StateSelect from '../components/StateSelect.vue'

const router = useRouter()
const form = ref({
    project_name: '',
    description: '',
    state: 0,
    node_id: ''
})

// 提交表单
const handleSubmit = async () => {
    try {
        await axios.post('/api/project/create', form.value)
        ElMessage.success('创建成功')
        router.push('/projects')
    } catch (error) {
        ElMessage.error('创建失败：' + (error.response?.data?.message || error.message))
    }
}

// 取消
const handleCancel = () => {
    router.push('/projects')
}
</script>

<style scoped>
.project-add {
    padding: 20px;
}
</style>
