<template>
    <div class="login-container">
        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" class="login-form" autocomplete="on"
            label-position="left">
            <div class="title-container">
                <h3 class="title">登录</h3>
            </div>

            <el-form-item prop="username">
                <span class="svg-container">
                    <el-icon>
                        <User />
                    </el-icon>
                </span>
                <el-input v-model="loginForm.username" placeholder="用户名" name="username" type="text" tabindex="1"
                    autocomplete="on" />
            </el-form-item>

            <el-form-item prop="password">
                <span class="svg-container">
                    <el-icon>
                        <Lock />
                    </el-icon>
                </span>
                <el-input v-model="loginForm.password" :type="passwordVisible ? 'text' : 'password'" placeholder="密码"
                    name="password" tabindex="2" autocomplete="on" @keyup.enter="handleLogin">
                    <template #suffix>
                        <el-icon class="show-pwd" @click="passwordVisible = !passwordVisible">
                            <View v-if="passwordVisible" />
                            <Hide v-else />
                        </el-icon>
                    </template>
                </el-input>
            </el-form-item>

            <el-form-item prop="captcha">
                <span class="svg-container">
                    <el-icon>
                        <Key />
                    </el-icon>
                </span>
                <el-input v-model="loginForm.captcha" placeholder="验证码" name="captcha" type="text" tabindex="3"
                    autocomplete="off" style="width: 60%" />
                <div class="captcha-container">
                    <img :src="captchaUrl" @click="refreshCaptcha" alt="captcha" class="captcha-img">
                </div>
            </el-form-item>

            <el-button :loading="loading" type="primary" style="width: 100%; margin-bottom: 30px"
                @click.prevent="handleLogin">
                登录
            </el-button>

            <div class="register-link">
                <router-link to="/register">注册新账号</router-link>
            </div>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, View, Hide, Key } from '@element-plus/icons-vue'
import { getCSRFToken } from '../../api/auth'
import { useUserStore } from '../../stores/user'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const passwordVisible = ref(false)
const loginFormRef = ref<FormInstance>()
const captchaUrl = ref('')

const loginForm = reactive({
    username: '',
    password: '',
    captcha: ''
})

const loginRules = {
    username: [{ required: true, trigger: 'blur', message: '请输入用户名' }],
    password: [{ required: true, trigger: 'blur', message: '请输入密码' }],
    captcha: [{ required: true, trigger: 'blur', message: '请输入验证码' }]
}

const refreshCaptcha = () => {
    captchaUrl.value = `${import.meta.env.VITE_API_URL}/api/captcha/?t=${Date.now()}`
}

const handleLogin = async () => {
    if (!loginFormRef.value) return

    try {
        loading.value = true
        await loginFormRef.value.validate()

        // 获取 CSRF token
        const csrfResponse = await getCSRFToken()
        const csrfToken = csrfResponse.data.csrfToken

        // 获取 store 实例
        const userStore = useUserStore()

        // 添加 CSRF token 到登录数据
        await userStore.login({
            ...loginForm,
            csrfmiddlewaretoken: csrfToken
        })

        // 获取重定向地址
        const redirect = (router.currentRoute.value.query.redirect as string) || '/main/projects'
        router.push(redirect)

        ElMessage.success('登录成功')
    } catch (error: any) {
        ElMessage.error(error.message || '登录失败')
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    refreshCaptcha()
})
</script>

<style lang="scss" scoped>
.login-container {
    min-height: 100vh;
    width: 100%;
    background-color: #2d3a4b;
    overflow: hidden;

    .login-form {
        position: relative;
        width: 520px;
        max-width: 100%;
        padding: 160px 35px 0;
        margin: 0 auto;
        overflow: hidden;
    }

    .title-container {
        position: relative;

        .title {
            font-size: 26px;
            color: #eee;
            margin: 0 auto 40px auto;
            text-align: center;
            font-weight: bold;
        }
    }

    .svg-container {
        padding: 6px 5px 6px 15px;
        color: #889aa4;
        vertical-align: middle;
        display: inline-block;
    }

    .show-pwd {
        cursor: pointer;
        color: #889aa4;
    }

    .captcha-container {
        position: absolute;
        right: 10px;
        top: 0;
        height: 100%;
        display: flex;
        align-items: center;
        cursor: pointer;

        .captcha-img {
            height: 32px;
            border-radius: 4px;
        }
    }

    .register-link {
        text-align: center;
        font-size: 14px;
        color: #fff;
        margin-top: 20px;

        a {
            color: #409eff;
            text-decoration: none;

            &:hover {
                text-decoration: underline;
            }
        }
    }

    :deep(.el-input) {
        display: inline-block;
        height: 47px;
        width: 85%;

        input {
            background: transparent;
            border: 0;
            -webkit-appearance: none;
            border-radius: 0;
            padding: 12px 5px 12px 15px;
            color: #fff;
            height: 47px;
            caret-color: #fff;

            &:-webkit-autofill {
                box-shadow: 0 0 0 1000px #283443 inset !important;
                -webkit-text-fill-color: #fff !important;
            }
        }
    }

    :deep(.el-form-item) {
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        color: #454545;
    }
}
</style>