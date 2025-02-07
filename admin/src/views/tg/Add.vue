<template>
    <div class="add-container">
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
            <el-form-item label="配置名称" prop="tg_name">
                <el-input v-model="form.tg_name" placeholder="请输入配置名称" />
            </el-form-item>
            <el-form-item label="Bot Token" prop="bot_token">
                <el-input v-model="form.bot_token" placeholder="请输入 Bot Token" />
            </el-form-item>
            <el-form-item label="Chat ID" prop="chat_id">
                <el-input v-model="form.chat_id" placeholder="请输入 Chat ID" />
            </el-form-item>
            <el-form-item label="URL" prop="url">
                <el-input v-model="form.url" placeholder="请输入 URL" />
            </el-form-item>
            <el-form-item label="发送状态码" prop="state_code">
                <el-input v-model="form.state_code" placeholder="请输入发送状态码" />
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
import { createPNTG } from '../../api/pntg'
import { addTgConfigToCache } from '../../utils/tgUtils'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = ref({
    tg_name: '',
    bot_token: '',
    chat_id: '',
    url: '',
    state_code: ''
})

const rules = {
    tg_name: [
        { required: true, message: '请输入配置名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ],
    bot_token: [
        { required: true, message: '请输入 Bot Token', trigger: 'blur' }
    ],
    chat_id: [
        { required: true, message: '请输入 Chat ID', trigger: 'blur' }
    ],
    url: [
        { required: true, message: '请输入 URL', trigger: 'blur' }
    ]
}

const handleSubmit = async () => {
    if (!formRef.value) return

    try {
        await formRef.value.validate()
        loading.value = true

        const response: any = await createPNTG(form.value)
        addTgConfigToCache(response)
        ElMessage.success('创建成功')
        router.push('/main/tg/management')
    } catch (error: any) {
        ElMessage.error(error.message || '保存失败')
    } finally {
        loading.value = false
    }
}

const handleCancel = () => {
    router.push('/main/tg/management')
}
</script>

<style scoped>
.add-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}
</style>