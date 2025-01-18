<template>
    <div class="edit-container">
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
            <el-form-item label="状态名称" prop="state_name">
                <el-input v-model="form.state_name" placeholder="请输入状态名称" />
            </el-form-item>
            <el-form-item label="状态描述" prop="description">
                <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入状态描述" />
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
import { getStateById, updateState } from '../../api/state'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const currentStateId = ref(Number(route.params.stateId))

const form = ref({
    state_name: '',
    description: ''
})

const rules = {
    state_name: [
        { required: true, message: '请输入状态名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ],
    description: [
        { required: true, message: '请输入状态描述', trigger: 'blur' },
        { max: 500, message: '最多 500 个字符', trigger: 'blur' }
    ]
}

const fetchState = async () => {
    try {
        const stateId = Number(route.params.stateId)
        const data: any = await getStateById(stateId)
        if (data) {
            form.value = {
                ...data,
            }
        }
    } catch (error: any) {
        ElMessage.error('获取状态信息失败')
        console.error('Error fetching state:', error)
    }
}

const handleSubmit = async () => {
    if (!formRef.value) return
    try {
        await formRef.value.validate()
        loading.value = true
        await updateState(currentStateId.value, form.value)
        ElMessage.success('更新成功')
        router.push('/main/state/management')
    } catch (error: any) {
        ElMessage.error(error.message || '保存失败')
    } finally {
        loading.value = false
    }
}

const handleCancel = () => {
    router.push('/main/state/management')
}

onMounted(() => {
    fetchState()
})
</script>

<style scoped>
.edit-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}
</style>