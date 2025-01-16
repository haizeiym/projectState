<template>
    <div class="project-list">
        <div class="page-header">
            <h2>项目列表</h2>
            <el-button type="primary" @click="router.push('/main/project/add')">
                <el-icon>
                    <Plus />
                </el-icon>新增项目
            </el-button>
        </div>

        <el-table v-loading="loading" :data="projects" style="width: 100%">
            <el-table-column prop="project_id" label="项目ID" width="100" />
            <el-table-column prop="project_name" label="项目名称" />
            <el-table-column prop="description" label="描述" show-overflow-tooltip />
            <el-table-column label="操作" width="250">
                <template #default="scope">
                    <el-button type="primary" size="small"
                        @click="handleViewNodes(scope.row.node_id, scope.row.project_id)"
                        :disabled="!scope.row.node_id">
                        节点管理
                    </el-button>
                    <el-button type="warning" size="small" @click="handleEdit(scope.row)">
                        编辑
                    </el-button>
                    <el-button type="danger" size="small" @click="handleDelete(scope.row)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getProjectList } from '../api/project'

const router = useRouter()
const loading = ref(false)
const projects = ref([])

const fetchProjects = async () => {
    loading.value = true
    try {
        const response = await getProjectList()
        projects.value = response.data || []
    } catch (error: any) {
        projects.value = []
        ElMessage.error('获取项目列表失败：' + (error.response?.data?.message || error.message))
    } finally {
        loading.value = false
    }
}

const handleViewNodes = (nodeId: number, projectId: number) => {
    router.push({ path: `/main/node/${nodeId}`, query: { projectId } })
}

const handleEdit = (row: any) => {
    router.push(`/main/project/edit/${row.project_id}`)
}

const handleDelete = async (row: any) => {
    try {
        await ElMessageBox.confirm('确定要删除该项目吗？', '提示', {
            type: 'warning'
        })
        // TODO: 实现删除逻辑
        ElMessage.success('删除成功')
        await fetchProjects()
    } catch {
        // 用户取消删除
    }
}

onMounted(() => {
    fetchProjects()
})
</script>

<style scoped lang="scss">
.project-list {
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;

        h2 {
            margin: 0;
            font-size: 20px;
            color: #303133;
        }
    }
}
</style>