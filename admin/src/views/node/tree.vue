<template>
    <div class="node-tree">
        <div class="header">
            <h2>节点管理</h2>
            <div class="header-actions">
                <el-button type="primary" @click="handleAddNode">
                    <el-icon>
                        <Plus />
                    </el-icon>添加节点
                </el-button>
                <el-button @click="handleClose">
                    <el-icon>
                        <Back />
                    </el-icon>返回项目列表
                </el-button>
            </div>
        </div>
        <el-table :data="treeData" style="width: 100%" row-key="node_id"
            :tree-props="{ children: 'children', hasChildren: 'hasChildren' }" default-expand-all>
            <el-table-column prop="node_name" label="节点名称" />
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="state" label="状态">
                <template #default="scope">
                    <StateTag :modelValue="scope.row.state" />
                </template>
            </el-table-column>
            <el-table-column label="操作" width="280">
                <template #default="scope">
                    <div class="action-buttons">
                        <el-button type="success" link @click="handleAddChild(scope.row)" class="action-button">
                            <el-icon>
                                <Plus />
                            </el-icon>添加子节点
                        </el-button>
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
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Back, Edit, Delete } from '@element-plus/icons-vue'
import { getNodeTree, deleteNode } from '../../api/node'
import StateTag from '../../components/StateTag.vue'

const route = useRoute()
const router = useRouter()
const treeData = ref([])

const fetchNodeTree = async () => {
    try {
        const nodeId = Number(route.params.nodeId)
        const response: any = await getNodeTree(nodeId)
        treeData.value = response.children || []
    } catch (error: any) {
        ElMessage.error('获取节点树失败')
        console.error('Error fetching node tree:', error)
    }
}

const handleAddNode = () => {
    const nodeId = route.params.nodeId
    router.push(`/main/node/add/${nodeId}?parent_id=${nodeId}`)
}

const handleAddChild = (data: any) => {
    router.push(`/main/node/add/${route.params.nodeId}?parent_id=${data.node_id}`)
}

const handleEdit = (data: any) => {
    router.push(`/main/node/edit/${data.node_id}?parent_id=${route.params.nodeId}`)
}

const handleDelete = (data: any) => {
    ElMessageBox.confirm('确定要删除该节点吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        try {
            await deleteNode(data.node_id)
            ElMessage.success('删除成功')
            await fetchNodeTree()
        } catch (error) {
            ElMessage.error('删除失败')
        }
    })
}

const handleClose = () => {
    router.push('/main/projects')
}

onMounted(() => {
    fetchNodeTree()
})
</script>

<style scoped>
.node-tree {
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