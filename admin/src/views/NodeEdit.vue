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


const emit = defineEmits(['success'])

const dialogVisible = ref(false)
const form = ref({
    node_id: 0,
    node_name: '',
    description: '',
    state: 0
})

// 获取节点信息
const fetchNode = async () => {
    try {
        const response = await axios.get(`/api/node/get/${form.value.node_id}`)
        form.value = {
            node_id: form.value.node_id,
            node_name: response.data.node_name,
            description: response.data.description,
            state: response.data.state
        }
    } catch (error) {
        ElMessage.error('获取节点信息失败：' + (error.response?.data?.message || error.message))
        dialogVisible.value = false
    }
}

// 处理状态变化
const handleStateChange = async (newState) => {
    try {
        // 获取所有子节点ID
        const response = await axios.get(`/api/node/tree/${form.value.node_id}`)

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

// 提交表单
const handleSubmit = async () => {
    try {
        await axios.post(`/api/node/update/${form.value.node_id}`, form.value)
        ElMessage.success('修改成功')
        dialogVisible.value = false
        emit('success')
        // 重置表单
        form.value = {
            node_id: 0,
            node_name: '',
            description: '',
            state: 0
        }
    } catch (error) {
        ElMessage.error('修改失败：' + (error.response?.data?.message || error.message))
    }
}

// 取消
const handleCancel = () => {
    dialogVisible.value = false
    // 重置表单
    form.value = {
        node_id: 0,
        node_name: '',
        description: '',
        state: 0
    }
}

// 对外暴露打开弹窗的方法
const open = (nodeId) => {
    if (!nodeId || nodeId <= 0) {
        ElMessage.error('节点ID不能为空')
        return
    }
    form.value.node_id = nodeId
    dialogVisible.value = true
    fetchNode()
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