<template>
    <div class="login-container">
        <el-form ref="loginFormRef" :model="loginForm" class="login-form">
            <h3 class="title">登录</h3>
            <el-form-item prop="username">
                <el-input v-model="loginForm.username" placeholder="用户名" maxlength="20" />
            </el-form-item>
            <el-form-item prop="password">
                <el-input v-model="loginForm.password" type="password" placeholder="密码" />
            </el-form-item>
            <el-form-item prop="captcha" class="captcha-item">
                <el-input v-model="loginForm.captcha" placeholder="验证码" maxlength="4" />
                <div class="captcha-container">
                    <img :src="captchaUrl" @click="refreshCaptcha" alt="验证码" class="captcha-img">
                </div>
            </el-form-item>
            <el-form-item>
                <el-button :loading="loading" type="primary" @click="handleLogin" class="submit-btn">登录</el-button>
                <el-button @click="goToRegister" class="submit-btn">注册账号</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCSRFToken } from '../../api/auth'
import { userStore } from '../../stores/user'
import type { FormInstance } from 'element-plus'
import config from '../../config/index.ts'

const router = useRouter()
const loading = ref(false)
const loginFormRef = ref<FormInstance>()
const captchaUrl = ref('')

const loginForm = reactive({
    username: '',
    password: '',
    captcha: ''
})

const refreshCaptcha = () => {
    captchaUrl.value = `${config.API_URL}/api/captcha/?t=${Date.now()}`
}

const handleLogin = async () => {
    if (!loginFormRef.value) return

    try {
        loading.value = true
        await loginFormRef.value.validate()

        const csrfResponse: any = await getCSRFToken()
        const csrfToken = csrfResponse.csrfToken

        const loginResponse: any = await userStore.login({
            username: loginForm.username,
            password: loginForm.password,
            captcha: loginForm.captcha,
            csrfmiddlewaretoken: csrfToken
        })

        if (loginResponse && loginResponse.id) {
            // 保存用户信息到 localStorage
            localStorage.setItem('Admin-Token', loginResponse.id.toString())
            localStorage.setItem('userInfo', JSON.stringify(loginResponse))

            // 等待下一个 tick 再进行路由跳转
            await router.push((router.currentRoute.value.query.redirect as string) || '/main/projects')
            ElMessage.success('登录成功')
        } else {
            throw new Error('Login failed')
        }
    } catch (error: any) {
        console.error('Login Error:', error)
        ElMessage.error(error.response?.data?.message || '登录失败')
    } finally {
        loading.value = false
    }
}

const goToRegister = () => {
    router.push('/register')
}

onMounted(() => {
    refreshCaptcha()
})
</script>

<style lang="scss" scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f3f3f3;
}

.login-form {
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

.login-form :deep(.el-input__wrapper) {
    box-shadow: 0 0 0 1px #dcdfe6;
    height: 40px;
}

.login-form :deep(.el-input__wrapper.is-focus) {
    box-shadow: 0 0 0 1px #409eff;
}

.login-form :deep(.el-form-item.is-error .el-input__wrapper) {
    box-shadow: 0 0 0 1px #f56c6c;
}

.captcha-item :deep(.el-input__wrapper) {
    padding-right: 120px;
}
</style>