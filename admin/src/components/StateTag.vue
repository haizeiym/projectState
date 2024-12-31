<template>
    <div class="state-wrapper">
        <template v-if="editable">
            <StateSelect :modelValue="modelValue" @update:modelValue="handleChange" :disabled="disabled" />
        </template>
        <template v-else>
            <el-tag :type="getStateType(modelValue)" effect="light" class="state-tag">
                {{ getStateLabel(modelValue) }}
            </el-tag>
        </template>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import StateSelect from './StateSelect.vue'

const props = defineProps({
    modelValue: {
        type: Number,
        default: 0
    },
    editable: {
        type: Boolean,
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:modelValue', 'change'])

// 状态类型映射
const getStateType = (state) => {
    const types = {
        0: 'info',    // 未开始
        1: 'warning', // 进行中
        2: 'success', // 已完成
        3: 'danger'   // 已取消
    }
    return types[state] || 'info'
}

// 状态标签映射
const getStateLabel = (state) => {
    const labels = {
        0: '未开始',
        1: '进行中',
        2: '已完成',
        3: '已取消'
    }
    return labels[state] || '未知状态'
}

// 处理状态变化
const handleChange = (value) => {
    emit('update:modelValue', value)
    emit('change', value)
}
</script>

<style scoped>
.state-wrapper {
    display: inline-block;
}

.state-tag {
    min-width: 70px;
    text-align: center;
}
</style>