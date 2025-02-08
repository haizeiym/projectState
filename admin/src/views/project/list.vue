<template>
    <div class="project-list">
        <div class="header">
            <h2>项目列表</h2>
            <div class="button-group">
                <el-button type="primary" @click="toggleProjectIdVisibility">
                    {{ showProjectId ? '隐藏项目ID' : '显示项目ID' }}
                </el-button>
                <el-button type="primary" @click="handleAdd">添加项目</el-button>
                <el-button type="primary" @click="handleStateManagement">状态管理</el-button>
                <el-button type="primary" @click="handleTgManagement">TG管理</el-button>
            </div>
        </div>
        <el-table :data="filteredProjects" style="width: 100%" v-loading="loading">
            <el-table-column v-if="showProjectId" prop="project_id" label="项目ID" width="100" />
            <el-table-column prop="project_name" label="项目名称" />
            <el-table-column prop="description" label="项目描述" />
            <el-table-column label="状态" width="100">
                <template #default="scope">
                    <StateTag :modelValue="scope.row.state" />
                </template>
            </el-table-column>
            <el-table-column label="操作" width="280">
                <template #default="scope">
                    <el-button type="primary" size="small" @click="handleEdit(scope.row)"
                        v-if="hasProjectPermission(scope.row.project_id)">
                        编辑
                    </el-button>
                    <el-button type="success" size="small" @click="handleNodeManage(scope.row)"
                        v-if="hasProjectPermission(scope.row.project_id)">
                        节点
                    </el-button>
                    <el-button type="danger" size="small" @click="handleDelete(scope.row)"
                        v-if="hasProjectPermission(scope.row.project_id)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getProjectList, deleteProject } from '../../api/project'
import { updateUserProjects } from '../../api/auth'
import { userStore } from '../../stores/user'
import { deleteNode } from '../../api/node'
import StateTag from '../../components/StateTag.vue'

const router = useRouter()
const loading = ref(false)
const projects = ref([])
const showProjectId = ref(false)

const filteredProjects = computed(() => projects.value)

const hasProjectPermission = (projectId: number) => {
    const userProjectIds = userStore.userInfo.value?.projectIds ?? []
    return userProjectIds.includes(projectId)
}


const fetchProjects = async () => {
    try {
        loading.value = true
        const projectIds = userStore.userInfo.value?.projectIds ?? []

        if (projectIds.length > 0) {
            const response = await getProjectList(projectIds)
            projects.value = response.data || []
        } else {
            projects.value = []
        }
    } catch (error: any) {
        ElMessage.error('获取项目列表失败')
        console.error('Error fetching projects:', error)
    } finally {
        loading.value = false
    }
}

const handleAdd = () => {
    router.push('/main/project/add')
}

const handleEdit = (row: any) => {
    router.push(`/main/project/edit/${row.project_id}`)
}

const handleNodeManage = (row: any) => {
    router.push({
        path: `/main/node/tree/${row.node_id}`,
        query: {
            project_name: row.project_name,
            description: row.description
        }
    })
}

const handleDelete = (row: any) => {
    ElMessageBox.confirm('确定要删除该项目吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        try {
            await deleteNode(row.node_id)
            await deleteProject(row.project_id)

            // 更新用户的 project_ids
            if (userStore.userInfo.value?.id) {
                const projectIds = userStore.userInfo.value.projectIds || []
                const updatedProjectIds = projectIds.filter(id => id !== row.project_id)
                // 使用新的 handleUpdateUserProjects 函数
                await handleUpdateUserProjects(userStore.userInfo.value.id, updatedProjectIds)
                userStore.updateUserInfo({
                    ...userStore.userInfo.value,
                    projectIds: updatedProjectIds
                })
            }

            ElMessage.success('删除成功')
            fetchProjects()
        } catch (error) {
            ElMessage.error('删除失败')
        }
    }).catch(() => {
        // 用户取消删除操作
    })
}

const handleStateManagement = () => {
    router.push('/main/state/management')
}

const handleTgManagement = () => {
    router.push('/main/tg/management')
}

const toggleProjectIdVisibility = () => {
    showProjectId.value = !showProjectId.value
}

const handleUpdateUserProjects = async (userId: number, projectIds: number[]) => {
    try {
        await updateUserProjects(userId, projectIds)
        ElMessage.success('更新成功')
        await fetchProjects()
    } catch (error) {
        console.error('更新失败:', error)
        ElMessage.error('更新失败')
    }
}

onMounted(() => {
    if (userStore.userInfo.value) {
        fetchProjects()
    }
})

watch(() => userStore.userInfo.value, (newVal) => {
    if (newVal) {
        fetchProjects()
    } else {
        projects.value = []
    }
})
</script>

<style scoped>
.project-list {
    padding: 20px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.button-group {
    display: flex;
    gap: 10px;
}

.header h2 {
    margin: 0;
    flex-grow: 1;
}
</style>