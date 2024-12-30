<template>
    <div class="node-tree">
        <h2>节点树形展示</h2>
        <el-table v-loading="loading" :data="nodes" row-key="node_id" style="width: 100%; margin-top: 20px;">
            <el-table-column prop="node_id" label="节点ID" width="180" />
            <el-table-column prop="node_name" label="节点名称" width="180" />
            <el-table-column prop="description" label="描述" width="180" />
            <el-table-column prop="state" label="状态" width="180" />
            <el-table-column label="操作" width="180">
                <template #default="scope">
                    <el-button type="primary" size="small" @click="handleExpand(scope.row.node_id)">
                        展开
                    </el-button>
                    <el-button type="danger" size="small" @click="handleDelete(scope.row.node_id)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const nodes = ref([])
const loading = ref(false)

// 获取节点及其子节点数据
const fetchNodes = async (nodeId) => {
    loading.value = true
    try {
        const response = await axios.get(`/api/node/tree/${nodeId}`)
        nodes.value = response.data
    } catch (error) {
        console.error('Error fetching nodes:', error)
    } finally {
        loading.value = false
    }
}

// 展开节点
const handleExpand = (nodeId) => {
    router.push(`/node/${nodeId}`)
}

// 删除节点
const handleDelete = async (nodeId) => {
    try {
        await axios.delete(`http://localhost:8000/api/node/delete/${nodeId}`)
        await fetchNodes(route.params.nodeId)
    } catch (error) {
        console.error('Error deleting node:', error)
    }
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
</style>