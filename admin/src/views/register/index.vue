<template>
    <div class="register-container">
        <el-form ref="registerFormRef" :model="registerForm" :rules="rules" class="register-form">
            <h3 class="title">注册</h3>
            <el-form-item prop="username">
                <el-input v-model="registerForm.username" placeholder="用户名" />
            </el-form-item>
            <el-form-item prop="password">
                <el-input v-model="registerForm.password" type="password" placeholder="密码" />
            </el-form-item>
            <el-form-item prop="confirmPassword">
                <el-input v-model="registerForm.confirmPassword" type="password" placeholder="确认密码" />
            </el-form-item>
            <el-form-item prop="captcha" class="captcha-item">
                <el-input v-model="registerForm.captcha" placeholder="验证码" maxlength="4" />
                <div class="captcha-container">
                    <img :src="captchaUrl" @click="refreshCaptcha" alt="验证码" class="captcha-img">
                </div>
            </el-form-item>
            <el-form-item>
                <el-button :loading="loading" type="primary" @click="handleRegister" class="submit-btn">注册</el-button>
                <el-button @click="goToLogin" class="submit-btn">返回登录</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { register } from '../../api/auth'
import config from '../../config/index.ts'

const router = useRouter()
const loading = ref(false)
const registerFormRef = ref<FormInstance>()

const registerForm = ref({
    username: '',
    password: '',
    confirmPassword: '',
    captcha: ''
})

const captchaUrl = ref('/api/captcha/' + '?t=' + Date.now())

const rules = {
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, message: '用户名长度至少为3个字符', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
    ],
    confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        {
            validator: (_rule: any, value: string, callback: Function) => {
                if (value !== registerForm.value.password) {
                    callback(new Error('两次输入的密码不一致'))
                } else {
                    callback()
                }
            },
            trigger: 'blur'
        }
    ],
    captcha: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

const handleRegister = async () => {
    if (!registerFormRef.value) return

    try {
        await registerFormRef.value.validate()
        loading.value = true

        const response: any = await register({
            username: registerForm.value.username,
            password: registerForm.value.password,
            captcha: registerForm.value.captcha
        })
        
        if (response.message) {
            ElMessage.success(response.message)
        } else {
            ElMessage.success('注册成功')
        }
        router.push('/login')
    } catch (error: any) {
        const errorMsg = error.response?.error || error.message || '注册失败'
        ElMessage.error(errorMsg)
        if (errorMsg.includes('验证码')) {
            refreshCaptcha()
        }
    } finally {
        loading.value = false
    }
}

const refreshCaptcha = () => {
    const timestamp = Date.now()
    captchaUrl.value = `${config.API_URL}/api/captcha/?t=${timestamp}`
}

const goToLogin = () => {
    router.push('/login')
}

onMounted(() => {
    refreshCaptcha()
})
</script>

<style scoped>
.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f3f3f3;
}

.register-form {
    width: 400px;
    padding: 30px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title {
    text-align: center;
    margin-bottom: 30px;
}

.submit-btn {
    width: 100%;
    margin-top: 10px;
}

.captcha-item {
    position: relative;
}

.captcha-container {
    position: absolute;
    right: 1px;
    top: 1px;
    height: 38px;
    cursor: pointer;
    background: #fff;
    border-radius: 0 4px 4px 0;
    border-left: 1px solid #dcdfe6;
    padding: 0 15px;
    display: flex;
    align-items: center;
    transition: all 0.3s;
}

.captcha-container:hover {
    background-color: #f5f7fa;
}

.captcha-img {
    height: 34px;
    cursor: pointer;
}

.register-form :deep(.el-input__wrapper) {
    box-shadow: 0 0 0 1px #dcdfe6;
    height: 40px;
}

.register-form :deep(.el-input__wrapper.is-focus) {
    box-shadow: 0 0 0 1px #409eff;
}

.register-form :deep(.el-form-item.is-error .el-input__wrapper) {
    box-shadow: 0 0 0 1px #f56c6c;
}

.captcha-item :deep(.el-input__wrapper) {
    padding-right: 120px;
}
</style>