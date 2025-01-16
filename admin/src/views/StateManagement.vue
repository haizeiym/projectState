<template>
    <PageLayout title="状态管理">
        <div class="toolbar">
            <el-button type="primary" @click="openAddState">添加状态</el-button>
            <el-button type="default" @click="closeStateManagement">关闭</el-button>
        </div>
        <el-table :data="filteredStateCodes" style="width: 100%" v-loading="loading">
            <el-table-column prop="state_code" label="状态码" width="180" />
            <el-table-column label="状态名称" width="180">
                <template #default="scope">
                    <el-tag :type="getStateType(scope.row.state_code)">
                        {{ scope.row.state_name }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作" width="160">
                <template #default="scope">
                    <el-button type="warning" size="small" @click="openEditDialog(scope.row.state_code)">修改</el-button>
                    <el-button type="danger" size="small"
                        @click="confirmDeleteState(scope.row.state_code)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination v-if="pagination.total > pagination.pageSize" background layout="prev, pager, next"
            :total="pagination.total" :page-size="pagination.pageSize" @current-change="handlePageChange" />
        <EditStateDialog ref="editStateDialog" @state-updated="fetchStateCodes" />
    </PageLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import PageLayout from '../components/PageLayout.vue'
import EditStateDialog from './EditStateEdit.vue'
import { getStateList, deleteState } from '../api/state'
import { getStateType } from '../utils/stateUtils'

const stateCodes = ref([])
const filteredStateCodes = ref([])
const loading = ref(false)
const router = useRouter()

const pagination = ref({
    currentPage: 1,
    pageSize: 10,
    total: 0
})

const editStateDialog = ref(null)

const fetchStateCodes = async () => {
    loading.value = true
    try {
        const response = await getStateList()
        stateCodes.value = response
        pagination.value.total = stateCodes.value.length
        filterStateCodes()
    } catch (error) {
        ElMessage.error('获取状态码失败：' + (error.response?.data?.message || error.message))
    } finally {
        loading.value = false
    }
}

const filterStateCodes = () => {
    filteredStateCodes.value = stateCodes.value.slice(0, pagination.value.pageSize)
}

const handlePageChange = (page) => {
    pagination.value.currentPage = page
    const start = (page - 1) * pagination.value.pageSize
    const end = start + pagination.value.pageSize
    filteredStateCodes.value = stateCodes.value.slice(start, end)
}

const closeStateManagement = () => {
    router.push('/projects')
}

const openAddState = () => {
    router.push('/add-state')
}

const openEditDialog = (stateCode) => {
    editStateDialog.value.open(stateCode)
}

const confirmDeleteState = (stateCode) => {
    ElMessageBox.confirm('此操作将永久删除该状态, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(() => {
        handleDeleteState(stateCode)
    }).catch(() => {
        ElMessage.info('已取消删除')
    })
}

const handleDeleteState = async (stateCode) => {
    try {
        await deleteState(stateCode)
        ElMessage.success('状态删除成功')
        fetchStateCodes()
    } catch (error) {
        ElMessage.error('状态删除失败：' + (error.response?.data?.message || error.message))
    }
}

onMounted(() => {
    fetchStateCodes()
})
</script>

<style scoped>
.toolbar {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-bottom: 20px;
}

.el-table {
    margin-bottom: 20px;
}
</style>