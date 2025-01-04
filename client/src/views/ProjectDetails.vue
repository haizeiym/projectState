<template>
  <div class="project-details">
    <el-input v-model="projectId" placeholder="Enter Project ID" @change="fetchProjectDetails" />
    <div v-if="project">
      <h2 class="project-title">{{ project.project_name }}</h2>
      <p class="project-description">{{ project.description }}</p>
      <h3 class="child-nodes-title">Child Nodes</h3>
      <ul class="node-list">
        <NodeItem v-for="node in nodes" :key="node.node_id" :node="node" />
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import NodeItem from '../components/NodeItem.vue'

const projectId = ref('')
const project = ref(null)
const nodes = ref([])

const fetchProjectDetails = async () => {
  try {
    const projectResponse = await axios.get(`/api/project/get/${projectId.value}`)
    project.value = projectResponse.data

    const nodesResponse = await axios.get(`/api/node/tree/${project.value.node_id}`)
    nodes.value = nodesResponse.data.children || []
  } catch (error) {
    console.error('Failed to fetch project details:', error)
  }
}
</script>

<style scoped>
.project-details {
  padding: 20px;
  background-color: #f7f9fc;
  /* Light background for contrast */
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.project-title {
  font-size: 1.5em;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 10px;
}

.project-description {
  font-size: 1em;
  color: #7f8c8d;
  margin-bottom: 20px;
}

.child-nodes-title {
  font-size: 1.2em;
  font-weight: bold;
  color: #34495e;
  margin-bottom: 10px;
}

.node-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

@media (max-width: 600px) {
  .project-details {
    padding: 10px;
  }
}
</style>