<template>
    <div class="state-management">
        <div class="header">
            <h2>状态管理</h2>
            <div class="header-actions">
                <el-button type="primary" @click="handleAddState">
                    <el-icon>
                        <Plus />
                    </el-icon>添加状态
                </el-button>
                <el-button type="primary" @click="handleBackToProjects">
                    <el-icon>
                        <Back />
                    </el-icon>返回项目列表
                </el-button>
            </div>
        </div>
        <el-table :data="stateData" style="width: 100%">
            <el-table-column prop="state_code" label="状态代码" />
            <el-table-column prop="state_name" label="状态名称" />
            <el-table-column label="操作" width="280">
                <template #default="scope">
                    <div class="action-buttons">
                        <el-button type="primary" link @click="handleEdit(scope.row)" class="action-button">
                            <el-icon>
                                <Edit />
                            </el-icon>编辑
                        </el-button>
                        <el-button type="danger" link @click="handleDelete(scope.row)" class="action-button">
                            <el-icon>
                                <Delete />
                            </el-icon>删除
                        </el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, Back } from '@element-plus/icons-vue'
import { getStateList, deleteState } from '../../api/state'

const router = useRouter()
const stateData = ref([])

const fetchStateList = async () => {
    try {
        const response: any = await getStateList()
        stateData.value = response || []
    } catch (error: any) {
        ElMessage.error('获取状态列表失败')
        console.error('Error fetching state list:', error)
    }
}

const handleAddState = () => {
    router.push('/main/state/add')
}

const handleBackToProjects = () => {
    router.push('/main/projects')
}

const handleEdit = (data: any) => {
    router.push(`/main/state/edit/${data.state_code}`)
}

const handleDelete = (data: any) => {
    ElMessageBox.confirm('确定要删除该状态吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        try {
            await deleteState(data.state_code)
            ElMessage.success('删除成功')
            await fetchStateList()
        } catch (error) {
            ElMessage.error('删除失败')
        }
    })
}

onMounted(() => {
    fetchStateList()
})
</script>

<style scoped>
.state-management {
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

.header-actions {
    display: flex;
    gap: 10px;
}

.action-buttons {
    display: flex;
    gap: 8px;
}

.action-button {
    display: flex;
    align-items: center;
    gap: 4px;
}

.action-button .el-icon {
    margin-right: 2px;
}
</style>