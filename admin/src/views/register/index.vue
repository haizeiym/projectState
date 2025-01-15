<template>
    <div class="register-container">
        <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" class="register-form"
            autocomplete="on" label-position="left">
            <div class="title-container">
                <h3 class="title">注册新账号</h3>
            </div>

            <el-form-item prop="username">
                <span class="svg-container">
                    <el-icon>
                        <User />
                    </el-icon>
                </span>
                <el-input v-model="registerForm.username" placeholder="用户名" name="username" type="text" tabindex="1"
                    autocomplete="on" class="custom-input" />
            </el-form-item>

            <el-form-item prop="password">
                <span class="svg-container">
                    <el-icon>
                        <Lock />
                    </el-icon>
                </span>
                <el-input v-model="registerForm.password" :type="passwordVisible ? 'text' : 'password'" placeholder="密码"
                    name="password" tabindex="2" autocomplete="on" class="custom-input">
                    <template #suffix>
                        <el-icon class="show-pwd" @click="passwordVisible = !passwordVisible">
                            <View v-if="passwordVisible" />
                            <Hide v-else />
                        </el-icon>
                    </template>
                </el-input>
            </el-form-item>

            <el-form-item prop="email">
                <span class="svg-container">
                    <el-icon>
                        <Message />
                    </el-icon>
                </span>
                <el-input v-model="registerForm.email" placeholder="邮箱（选填）" name="email" type="email" tabindex="3"
                    autocomplete="on" class="custom-input" />
            </el-form-item>

            <el-form-item prop="project_id">
                <span class="svg-container">
                    <el-icon>
                        <Folder />
                    </el-icon>
                </span>
                <el-input v-model.number="registerForm.project_id" placeholder="项目ID" name="project_id" type="number"
                    tabindex="4" autocomplete="on" class="custom-input" />
            </el-form-item>

            <el-form-item prop="captcha">
                <span class="svg-container">
                    <el-icon>
                        <Key />
                    </el-icon>
                </span>
                <el-input v-model="registerForm.captcha" placeholder="验证码" name="captcha" type="text" tabindex="5"
                    autocomplete="off" class="custom-input" style="width: 60%" />
                <div class="captcha-container">
                    <img :src="captchaUrl" @click="refreshCaptcha" alt="captcha" class="captcha-img">
                </div>
            </el-form-item>

            <el-button :loading="loading" type="primary" style="width: 100%; margin-bottom: 30px; height: 47px;"
                @click.prevent="handleRegister">
                注册
            </el-button>

            <div class="login-link">
                <router-link to="/login">返回登录</router-link>
            </div>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Folder, View, Hide, Key } from '@element-plus/icons-vue'
import { register } from '../../api/auth'
import type { FormInstance } from 'element-plus'
import config from '../../config'

const router = useRouter()
const loading = ref(false)
const passwordVisible = ref(false)
const registerFormRef = ref<FormInstance>()
const captchaUrl = ref('')

const registerForm = reactive({
    username: '',
    password: '',
    email: '',
    project_id: '',
    captcha: ''
})

const registerRules = {
    username: [{ required: true, trigger: 'blur', message: '请输入用户名' }],
    password: [{ required: true, trigger: 'blur', message: '请输入密码' }],
    project_id: [{ required: true, trigger: 'blur', message: '请输入项目ID' }],
    captcha: [{ required: true, trigger: 'blur', message: '请输入验证码' }]
}

const refreshCaptcha = () => {
    captchaUrl.value = `${config.API_URL}/api/captcha/?t=${Date.now()}`
}

const handleRegister = async () => {
    if (!registerFormRef.value) return

    try {
        loading.value = true
        console.log(registerForm)
        await registerFormRef.value.validate()
        await register(registerForm)
        ElMessage.success('注册成功')
        router.push('/login')
    } catch (error: any) {
        ElMessage.error(error.message || '注册失败')
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    refreshCaptcha()
})
</script>

<style lang="scss" scoped>
.register-container {
    min-height: 100vh;
    width: 100%;
    background-color: #f0f2f5;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;

    .register-form {
        width: 520px;
        max-width: 100%;
        padding: 35px;
        margin: 0 auto;
        background: #ffffff;
        border-radius: 4px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    }

    .title-container {
        .title {
            font-size: 26px;
            color: #333;
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
        width: 30px;
        text-align: center;
    }

    .show-pwd {
        cursor: pointer;
        color: #889aa4;
    }

    .captcha-container {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        cursor: pointer;
        padding: 2px;
        border: 1px solid #dcdfe6;
        border-radius: 4px;
        transition: all 0.3s;

        &:hover {
            border-color: #409eff;
            transform: translateY(-50%) scale(1.05);
        }

        .captcha-img {
            height: 38px;
            width: 100px;
            border-radius: 2px;
            display: block;
        }
    }

    .login-link {
        text-align: center;
        font-size: 14px;
        color: #606266;
        margin-top: 20px;

        a {
            color: #409eff;
            text-decoration: none;

            &:hover {
                text-decoration: underline;
            }
        }
    }

    :deep(.custom-input) {
        .el-input__wrapper {
            padding: 0;
            box-shadow: none !important;
            background-color: transparent;
        }

        input {
            height: 47px;
            color: #333;
            padding-left: 10px;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            background-color: #fff;

            &:focus {
                border-color: #409eff;
            }
        }
    }

    :deep(.el-form-item) {
        border: none;
        background: transparent;
        margin-bottom: 20px;

        .el-form-item__error {
            padding-top: 4px;
        }
    }
}
</style>