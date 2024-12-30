<template>
    <div class="page-container">
        <div class="page-header">
            <h2>{{ title }}</h2>
            <div class="header-actions">
                <slot name="actions"></slot>
            </div>
        </div>
        <div class="page-content">
            <slot></slot>
        </div>
    </div>
</template>

<script setup>
defineProps({
    title: {
        type: String,
        required: true
    }
})
</script>

<style scoped>
.page-container {
    padding: 20px;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.header-actions {
    display: flex;
    gap: 10px;
}

.page-content {
    background-color: var(--el-bg-color);
    border-radius: 4px;
    padding: 20px;
}
</style> 