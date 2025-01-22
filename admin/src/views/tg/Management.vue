<template>
    <PageLayout title="Telegram 管理">
        <template #actions>
            <el-button type="primary" @click="handleAdd">
                <el-icon>
                    <Plus />
                </el-icon>添加配置
            </el-button>
            <el-button type="primary" @click="handleBackToProjects">
                <el-icon>
                    <Back />
                </el-icon>返回项目列表
            </el-button>
        </template>

        <el-table :data="tgList" v-loading="loading" style="width: 100%">
            <el-table-column prop="tg_id" label="ID" width="100" />
            <el-table-column prop="tg_name" label="名称" />
            <el-table-column label="操作" width="200">
                <template #default="{ row }">
                    <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
                    <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </PageLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import PageLayout from '../../components/PageLayout.vue'
import { getTgList, deletePNTG } from '../../api/pntg'

const router = useRouter()
const loading = ref(false)
const tgList = ref([])

const fetchTgList = async () => {
    try {
        loading.value = true
        const response: any = await getTgList()
        tgList.value = response
    } catch (error: any) {
        ElMessage.error('获取列表失败：' + error.message)
    } finally {
        loading.value = false
    }
}

const handleAdd = () => {
    router.push('/main/tg/add')
}

const handleBackToProjects = () => {
    router.push('/main/projects')
}

const handleEdit = (row: any) => {
    router.push(`/main/tg/edit/${row.tg_id}`)
}

const handleDelete = async (row: any) => {
    try {
        await ElMessageBox.confirm('确定要删除该配置吗？', '提示', {
            type: 'warning'
        })
        await deletePNTG(row.tg_id)
        ElMessage.success('删除成功')
        fetchTgList()
    } catch (error: any) {
        if (error !== 'cancel') {
            ElMessage.error('删除失败：' + error.message)
        }
    }
}

onMounted(() => {
    fetchTgList()
})
</script>