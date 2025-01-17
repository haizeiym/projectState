<template>
    <div class="project-list">
        <div class="header">
            <h2>项目列表</h2>
            <el-button type="primary" @click="handleAdd" v-if="hasManagePermission">添加项目</el-button>
        </div>
        <el-table :data="filteredProjects" style="width: 100%" v-loading="loading">
            <el-table-column prop="project_id" label="项目ID" width="100" />
            <el-table-column prop="project_name" label="项目名称" />
            <el-table-column prop="description" label="项目描述" />
            <el-table-column label="操作" width="280">
                <template #default="scope">
                    <el-button type="primary" size="small" @click="handleEdit(scope.row)"
                        v-if="hasProjectPermission(scope.row.project_id)">
                        编辑
                    </el-button>
                    <el-button type="success" size="small" @click="handleNodes(scope.row)"
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
import { userStore } from '../../stores/user'

const router = useRouter()
const loading = ref(false)
const projects = ref([])

const filteredProjects = computed(() => projects.value)

const hasProjectPermission = (projectId: number) => {
    const userProjectIds = userStore.userInfo.value?.projectIds ?? []
    return userProjectIds.includes(projectId)
}

const hasManagePermission = computed(() => {
    const userProjectIds = userStore.userInfo.value?.projectIds ?? []
    return userProjectIds.length > 0
})

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

const handleNodes = (row: any) => {
    router.push(`/main/node/tree/${row.node_id}`)
}

const handleDelete = (row: any) => {
    ElMessageBox.confirm('确定要删除该项目吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        try {
            await deleteProject(row.project_id)
            ElMessage.success('删除成功')
            fetchProjects()
        } catch (error) {
            ElMessage.error('删除失败')
        }
    }).catch(() => {
        // 用户取消删除操作
    })
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

.header h2 {
    margin: 0;
}
</style>