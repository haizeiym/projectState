<template>
    <li class="node-item">
        <div class="node-info">
            <h4 class="node-name">{{ node.node_name }}</h4>
            <p class="node-description">{{ node.description }}</p>
            <span class="node-state">{{ node.state }}</span>
        </div>
        <ul v-if="node.children && node.children.length" class="child-nodes">
            <NodeItem v-for="child in node.children" :key="child.node_id" :node="child" />
        </ul>
    </li>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    node: {
        type: Object,
        required: true
    }
})
</script>

<style scoped>
.node-item {
    margin-bottom: 2px;
    padding: 2px;
    border: 1px solid #ccc;
    border-radius: 3px;
    background-color: #f0f8ff;
    transition: background-color 0.3s;
}

.node-item:hover {
    background-color: #e0f7fa;
}

ul {
    padding-left: 15px;
    margin-top: 2px;
}

.child-nodes {
    border-left: 1px dashed #ccc;
    margin-left: 5px;
    padding-left: 5px;
}

.node-info {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.node-name {
    font-size: 1em;
    font-weight: bold;
    margin-right: 5px;
    color: #2c3e50;
}

.node-description {
    font-size: 0.9em;
    color: #7f8c8d;
    margin-right: 5px;
}

.node-state {
    font-size: 0.9em;
    color: #fff;
    background-color: #3498db;
    padding: 1px 3px;
    border-radius: 2px;
}
</style>