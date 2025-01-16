<template>
    <el-dialog v-model="dialogVisible" title="编辑状态" width="30%">
        <el-form :model="stateForm" ref="stateFormRef" label-width="80px">
            <el-form-item label="状态码">
                <el-input v-model="stateForm.state_code" type="number" disabled />
            </el-form-item>
            <el-form-item label="状态名称" prop="state_name"
                :rules="[{ required: true, message: '请输入状态名称', trigger: 'blur' }]">
                <el-input v-model="stateForm.state_name" />
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="cancel">取消</el-button>
            <el-button type="primary" @click="updateState">保存</el-button>
        </div>
    </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getStateById, updateState } from '../api/state'

const dialogVisible = ref(false)
const stateForm = ref({
    state_code: '',
    state_name: ''
})

const emit = defineEmits(['state-updated'])
const stateFormRef = ref(null)

const open = async (stateCode) => {
    try {
        const response = await getStateById(stateCode)
        stateForm.value = response
        dialogVisible.value = true
    } catch (error) {
        ElMessage.error('获取状态信息失败：' + (error.response?.data?.message || error.message))
    }
}

defineExpose({
    open
})

const handleUpdateState = async () => {
    try {
        await stateFormRef.value.validate()
        await updateState(stateForm.value.state_code, stateForm.value)
        ElMessage.success('状态更新成功')
        dialogVisible.value = false
        emit('state-updated')
    } catch (error) {
        ElMessage.error('状态更新失败：' + (error.response?.data?.message || error.message))
    }
}

const cancel = () => {
    dialogVisible.value = false
}
</script>

<style scoped>
.dialog-footer {
    text-align: right;
}
</style>