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
            <el-table-column label="操作" width="120">
                <template #default="scope">
                    <el-button type="danger" size="small" @click="handleDelete(scope.row.project_id)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const projects = ref([])
const loading = ref(false)

const fetchProjects = async () => {
    loading.value = true
    try {
        const response = await axios.get('/api/project/list')
        if (!response.data || !Array.isArray(response.data)) {
            throw new Error('返回数据格式错误')
        }
        projects.value = response.data
    } catch (error) {
        projects.value = [] // 发生错误时清空数据
        ElMessage.error('获取项目列表失败：' + (error.response?.data?.message || error.message))
    } finally {
        loading.value = false
    }
}

const handleDelete = async (projectId) => {
    try {
        await ElMessageBox.confirm('确认要删除该项目吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        })

        loading.value = true
        const response = await axios.delete(`/api/project/delete/${projectId}`)
        console.log(response.data)
        if (response.data.status === 'success') {
            ElMessage.success('删除成功')
            await fetchProjects() // 重新加载项目列表
        } else {
            ElMessage.error('删除失败：' + response.data.message)
        }
    } catch (error) {
        console.log(error)
        if (error !== 'cancel') {
            ElMessage.error('删除失败：' + (error.response?.data?.message || error.message))
        }
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchProjects()
})
</script>