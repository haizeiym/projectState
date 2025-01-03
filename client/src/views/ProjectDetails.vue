<template>
  <div class="project-details">
    <el-input v-model="projectId" placeholder="Enter Project ID" @change="fetchProjectDetails" />
    <div v-if="project">
      <h2>{{ project.project_name }}</h2>
      <p>{{ project.description }}</p>
      <StateTag :modelValue="project.state" />
      <h3>Child Nodes</h3>
      <ul>
        <li v-for="node in nodes" :key="node.node_id">
          <h4>{{ node.node_name }}</h4>
          <p>{{ node.description }}</p>
          <StateTag :modelValue="node.state" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import StateTag from '../components/StateTag.vue'

const projectId = ref('')
const project = ref(null)
const nodes = ref([])

const fetchProjectDetails = async () => {
  try {
    const projectResponse = await axios.get(`/api/project/get/${projectId.value}`)
    project.value = projectResponse.data

    const nodesResponse = await axios.get(`/api/node/tree/${projectId.value}`)
    nodes.value = nodesResponse.data
  } catch (error) {
    console.error('Failed to fetch project details:', error)
  }
}
</script>

<style scoped>
.project-details {
  padding: 20px;
}

@media (max-width: 600px) {
  .project-details {
    padding: 10px;
  }
}
</style> 