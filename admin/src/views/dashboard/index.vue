<template>
    <el-container class="layout-container">
        <el-container>
            <!-- 顶部导航 -->
            <el-header>
                <div class="header-right">
                    <el-dropdown @command="handleCommand" class="user-dropdown">
                        <span class="el-dropdown-link">
                            <el-avatar :size="32" class="user-avatar">
                                {{ userInfo?.username?.[0]?.toUpperCase() || 'U' }}
                            </el-avatar>
                            <span class="username">{{ userInfo?.username || '用户' }}</span>
                            <el-icon class="el-icon--right"><arrow-down /></el-icon>
                        </span>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </div>
            </el-header>

            <!-- 主要内容区 -->
            <el-main>
                <router-view v-slot="{ Component }">
                    <transition name="fade-transform" mode="out-in">
                        <component :is="Component" />
                    </transition>
                </router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import { userStore } from '../../stores/user'

const router = useRouter()
const userInfo = ref<any>(null)

const handleCommand = async (command: string) => {
    if (command === 'logout') {
        try {
            await userStore.logout()
            router.push('/login')
            ElMessage.success('退出成功')
        } catch (error) {
            ElMessage.error('退出失败')
        }
    }
}

onMounted(async () => {
    try {
        const info = await userStore.getInfo()
        userInfo.value = info
    } catch (error) {
        console.error('Failed to get user info:', error)
    }
})
</script>

<style scoped lang="scss">
.layout-container {
    height: 100vh;

    .el-header {
        background-color: #fff;
        border-bottom: 1px solid #dcdfe6;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
        height: 60px;

        .header-left {
            h2 {
                margin: 0;
                color: #303133;
                font-size: 20px;
            }
        }

        .header-right {
            display: flex;
            align-items: center;

            .user-dropdown {
                .el-dropdown-link {
                    display: flex;
                    align-items: center;
                    cursor: pointer;
                    padding: 0 8px;
                    height: 40px;
                    border-radius: 4px;
                    transition: background-color 0.3s;

                    &:hover {
                        background-color: #f5f7fa;
                    }

                    .user-avatar {
                        background: #409EFF;
                        color: #fff;
                        margin-right: 8px;
                    }

                    .username {
                        color: #303133;
                        margin: 0 8px;
                    }
                }
            }
        }
    }

    .el-main {
        background-color: #f0f2f5;
        padding: 20px;
        overflow-y: auto;
    }
}

// 路由切换动画
.fade-transform-enter-active,
.fade-transform-leave-active {
    transition: all 0.3s;
}

.fade-transform-enter-from {
    opacity: 0;
    transform: translateX(-30px);
}

.fade-transform-leave-to {
    opacity: 0;
    transform: translateX(30px);
}
</style>