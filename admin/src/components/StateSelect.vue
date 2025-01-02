<template>
    <el-select v-model="selectedState" @change="handleChange">
        <el-option v-for="(label, value) in stateOptions" :key="value" :label="label" :value="Number(value)">
            <el-tag :type="getStateType(Number(value))">{{ label }}</el-tag>
        </el-option>
    </el-select>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { getStateType, getStateCache } from '../utils/stateUtils'

const props = defineProps({
    modelValue: {
        type: Number,
        default: 0
    }
})

const emit = defineEmits(['update:modelValue'])

const selectedState = ref(props.modelValue)
const stateOptions = ref({})

// Fetch state options dynamically
const fetchStateOptions = async () => {
    stateOptions.value = await getStateCache()
}

// Fetch state options on component mount
onMounted(fetchStateOptions)

// Handle selection change
const handleChange = (value) => {
    emit('update:modelValue', value)
}

// Watch for external value changes
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