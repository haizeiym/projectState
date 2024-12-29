<template>
    <div class="project-list">
        <h2>项目列表</h2>
        <el-button type="primary" @click="$router.push('/project/add')">添加项目</el-button>
        <el-button type="primary" @click="$router.push('/node/add')">添加节点</el-button>

        <el-table :data="projects" style="width: 100%; margin-top: 20px;">
            <el-table-column prop="id" label="ID" width="180" />
            <el-table-column prop="name" label="名称" width="180" />
            <!-- 根据实际ProjectModel字段添加更多列 -->
        </el-table>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const projects = ref([])

const fetchProjects = async () => {
    try {
        const response = await axios.get('/api/project/list')
        projects.value = response.data
    } catch (error) {
        console.error('Error fetching projects:', error)
    }
}

onMounted(() => {
    fetchProjects()
})
</script>