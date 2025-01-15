<template>
    <div class="register-container">
        <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" class="register-form"
            autocomplete="on" label-position="left">
            <!-- ... 其他表单项保持不变 ... -->

            <el-form-item prop="captcha">
                <span class="svg-container">
                    <el-icon>
                        <Key />
                    </el-icon>
                </span>
                <el-input v-model="registerForm.captcha" placeholder="Captcha" name="captcha" type="text" tabindex="5"
                    autocomplete="off" style="width: 60%" />
                <div class="captcha-container">
                    <img :src="captchaUrl" @click="refreshCaptcha" alt="captcha" class="captcha-img">
                </div>
            </el-form-item>

            <!-- ... 其他内容保持不变 ... -->
        </el-form>
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue'
import { Key } from '@element-plus/icons-vue'

// ... 其他代码保持不变 ...

const registerForm = reactive({
    username: '',
    password: '',
    email: '',
    project_id: '',
    captcha: ''
})

const registerRules = {
    username: [{ required: true, trigger: 'blur', message: 'Please enter username' }],
    password: [{ required: true, trigger: 'blur', message: 'Please enter password' }],
    project_id: [{ required: true, trigger: 'blur', message: 'Please enter project ID' }],
    captcha: [{ required: true, trigger: 'blur', message: 'Please enter captcha' }]
}

const captchaUrl = ref('')

const refreshCaptcha = () => {
    captchaUrl.value = `${import.meta.env.VITE_API_URL}/api/captcha/?t=${Date.now()}`
}

onMounted(() => {
    refreshCaptcha()
})

// ... 其他代码保持不变 ...
</script>

<style lang="scss" scoped>
// ... 其他样式保持不变 ...

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
</style>