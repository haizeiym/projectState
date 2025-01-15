<template>
    <div class="app-wrapper">
        <div class="main-container">
            <router-view />
        </div>
    </div>
</template>

<script setup>
// Layout component logic here
</script>

<style scoped>
.app-wrapper {
    min-height: 100vh;
    width: 100%;
}

.main-container {
    min-height: 100vh;
    padding: 20px;
}
</style>