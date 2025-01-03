<template>
    <div class="project-add">
        <h2>添加项目</h2>
        <div class="description-text">
            <el-alert title="默认添加节点，名称，描述，状态相同" type="info" :closable="false" class="mb-20" />
        </div>
        <el-form :model="form" label-width="120px">
            <el-form-item label="项目名称">
                <el-input v-model="form.project_name" />
            </el-form-item>
            <el-form-item label="描述">
                <el-input v-model="form.description" type="textarea" />
            </el-form-item>
            <el-form-item label="状态">
                <StateSelect v-model="form.state" />
            </el-form-item>
            <!-- PNTGModel Fields -->
            <el-form-item label="Bot Token">
                <el-input v-model="form.bot_token" />
            </el-form-item>
            <el-form-item label="Chat ID">
                <el-input v-model="form.chat_id" />
            </el-form-item>
            <el-form-item label="URL">
                <el-input v-model="form.url" />
            </el-form-item>
            <el-form-item label="发送消息状态码">
                <el-select v-model="selectedStateCodes" multiple placeholder="选择状态码">
                    <el-option v-for="value in Object.keys(stateOptions)" :key="value" :label="stateOptions[value]"
                        :value="Number(value)">
                        <el-tag :type="getStateType(Number(value))">{{ stateOptions[value] }}</el-tag>
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="handleSubmit">创建</el-button>
                <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import StateSelect from '../components/StateSelect.vue'
import { getStateCache, getStateType } from '../utils/stateUtils'

const router = useRouter()
const form = ref({
    project_name: '',
    description: '',
    state: 0,
    node_id: '',
    bot_token: '',
    chat_id: '',
    url: '',
    state_codes: ''
})

const selectedStateCodes = ref([])
const stateOptions = ref({})

// 创建节点
const createNode = async () => {
    try {
        const response = await axios.post('/api/node/create', {
            node_name: form.value.project_name,
            description: form.value.description,
            state: form.value.state
        })
        if (response.data && response.data.node_id) {
            return response.data.node_id
        }
        throw new Error('创建节点失败：未获取到节点ID')
    } catch (error) {
        throw new Error('创建节点失败：' + (error.response?.data?.message || error.message))
    }
}

// 提交表单
const handleSubmit = async () => {
    try {
        // Update form.state_codes with selectedStateCodes
        form.value.state_codes = selectedStateCodes.value.join(',')

        // 先创建节点
        const nodeId = await createNode()

        // 设置节点ID并创建项目
        form.value.node_id = nodeId
        const projectResponse = await axios.post('/api/project/create', form.value)

        if (projectResponse.data && projectResponse.data.project_id) {
            // 使用创建成功后的 project_id 创建 PNTG 记录
            await axios.post('/api/pntg/create', {
                project_id: projectResponse.data.project_id,
                bot_token: form.value.bot_token,
                chat_id: form.value.chat_id,
                url: form.value.url,
                state_codes: form.value.state_codes
            })
        }

        ElMessage.success('创建成功')
        router.push('/projects')
    } catch (error) {
        ElMessage.error(error.message)
        // 如果项目创建失败，可以考虑删除已创建的节点
        if (form.value.node_id) {
            try {
                await axios.delete(`/api/node/delete/${form.value.node_id}`)
            } catch (e) {
                console.error('清理节点失败:', e)
            }
        }
    }
}

// 取消
const handleCancel = () => {
    router.push('/projects')
}

// Fetch state options on component mount
onMounted(async () => {
    stateOptions.value = await getStateCache()
    // Set default state to the first available state code
    const firstStateCode = Object.keys(stateOptions.value)[0]
    if (firstStateCode) {
        form.value.state = Number(firstStateCode)
    }
})
</script>

<style scoped>
.project-add {
    padding: 20px;
}

.description-text {
    margin-bottom: 20px;
}

.mb-20 {
    margin-bottom: 20px;
}
</style>
