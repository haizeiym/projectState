<template>
    <el-dialog :visible.sync="visible" title="编辑状态" width="30%">
        <el-form :model="stateForm" ref="stateFormRef" label-width="80px">
            <el-form-item label="状态码">
                <el-input v-model="stateForm.state_code" type="number" disabled />
            </el-form-item>
            <el-form-item label="状态名称" prop="state_name" :rules="[{ required: true, message: '请输入状态名称', trigger: 'blur' }]">
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
import { ref, watch } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const props = defineProps({
    visible: Boolean,
    stateCode: Number
})

const emit = defineEmits(['update:visible', 'state-updated'])

const stateForm = ref({
    state_code: props.stateCode,
    state_name: ''
})

const stateFormRef = ref(null)

watch(() => props.stateCode, async (newCode) => {
    if (newCode) {
        try {
            const response = await axios.get(`/api/statecode/get/${newCode}`)
            stateForm.value = response.data
        } catch (error) {
            ElMessage.error('获取状态信息失败：' + (error.response?.data?.message || error.message))
        }
    }
})

const updateState = async () => {
    try {
        await stateFormRef.value.validate()
        const response = await axios.post(`/api/statecode/update/${stateForm.value.state_code}`, stateForm.value)
        if (response.status === 200) {
            ElMessage.success('状态更新成功')
            emit('state-updated')
            emit('update:visible', false)
        }
    } catch (error) {
        ElMessage.error('状态更新失败：' + (error.response?.data?.message || error.message))
    }
}

const cancel = () => {
    emit('update:visible', false)
}
</script>

<style scoped>
.dialog-footer {
    text-align: right;
}
</style> 