<template>
    <div class="edit-container">
        <el-form ref="formRef" :model="form" :rules="rules" label-width="120px">
            <el-form-item label="节点名称" prop="node_name">
                <el-input v-model="form.node_name" placeholder="请输入节点名称" />
            </el-form-item>
            <el-form-item label="父节点" prop="parent_id">
                <el-select v-model="form.parent_id" placeholder="请选择父节点" clearable>
                    <el-option label="无父节点" :value="0" />
                    <el-option v-for="node in nodeList" :key="node.node_id" :label="node.node_name"
                        :value="node.node_id" :disabled="node.node_id === currentNodeId" />
                </el-select>
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { getNodeById, updateNode, getNodeList } from '../../api/node'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const nodeList = ref([])
const currentNodeId = ref(Number(route.params.nodeId))

const form = ref({
    node_name: '',
    parent_id: 0,
    state: 0,
    project_id: 0
})

const rules = {
    node_name: [
        { required: true, message: '请输入节点名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
    ],
    state: [
        { required: true, message: '请选择状态', trigger: 'change' }
    ]
}

const fetchNode = async () => {
    try {
        const nodeId = Number(route.params.nodeId)
        const response = await getNodeById(nodeId)
        if (response.data) {
            form.value = {
                ...response.data,
                parent_id: response.data.parent_id || 0
            }
            await fetchNodeList()
        }
    } catch (error: any) {
        ElMessage.error('获取节点信息失败')
        console.error('Error fetching node:', error)
    }
}

const fetchNodeList = async () => {
    try {
        const response = await getNodeList(form.value.project_id)
        nodeList.value = response.data || []
    } catch (error: any) {
        ElMessage.error('获取节点列表失败')
        console.error('Error fetching node list:', error)
    }
}

const handleSubmit = async () => {
    if (!formRef.value) return

    try {
        await formRef.value.validate()
        loading.value = true

        await updateNode(currentNodeId.value, form.value)
        ElMessage.success('更新成功')
        router.push(`/main/node/tree/${form.value.project_id}`)
    } catch (error: any) {
        ElMessage.error(error.message || '保存失败')
    } finally {
        loading.value = false
    }
}

const handleCancel = () => {
    router.push(`/main/node/tree/${form.value.project_id}`)
}

onMounted(() => {
    fetchNode()
})
</script>

<style scoped>
.edit-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}
</style>