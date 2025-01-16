<template>
    <PageLayout title="添加状态">
        <el-form :model="stateForm" ref="stateFormRef" label-width="80px">
            <el-form-item label="状态码" prop="state_code"
                :rules="[{ required: true, message: '请输入状态码', trigger: 'blur' }]">
                <el-input v-model="stateForm.state_code" type="number" />
            </el-form-item>
            <el-form-item label="状态名称" prop="state_name"
                :rules="[{ required: true, message: '请输入状态名称', trigger: 'blur' }]">
                <el-input v-model="stateForm.state_name" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="createState">创建</el-button>
                <el-button @click="cancel">取消</el-button>
            </el-form-item>
        </el-form>
    </PageLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { addState } from '../utils/stateUtils'
import PageLayout from '../components/PageLayout.vue'
import { ElMessage } from 'element-plus'

const stateForm = ref({
    state_code: '',
    state_name: ''
})

const stateFormRef = ref(null)
const router = useRouter()

const createState = async () => {
    try {
        await stateFormRef.value.validate()
        const response = await addState(stateForm.value)
        if (response.status === 201) {
            ElMessage.success('状态创建成功')
            router.push('/state-management')
        }
    } catch (error) {
        if (error.response?.status === 500) {
            ElMessage.error('状态码已存在')
        } else {
            ElMessage.error('状态创建失败：' + (error.response?.data?.message || error.message))
        }
    }
}

const cancel = () => {
    router.push('/state-management')
}
</script>

<style scoped>
/* 添加样式 */
</style>