<template>
    <div class="node-add">
        <h2>添加节点</h2>
        <el-form :model="form" label-width="120px">
            <!-- 根据NodeModel添加表单项 -->

            <el-form-item>
                <el-button type="primary" @click="submitForm">创建节点</el-button>
                <el-button @click="$router.push('/projects')">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
    // 根据NodeModel添加字段
})

const submitForm = async () => {
    try {
        await axios.post('/api/node/create', form.value)
        router.push('/projects')
    } catch (error) {
        console.error('Error creating node:', error)
    }
}
</script>
