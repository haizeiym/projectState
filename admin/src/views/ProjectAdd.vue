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

const router = useRouter()
const form = ref({
    name: '',
    // 根据ProjectModel添加更多字段
})

const submitForm = async () => {
    try {
        await axios.post('/api/project/create', form.value)
        router.push('/projects')
    } catch (error) {
        console.error('Error creating project:', error)
    }
}
</script>
