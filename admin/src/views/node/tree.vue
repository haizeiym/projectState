<template>
    <div class="node-tree">
        <div class="header">
            <h2>节点管理</h2>
            <el-button type="primary" @click="handleAddNode">添加节点</el-button>
        </div>
        <el-tree ref="treeRef" :data="treeData" :props="defaultProps" node-key="node_id" default-expand-all
            :expand-on-click-node="false">
            <template #default="{ node, data }">
                <div class="custom-tree-node">
                    <span>{{ node.label }}</span>
                    <span class="node-state">
                        <el-tag :type="getStateType(data.state)">
                            {{ getStateName(data.state) }}
                        </el-tag>
                    </span>
                    <span class="node-actions">
                        <el-button type="primary" link @click="handleEdit(data)">
                            编辑
                        </el-button>
                        <el-button type="danger" link @click="handleDelete(node, data)">
                            删除
                        </el-button>
                    </span>
                </div>
            </template>
        </el-tree>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
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
    const projectId = route.params.projectId
    router.push(`/main/node/add/${projectId}`)
}

const handleEdit = (data: any) => {
    router.push(`/main/node/edit/${data.node_id}`)
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

.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}

.node-state {
    margin: 0 20px;
}

.node-actions {
    margin-left: auto;
}
</style>