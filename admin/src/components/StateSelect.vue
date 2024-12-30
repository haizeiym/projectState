<template>
    <el-select v-model="selectedState" @change="handleChange">
        <el-option
            v-for="(label, value) in stateOptions"
            :key="value"
            :label="label"
            :value="Number(value)"
        >
            <el-tag :type="getStateType(Number(value))">{{ label }}</el-tag>
        </el-option>
    </el-select>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
    modelValue: {
        type: Number,
        default: 0
    }
})

const emit = defineEmits(['update:modelValue'])

const selectedState = ref(props.modelValue)

// 状态选项
const stateOptions = {
    0: '未开始',
    1: '进行中',
    2: '已完成',
    3: '已取消'
}

// 状态类型映射
const getStateType = (state) => {
    const types = {
        0: 'info',
        1: 'warning',
        2: 'success',
        3: 'danger'
    }
    return types[state] || ''
}

// 处理选择变化
const handleChange = (value) => {
    emit('update:modelValue', value)
}

// 监听外部值变化
watch(() => props.modelValue, (newVal) => {
    selectedState.value = newVal
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