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
                <StateSelect v-model="form.state" :disabled="hasParent" @change="handleStateChange" />
                <div v-if="hasParent" class="state-info">
                    <el-alert type="info" :closable="false" show-icon>
                        该节点有父节点，状态由父节点统一管理
                    </el-alert>
                </div>
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
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import StateSelect from '../components/StateSelect.vue'

const props = defineProps({
    nodeId: {
        type: Number,
        required: true,
        validator: (value) => {
            return value > 0 || value === null
        }
    }
})

const emit = defineEmits(['success'])

const dialogVisible = ref(false)
const form = ref({
    node_name: '',
    description: '',
    state: 0,
    parent_id: 0
})

const hasParent = computed(() => form.value.parent_id > 0)

// 获取节点信息
const fetchNode = async () => {
    try {
        const response = await axios.get(`/api/node/get/${props.nodeId}`)
        form.value = response.data
    } catch (error) {
        ElMessage.error('获取节点信息失败：' + (error.response?.data?.message || error.message))
        dialogVisible.value = false
    }
}

// 更新父节点状态
const updateParentState = async () => {
    if (form.value.parent_id) {
        try {
            await axios.post(`/api/node/update/${form.value.parent_id}`, {
                children_state: form.value.state
            })
        } catch (error) {
            console.error('更新父节点状态失败:', error)
        }
    }
}

// 处理状态变化
const handleStateChange = async (newState) => {
    try {
        // 更新所有子节点的状态
        const response = await axios.get(`/api/node/tree/${props.nodeId}`)
        const updateChildrenState = async (node) => {
            if (node.children && node.children.length > 0) {
                for (const child of node.children) {
                    await axios.post(`/api/node/update/${child.node_id}`, {
                        state: newState
                    })
                    await updateChildrenState(child)
                }
            }
        }
        await updateChildrenState(response.data)
    } catch (error) {
        ElMessage.error('更新子节点状态失败：' + (error.response?.data?.message || error.message))
    }
}

// 提交表单
const handleSubmit = async () => {
    try {
        await axios.post(`/api/node/update/${props.nodeId}`, form.value)
        await updateParentState()
        ElMessage.success('修改成功')
        dialogVisible.value = false
        emit('success')
    } catch (error) {
        ElMessage.error('修改失败：' + (error.response?.data?.message || error.message))
    }
}

// 取消
const handleCancel = () => {
    dialogVisible.value = false
}

// 对外暴露打开弹窗的方法
const open = async () => {
    console.log('open', props.nodeId)
    if (!props.nodeId || props.nodeId <= 0) {
        ElMessage.error('节点ID不能为空')
        return
    }
    dialogVisible.value = true
    await fetchNode()
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

.state-info {
    margin-top: 8px;
}

:deep(.el-alert) {
    padding: 8px 16px;
}
</style>