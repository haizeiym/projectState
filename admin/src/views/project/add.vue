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
import StateSelect from '../../components/StateSelect.vue'
import { createProject } from '../../api/project'
import { createPNTG } from '../../api/pntg'
import { createNode } from '../../api/node'
import { updateUserProjects } from '../../api/auth'
import { userStore } from '../../stores/user'
import { getStateCache, getStateType } from '../../utils/stateUtils'

const router = useRouter()
const form = ref({
    project_name: '',
    description: '',
    state: 0,
    bot_token: '',
    chat_id: '',
    url: ''
})

const stateOptions = ref({})
const selectedStateCodes = ref([])

const handleSubmit = async () => {
    try {

        // 创建节点
        const nodeResponse = await createNode({
            node_name: form.value.project_name,
            description: form.value.description,
            state: form.value.state
        })

        // 创建项目
        const projectResponse = await createProject({
            node_id: nodeResponse.node_id,
            project_name: form.value.project_name,
            description: form.value.description,
            state: form.value.state
        })

        // 创建 PNTG 配置
        await createPNTG({
            project_id: projectResponse.project_id,
            bot_token: form.value.bot_token,
            chat_id: form.value.chat_id,
            url: form.value.url
        })

        // 更新用户的 project_ids
        if (userStore.userInfo.value) {
            const projectIds = userStore.userInfo.value.projectIds || []
            projectIds.push(projectResponse.project_id)
            // 更新后端数据库
            await updateUserProjects(userStore.userInfo.value.id, projectIds)
            userStore.updateUserInfo({
                ...userStore.userInfo.value,
                projectIds
            })
        }

        ElMessage.success('项目创建成功')
        router.push('/main/projects')
    } catch (error) {
        ElMessage.error('项目创建失败：' + (error.response?.data?.message || error.message))
    }
}

const handleCancel = () => {
    router.push('/main/projects')
}

onMounted(async () => {
    stateOptions.value = await getStateCache()
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
