<template>
    <div class="add-container">
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
            <el-form-item label="节点名称" prop="node_name">
                <el-input v-model="form.node_name" placeholder="请输入节点名称" />
            </el-form-item>
            <el-form-item label="节点描述" prop="description">
                <el-input v-model="form.description" placeholder="请输入节点描述" />
            </el-form-item>
            <el-form-item label="状态" prop="state">
                <el-select v-model="form.state" placeholder="请选择状态">
                    <el-option label="未开始" :value="0" />
                    <el-option label="正常" :value="1" />
                    <el-option label="警告" :value="2" />
                    <el-option label="错误" :value="3" />
                </el-select>
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
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { createNode } from '../../api/node'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const currentNodeId = ref(Number(route.params.nodeId))

const form = ref({
    node_name: '',
    parent_id: Number(route.query.parent_id) || 0,
    description: '',
    state: 0
})

const rules = {
    node_name: [
        { required: true, message: '请输入节点名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ],
    description: [
        { required: true, message: '请输入节点描述', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ],
    state: [
        { required: true, message: '请选择状态', trigger: 'change' }
    ]
}

const handleSubmit = async () => {
    if (!formRef.value) return

    try {
        await formRef.value.validate()
        loading.value = true

        await createNode(form.value)
        ElMessage.success('创建成功')
        router.push(`/main/node/tree/${currentNodeId.value}`)
    } catch (error: any) {
        ElMessage.error(error.message || '保存失败')
    } finally {
        loading.value = false
    }
}

const handleCancel = () => {
    router.push(`/main/node/tree/${currentNodeId.value}`)
}


</script>

<style scoped>
.add-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}
</style>