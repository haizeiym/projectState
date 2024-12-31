<template>
    <PageLayout title="项目列表">
        <template #actions>
            <el-button type="primary" @click="$router.push('/project/add')">
                添加项目
            </el-button>
        </template>

        <el-table v-loading="loading" :data="projects" style="width: 100%">
            <!-- <el-table-column prop="project_id" label="项目ID" width="180" /> -->
            <el-table-column prop="project_name" label="项目名称" width="180" />
            <el-table-column prop="description" label="描述" width="180" />
            <el-table-column prop="state" label="状态" width="180">
                <template #default="scope">
                    <template v-if="scope.row.node_id">
                        <StateTag :modelValue="scope.row.state" />
                    </template>
                    <span v-else class="no-node-state">未关联节点</span>
                </template>
            </el-table-column>
            <el-table-column label="操作" width="280">
                <template #default="scope">
                    <el-button-group>
                        <el-button type="primary" size="small" @click="handleViewNodes(scope.row.node_id)"
                            :disabled="!scope.row.node_id">
                            查看节点
                        </el-button>
                        <el-button type="warning" size="small" @click="handleEdit(scope.row.project_id)">
                            修改
                        </el-button>
                        <el-button type="danger" size="small" @click="handleDelete(scope.row.project_id)">
                            删除
                        </el-button>
                    </el-button-group>
                </template>
            </el-table-column>
        </el-table>
    </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import StateTag from '../components/StateTag.vue'
import PageLayout from '../components/PageLayout.vue'

const projects = ref([])
const loading = ref(false)
const router = useRouter()

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
        await ElMessageBox.confirm('确认要删除该项目及其所有相关节点吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
            message: '此操作将永久删除该项目及其所有相关节点，是否继续？'
        })

        loading.value = true

        // 1. 先获取项目信息，获取node_id
        const projectResponse = await axios.get(`/api/project/get/${projectId}`)
        const nodeId = projectResponse.data.node_id

        // 2. 如果有关联节点，先删除节点及其子节点
        if (nodeId) {
            try {
                await axios.delete(`/api/node/delete/${nodeId}`)
            } catch (error) {
                console.error('删除节点失败:', error)
                throw new Error('删除节点失败：' + (error.response?.data?.message || error.message))
            }
        }

        // 3. 删除项目
        const response = await axios.delete(`/api/project/delete/${projectId}`)
        if (response.data.status === 'success') {
            ElMessage.success('删除项目及相关节点成功')
            await fetchProjects() // 重新加载项目列表
        } else {
            throw new Error(response.data.message || '删除项目失败')
        }
    } catch (error) {
        console.error(error)
        if (error !== 'cancel') {
            ElMessage.error(error.message || '删除失败')
        }
    } finally {
        loading.value = false
    }
}

const handleViewNodes = (nodeId) => {
    if (nodeId) {
        router.push(`/node/${nodeId}`)
    }
}

const handleEdit = (projectId) => {
    router.push(`/project/edit/${projectId}`)
}

onMounted(() => {
    fetchProjects()
})
</script>

<style scoped>
.no-node-state {
    color: var(--el-text-color-secondary);
    font-size: 13px;
}
</style>