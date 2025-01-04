<template>
    <li>
        <div class="node-info">
            <h4 class="node-name">{{ node.node_name }}</h4>
            <p class="node-description">{{ node.description }}</p>
            <span class="node-state">{{ node.state }}</span>
        </div>
        <ul v-if="node.children && node.children.length">
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
li {
    margin-bottom: 5px;
}

ul {
    padding-left: 20px;
}

.node-info {
    display: flex;
    align-items: center;
}

.node-name {
    font-size: 1.2em;
    margin-right: 10px;
}

.node-description {
    font-size: 0.9em;
    color: #666;
    margin-right: 10px;
}

.node-state {
    font-size: 0.9em;
    color: #333;
    background-color: #f0f0f0;
    padding: 2px 6px;
    border-radius: 4px;
}
</style>