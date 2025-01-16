<template>
    <el-select :model-value="modelValue" placeholder="请选择状态" clearable :loading="loading"
        @update:model-value="handleChange">
        <el-option v-for="option in stateOptions" :key="option.value" :value="option.value" :label="option.label">
            <el-tag :type="getTagType(option.value)" size="small">{{ option.label }}</el-tag>
        </el-option>
    </el-select>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getStateCache, getStateColor } from '../utils/stateUtils';


const emit = defineEmits<{
    'update:modelValue': [value: number | null]
}>()

const stateOptions = ref<Array<{ value: number, label: string }>>([])
const loading = ref(false)

const loadStates = async () => {
    loading.value = true
    try {
        const stateMap = await getStateCache()
        if (stateMap) {
            stateOptions.value = Object.entries(stateMap).map(([code, name]) => ({
                value: Number(code),
                label: name
            }))
        }
    } catch (error) {
        console.error('Failed to load states:', error)
    } finally {
        loading.value = false
    }
}

const getTagType = (value: number) => {
    return getStateColor(value)
}

const handleChange = (value: number | null) => {
    emit('update:modelValue', value)
}

onMounted(() => {
    loadStates()
})
</script>

<style scoped>
.el-select {
    width: 150px;
    display: inline-block;
}

.el-tag {
    min-width: 60px;
    text-align: center;
    white-space: nowrap;
}
</style>