<template>
    <div class="state-wrapper">
        <template v-if="editable">
            <StateSelect :modelValue="modelValue" @update:modelValue="handleChange" :disabled="disabled" />
        </template>
        <template v-else>
            <el-tag :type="getStateType(modelValue)" effect="light" class="state-tag">
                {{ stateLabel }}
            </el-tag>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import StateSelect from './StateSelect.vue'
import { getStateLabel, getStateType } from '../utils/stateUtils'

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

const stateLabel = ref('未知状态')

// Fetch the state label when the component is mounted or when modelValue changes
const fetchStateLabel = async () => {
    stateLabel.value = await getStateLabel(props.modelValue)
}

watch(() => props.modelValue, fetchStateLabel, { immediate: true })

// 处理状态变化
const handleChange = (value: number | null) => {
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