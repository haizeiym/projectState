<template>
    <el-dialog v-model="dialogVisible" title="修改节点" width="500px">
        <el-form :model="form" label-width="120px">
            <el-form-item label="节点名称">
                <el-input v-model="form.node_name" />
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.description" type="textarea" />
            </el-form-item>
            <el-form-item label="状态">
                <StateTag v-model="form.state" editable @change="handleStateChange" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="handleCancel">取消</el-button>
                <el-button type="primary" @click="handleSubmit">保存</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import StateTag from '../components/StateTag.vue'
import { getNodeById, updateNode } from '../api/node'

const props = defineProps({
    nodeId: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['node-updated'])
const dialogVisible = ref(false)
const form = ref({
    node_name: '',
    description: '',
    state: 0
})

const open = async () => {
    try {
        const response = await getNodeById(props.nodeId)
        form.value = response
        dialogVisible.value = true
    } catch (error) {
        ElMessage.error('获取节点信息失败：' + (error.response?.data?.message || error.message))
    }
}

const handleSubmit = async () => {
    try {
        await updateNode(props.nodeId, form.value)
        ElMessage.success('更新成功')
        dialogVisible.value = false
        emit('node-updated')
    } catch (error) {
        ElMessage.error('更新失败：' + (error.response?.data?.message || error.message))
    }
}

// 处理状态变化
const handleStateChange = async (newState) => {
    try {
        // 获取所有子节点ID
        const response = await axios.get(`/api/node/tree/${props.nodeId}`)

        // 收集所有子节点ID
        const collectNodeIds = (node, ids = []) => {
            if (node.children && node.children.length > 0) {
                node.children.forEach(child => {
                    ids.push(child.node_id)
                    collectNodeIds(child, ids)
                })
            }
            return ids
        }

        const nodeIds = collectNodeIds(response.data)

        // 批量更新所有子节点状态
        if (nodeIds.length > 0) {
            await axios.post('/api/node/batch_update', {
                node_ids: nodeIds,
                state: newState
            })
        }
    } catch (error) {
        ElMessage.error('更新子节点状态失败：' + (error.response?.data?.message || error.message))
    }
}

// 取消
const handleCancel = () => {
    dialogVisible.value = false
    // 重置表单
    form.value = {
        node_name: '',
        description: '',
        state: 0
    }
}

defineExpose({
    open
})
</script>

<style scoped>
.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
</style>