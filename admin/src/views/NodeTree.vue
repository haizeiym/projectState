<template>
    <div class="node-tree">
        <div class="header">
            <h2>节点树形展示</h2>
            <div class="header-buttons">
                <el-button type="primary" @click="handleAddNode">添加节点</el-button>
                <el-button type="default" @click="handleClose">关闭</el-button>
            </div>
        </div>

        <!-- 当前节点信息 -->
        <el-card class="current-node" v-if="currentNode">
            <template #header>
                <div class="card-header">
                    <span>当前节点信息</span>
                </div>
            </template>
            <div class="node-info">
                <div class="info-row">
                    <div class="info-col">
                        <p><strong>节点ID:</strong>{{ currentNode.node_id }}</p>
                        <p><strong>节点名称:</strong>{{ currentNode.node_name }}</p>
                        <p><strong>描述:</strong>{{ currentNode.description }}</p>
                    </div>
                    <div class="info-col">
                        <p><strong>状态:</strong>
                            <StateSelect v-model="currentNode.state" disabled />
                        </p>
                        <p><strong>父节点ID:</strong>{{ currentNode.parent_id }}</p>
                    </div>
                </div>
            </div>
        </el-card>

        <!-- 子节点列表 -->
        <h3 class="subtitle">子节点列表</h3>
        <el-table v-loading="loading" :data="nodes" row-key="node_id" style="width: 100%; margin-top: 20px;">
            <el-table-column prop="node_id" label="节点ID" width="180" />
            <el-table-column prop="node_name" label="节点名称" width="180" />
            <el-table-column prop="description" label="描述" width="180" />
            <el-table-column prop="state" label="状态" width="180">
                <template #default="scope">
                    <StateSelect v-model="scope.row.state" disabled />
                </template>
            </el-table-column>
            <el-table-column label="操作" width="280">
                <template #default="scope">
                    <el-button-group>
                        <el-button 
                            type="primary" 
                            size="small" 
                            @click="handleAddSubNode(scope.row.node_id)"
                        >
                            添加子节点
                        </el-button>
                        <el-button 
                            type="danger" 
                            size="small" 
                            @click="handleDelete(scope.row.node_id)"
                        >
                            删除
                        </el-button>
                    </el-button-group>
                </template>
            </el-table-column>
        </el-table>

        <!-- 添加节点弹窗 -->
        <NodeAdd
            ref="nodeAddRef"
            :parent-id="selectedParentId"
            @success="fetchNodes(route.params.nodeId)"
        />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessageBox, ElMessage } from 'element-plus'
import StateSelect from '../components/StateSelect.vue'
import NodeAdd from './NodeAdd.vue'

const route = useRoute()
const router = useRouter()
const nodes = ref([])
const loading = ref(false)
const currentNode = ref(null)
const nodeAddRef = ref(null)
const selectedParentId = ref(0)

// 获取节点及其子节点数据
const fetchNodes = async (nodeId) => {
    loading.value = true
    try {
        const response = await axios.get(`/api/node/tree/${nodeId}`)
        currentNode.value = response.data
        nodes.value = response.data.children
    } catch (error) {
        console.error('Error fetching nodes:', error)
        ElMessage.error('获取节点数据失败')
    } finally {
        loading.value = false
    }
}

// 删除节点
const handleDelete = async (nodeId) => {
    try {
        await ElMessageBox.confirm('确认要删除该节点及其所有子节点吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
            message: '此操作将永久删除该节点及其所有子节点，是否继续？'
        })

        await axios.delete(`/api/node/delete/${nodeId}`)
        ElMessage.success('删除成功')
        await fetchNodes(route.params.nodeId)
    } catch (error) {
        if (error !== 'cancel') {
            console.error('Error deleting node:', error)
            ElMessage.error('删除节点失败')
        }
    }
}

// 关闭页面
const handleClose = () => {
    router.push('/projects')
}

// 打开添加节点弹窗
const handleAddNode = () => {
    selectedParentId.value = Number(route.params.nodeId)
    nodeAddRef.value.open()
}

// 添加子节点
const handleAddSubNode = (parentId) => {
    selectedParentId.value = parentId
    nodeAddRef.value.open()
}

onMounted(() => {
    if (route.params.nodeId) {
        fetchNodes(route.params.nodeId)
    }
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

.header-buttons {
    display: flex;
    gap: 10px;
}

.current-node {
    margin-bottom: 20px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.node-info {
    line-height: 1.8;
}

.info-row {
    display: flex;
    gap: 40px;
}

.info-col {
    flex: 1;
    /* 每列占据相等空间 */
}

.info-row p {
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.info-row .el-tag {
    margin-left: 4px;
}

.subtitle {
    margin: 20px 0;
    color: #606266;
}

.el-tag {
    min-width: 60px;
    text-align: center;
}
</style>