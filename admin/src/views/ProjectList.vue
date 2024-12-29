<template>
    <div class="project-list">
        <h2>项目列表</h2>
        <el-button type="primary" @click="$router.push('/project/add')">添加项目</el-button>
        <el-button type="primary" @click="$router.push('/node/add')">添加节点</el-button>

        <el-table v-loading="loading" :data="projects" style="width: 100%; margin-top: 20px;">
            <el-table-column prop="project_id" label="项目ID" width="180" />
            <el-table-column prop="project_name" label="项目名称" width="180" />
            <el-table-column prop="description" label="描述" width="180" />
            <el-table-column prop="state" label="状态" width="180" />
            <el-table-column prop="node_id" label="节点ID" width="180" />
        </el-table>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const projects = ref([])
const loading = ref(false)

const fetchProjects = async () => {
    loading.value = true
    try {
        const response = await axios.get('/api/project/list')
        projects.value = response.data
    } catch (error) {
        ElMessage.error('获取项目列表失败：' + error.message)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchProjects()
})
</script>