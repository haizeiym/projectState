<template>
    <el-dialog v-model="dialogVisible" title="添加节点" width="500px">
        <el-form :model="form" label-width="120px">
            <el-form-item label="节点名称">
                <el-input v-model="form.node_name" />
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.description" type="textarea" />
            </el-form-item>
            <el-form-item label="状态">
                <StateSelect v-model="form.state" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="handleCancel">取消</el-button>
                <el-button type="primary" @click="handleSubmit">创建</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import StateSelect from '../components/StateSelect.vue'
import { createNode } from '../api/node'

const props = defineProps({
    parentId: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['node-added'])
const dialogVisible = ref(false)
const form = ref({
    node_name: '',
    description: '',
    state: 0,
    parent_id: props.parentId
})

const handleSubmit = async () => {
    try {
        await createNode(form.value)
        ElMessage.success('创建成功')
        dialogVisible.value = false
        emit('node-added')
        form.value = {
            node_name: '',
            description: '',
            state: 0,
            parent_id: props.parentId
        }
    } catch (error) {
        ElMessage.error('创建失败：' + (error.response?.data?.message || error.message))
    }
}

// 取消
const handleCancel = () => {
    dialogVisible.value = false
}

// 对外暴露打开弹窗的方法
const open = () => {
    dialogVisible.value = true
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
