<template>
    <div class="edit-container">
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
            <el-form-item label="节点名称" prop="node_name">
                <el-input v-model="form.node_name" placeholder="请输入节点名称" />
            </el-form-item>
            <el-form-item label="节点描述" prop="description">
                <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入节点描述" />
            </el-form-item>
            <el-form-item label="状态" prop="state">
                <el-select v-model="form.state" placeholder="请选择状态" @change="handleStateChange">
                    <el-option label="未开始" :value="0" />
                    <el-option label="正常" :value="1" />
                    <el-option label="警告" :value="2" />
                    <el-option label="错误" :value="3" />
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="handleSubmit" :loading="loading">保存</el-button>
                <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { getNodeById, getNodeTree, updateNode, batchUpdateNode } from '../../api/node'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const currentNodeId = ref(Number(route.params.nodeId))
const parentId = ref(Number(route.query.parent_id))

const form = ref({
    node_name: '',
    description: '',
    state: 0,
    parent_id: 0
})

const rules = {
    node_name: [
        { required: true, message: '请输入节点名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ],
}

const fetchNode = async () => {
    try {
        const data: any = await getNodeById(currentNodeId.value)
        if (data) {
            form.value = {
                ...data,
            }
        }
    } catch (error: any) {
        ElMessage.error('获取节点信息失败')
        console.error('Error fetching node:', error)
    }
}

const handleSubmit = async () => {
    if (!formRef.value) return
    try {
        await formRef.value.validate()
        loading.value = true
        await updateNode(currentNodeId.value, form.value)
        ElMessage.success('更新成功')
        router.push(`/main/node/tree/${parentId.value}`)
    } catch (error: any) {
        ElMessage.error(error.message || '保存失败')
    } finally {
        loading.value = false
    }
}

const handleStateChange = async (newState: any) => {
    try {
        const nodeTree = await getNodeTree(currentNodeId.value)
        const collectNodeIds = (node: any, ids: any = [currentNodeId.value]) => {
            if (node.children && node.children.length > 0) {
                node.children.forEach((child: any) => {
                    ids.push(child.node_id)
                    collectNodeIds(child, ids)
                })
            }
            return ids
        }
        const nodeIds = collectNodeIds(nodeTree)
        await batchUpdateNode({
            node_ids: nodeIds,
            state: newState
        })
        ElMessage.success('状态更新成功')
        router.push(`/main/node/tree/${parentId.value}`)
    } catch (error: any) {
        ElMessage.error('更新子节点状态失败：' + (error.response?.data?.message || error.message))
    }
}

const handleCancel = () => {
    router.push(`/main/node/tree/${parentId.value}`)
}

onMounted(() => {
    fetchNode()
})
</script>

<style scoped>
.edit-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}
</style>