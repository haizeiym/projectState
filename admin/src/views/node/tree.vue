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
        <el-tree ref="treeRef" :data="treeData" :props="defaultProps" node-key="node_id" default-expand-all
            :expand-on-click-node="false">
            <template #default="{ node, data }">
                <div class="custom-tree-node">
                    <span>{{ node.label }}</span>
                    <div class="node-operations">
                        <span class="node-actions">
                            <div class="description-wrapper">
                                <span class="description-text">{{ data.description }}</span>
                            </div>
                            <span class="node-state">
                                <el-tag :type="getStateType(data.state)">
                                    {{ getStateName(data.state) }}
                                </el-tag>
                            </span>
                            <el-button type="success" link @click="handleAddChild(data)" class="action-button">
                                <el-icon>
                                    <Plus />
                                </el-icon>添加子节点
                            </el-button>
                            <el-button type="primary" link @click="handleEdit(data)" class="action-button">
                                <el-icon>
                                    <Edit />
                                </el-icon>编辑
                            </el-button>
                            <el-button type="danger" link @click="handleDelete(node, data)" class="action-button">
                                <el-icon>
                                    <Delete />
                                </el-icon>删除
                            </el-button>
                        </span>
                    </div>
                </div>
            </template>
        </el-tree>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Back, Edit, Delete } from '@element-plus/icons-vue'
import { getNodeTree, deleteNode } from '../../api/node'

const route = useRoute()
const router = useRouter()
const treeRef = ref()
const treeData = ref([])

const defaultProps = {
    children: 'children',
    label: 'node_name'
}

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

const handleDelete = (_node: any, data: any) => {
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

const getStateType = (state: number) => {
    const stateMap: { [key: number]: string } = {
        0: '',
        1: 'success',
        2: 'warning',
        3: 'danger'
    }
    return stateMap[state] || ''
}

const getStateName = (state: number) => {
    const stateMap: { [key: number]: string } = {
        0: '未开始',
        1: '正常',
        2: '警告',
        3: '错误'
    }
    return stateMap[state] || '未知'
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

.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    font-size: 14px;
    padding: 8px;
}

.node-operations {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
}

.description-wrapper {
    width: 300px;
    min-height: 22px;
    padding: 4px 8px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.description-text {
    display: block;
    color: #606266;
    line-height: 1.4;
    word-break: break-all;
    white-space: pre-wrap;
}

.node-state {
    display: flex;
    align-items: center;
    min-width: 80px;
    justify-content: center;
}

.node-actions {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-left: auto;
    flex-shrink: 0;
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