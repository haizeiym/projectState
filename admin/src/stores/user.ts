import { login, logout, getInfo } from '../api/auth';
import { ref } from 'vue';

// 创建用户状态管理
const token = ref(localStorage.getItem('Admin-Token') || '');
const userInfo = ref<{
    id: number | null;
    username: string;
    projectIds: number[];
    isSuper: boolean;
} | null>(null);

export const useUser = () => {
    async function loginAction(userInfo: any) {
        try {
            const response: any = await login(userInfo);
            if (response && response.id) {
                token.value = response.id.toString();
                localStorage.setItem('Admin-Token', token.value);
                
                // 保存用户信息，包括项目ID列表
                const userData = {
                    id: response.id,
                    username: response.username,
                    projectIds: response.project_ids ? response.project_ids.split(',').map(Number) : [],
                    isSuper: response.is_superuser
                };
                localStorage.setItem('userInfo', JSON.stringify(userData));
                return response;
            }
            throw new Error('Login failed');
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async function getInfoAction() {
        try {
            const response:any = await getInfo();
            userInfo.value = {
                id: response.id,
                username: response.username,
                projectIds: response.project_ids ? response.project_ids.split(',').map(Number) : [],
                isSuper: response.is_superuser
            };
            return response;
        } catch (error) {
            console.error('GetInfo error:', error);
            throw error;
        }
    }

    async function logoutAction() {
        try {
            await logout();
            token.value = '';
            userInfo.value = null;
            localStorage.removeItem('Admin-Token');
            localStorage.removeItem('userInfo');
        } catch (error) {
            console.error('Logout error:', error);
            throw error;
        }
    }

    function hasProjectAccess(projectId: number): boolean {
        return userInfo.value?.isSuper || userInfo.value?.projectIds.includes(projectId) || false;
    }

    return {
        token,
        userInfo,
        login: loginAction,
        getInfo: getInfoAction,
        logout: logoutAction,
        hasProjectAccess
    };
};

// 导出一个全局实例
export const userStore = useUser(); 