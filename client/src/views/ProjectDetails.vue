<template>
  <div class="project-details">
    <div class="search-bar">
      <el-input v-model="projectId" placeholder="请输入项目ID" />
      <el-button type="primary" @click="fetchProjectDetails">搜索</el-button>
    </div>
    <div v-if="project">
      <h2 class="project-title">{{ project.project_name }}</h2>
      <p class="project-description">{{ project.description }}</p>
      <span :class="['project-state', getStateType(project.state)]">
        {{ projectStateLabel }}
      </span>
      <h3 class="child-nodes-title">子节点列表</h3>
      <ul class="node-list">
        <NodeItem v-for="node in nodes" :key="node.node_id" :node="node" />
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import NodeItem from '../components/NodeItem.vue'
import { getStateType, getStateLabel } from '../utils/stateUtils'
import { ElMessage } from 'element-plus'

const route = useRoute()

const projectId = ref(route.query.projectId || '')

const project = ref(null)
const nodes = ref([])
const projectStateLabel = ref('')

const fetchProjectDetails = async () => {
  if (projectId.value === '') {
    ElMessage.warning('请输入项目ID')
    return
  }
  try {
    const projectResponse = await axios.get(`/api/project/get/${projectId.value}`)
    project.value = projectResponse.data
    projectStateLabel.value = await getStateLabel(project.value.state)

    const nodesResponse = await axios.get(`/api/node/tree/${project.value.node_id}`)
    nodes.value = nodesResponse.data.children || []
  } catch (error) {
    if (error.response && error.response.status === 404) {
      ElMessage.error('项目不存在')
    } else {
      ElMessage.error('获取项目详情失败，请稍后再试')
    }
  }
}

onMounted(fetchProjectDetails)
</script>

<style scoped>
.project-details {
  padding: 20px;
  background-color: #f7f9fc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar .el-input {
  flex: 1;
  margin-right: 10px;
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
  margin-bottom: 10px;
}

.project-state {
  font-size: 0.9em;
  color: #fff;
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 20px;
}

.project-state.info {
  background-color: #3498db;
}

.project-state.warning {
  background-color: #f39c12;
}

.project-state.success {
  background-color: #2ecc71;
}

.project-state.danger {
  background-color: #e74c3c;
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