<template>
    <div class="add-container">
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
            <el-form-item label="状态代码" prop="state_code">
                <el-input v-model="form.state_code" placeholder="请输入状态代码" />
            </el-form-item>
            <el-form-item label="状态名称" prop="state_name">
                <el-input v-model="form.state_name" placeholder="请输入状态名称" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="handleSubmit" :loading="loading">保存</el-button>
                <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { addState } from '../../utils/stateUtils'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref({
    state_name: '',
    state_code: 0
})

const rules = {
    state_code: [
        { required: true, message: '请输入状态代码', trigger: 'blur' },
        { max: 10, message: '最多 10 个字符', trigger: 'blur' }
    ],
    state_name: [
        { required: true, message: '请输入状态名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ]
}

const handleSubmit = async () => {
    if (!formRef.value) return

    try {
        await formRef.value.validate()
        loading.value = true
        await addState(form.value)
        ElMessage.success('创建成功')
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
</script>

<style scoped>
.add-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}
</style>