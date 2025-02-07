<template>
    <div class="node-tree">
        <div class="header">
            <h2>节点管理</h2>
            <div class="header-actions">
                <el-button type="primary" @click="toggleNodeIdVisibility">
                    {{ showNodeId ? '隐藏节点ID' : '显示节点ID' }}
                </el-button>
                <el-button type="success" @click="handleSendNodes">
                    <el-icon>
                        <Message />
                    </el-icon>发送节点
                </el-button>
                <el-button type="primary" @click="handleAddNode">
                    <el-icon>
                        <Plus />
                    </el-icon>添加节点
                </el-button>
                <el-button @click="handleClose">
                    <el-icon>
                        <Back />
                    </el-icon>返回项目列表
                </el-button>
            </div>
        </div>
        <el-table :data="treeData" style="width: 100%" row-key="node_id"
            :tree-props="{ children: 'children', hasChildren: 'hasChildren' }" default-expand-all>
            <el-table-column v-if="showNodeId" prop="node_id" label="节点ID" />
            <el-table-column prop="node_name" label="节点名称" />
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="state" label="状态">
                <template #default="scope">
                    <StateTag :modelValue="scope.row.state" />
                </template>
            </el-table-column>
            <el-table-column label="操作" width="280">
                <template #default="scope">
                    <div class="action-buttons">
                        <el-button type="success" link @click="handleAddChild(scope.row)" class="action-button">
                            <el-icon>
                                <Plus />
                            </el-icon>添加子节点
                        </el-button>
                        <el-button type="primary" link @click="handleEdit(scope.row)" class="action-button">
                            <el-icon>
                                <Edit />
                            </el-icon>编辑
                        </el-button>
                        <el-button type="danger" link @click="handleDelete(scope.row)" class="action-button">
                            <el-icon>
                                <Delete />
                            </el-icon>删除
                        </el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog v-model="tgDialogVisible" title="选择发送目标" width="30%">
            <el-form>
                <el-form-item label="选择TG">
                    <el-select v-model="selectedTgData" placeholder="请选择TG">
                        <el-option v-for="item in tgConfigs" :key="item.tg_id" :label="item.tg_name" :value="item" />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleCancel">取消</el-button>
                    <el-button type="primary" @click="sendNodesInfo">
                        发送
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Back, Edit, Delete, Message } from '@element-plus/icons-vue'
import { getNodeTree, deleteNode } from '../../api/node'
import { getAllTgConfigs } from '../../utils/tgUtils'
import StateTag from '../../components/StateTag.vue'
import { getStateListData, getStateEmoji } from '../../utils/stateUtils'
import { TgConfig } from '../../utils/tgUtils'
import { sendMessage } from '../../api/pntg'

const route = useRoute()
const router = useRouter()
const treeData = ref([])
const showNodeId = ref(false)
const tgDialogVisible = ref(false)
const selectedTgData = ref<TgConfig | null>(null)
const tgConfigs = ref<TgConfig[]>([])
const stateCache = ref<Record<number, string> | null>(null)
const fetchNodeTree = async () => {
    try {
        const nodeId = Number(route.params.nodeId)
        const response: any = await getNodeTree(nodeId)
        treeData.value = response.children || []
    } catch (error: any) {
        ElMessage.error('获取节点树失败')
        console.error('Error fetching node tree:', error)
    }
}

const handleAddNode = () => {
    const nodeId = route.params.nodeId
    router.push(`/main/node/add/${nodeId}?parent_id=${nodeId}`)
}

const handleAddChild = (data: any) => {
    router.push(`/main/node/add/${route.params.nodeId}?parent_id=${data.node_id}`)
}

const handleEdit = (data: any) => {
    router.push(`/main/node/edit/${data.node_id}?parent_id=${route.params.nodeId}`)
}

const handleDelete = (data: any) => {
    ElMessageBox.confirm('确定要删除该节点吗？', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        try {
            await deleteNode(data.node_id)
            ElMessage.success('删除成功')
            await fetchNodeTree()
        } catch (error) {
            ElMessage.error('删除失败')
        }
    })
}

const handleClose = () => {
    router.push('/main/projects')
}

const toggleNodeIdVisibility = () => {
    showNodeId.value = !showNodeId.value
}

const handleSendNodes = async () => {
    getTgConfigs()
    stateCache.value = await getStateListData()
    tgDialogVisible.value = true
}

const getTgConfigs = async () => {
    try {
        const response: any = await getAllTgConfigs()
        tgConfigs.value = response
    } catch (error) {
        ElMessage.error('获取TG配置失败')
    }
}

const generateNodesInfo = (nodes: any[], level = 0) => {
    let info = ''

    // 当 state_code 不为 '0' 时，收集所有匹配状态的节点，不考虑层级
    if (selectedTgData.value?.state_code !== '0') {
        const collectMatchingNodes = (nodes: any[]) => {
            nodes.forEach(node => {
                // 如果状态匹配且是叶子节点，添加到结果中
                if (node.state.toString() === selectedTgData.value?.state_code &&
                    (!node.children || node.children.length === 0)) {
                    const stateEmoji = getStateEmoji(node.state)
                    info += `${stateEmoji} ${node.node_name}`
                    if (node.description) {
                        info += ` ${node.description}`
                    }
                    info += '\n'
                }

                // 递归检查子节点
                if (node.children && node.children.length > 0) {
                    collectMatchingNodes(node.children)
                }
            })
        }

        collectMatchingNodes(nodes)
        return info
    }

    // 当 state_code 为 '0' 时，保持原有的树形结构显示
    nodes.forEach(node => {
        const stateEmoji = getStateEmoji(node.state)

        // 添加当前节点信息
        info += '  '.repeat(level) + `**${node.node_name}**`
        if (node.description) {
            info += ` ${node.description}`
        }
        info += '\n'

        // 添加状态信息
        if (level > 0 || !node.children || node.children.length === 0) {
            info += '  '.repeat(level + 1) + `└─ ${stateEmoji}**${stateCache.value?.[node.state] || '未知状态'}**\n`
        }

        // 递归处理子节点
        if (node.children && node.children.length > 0) {
            info += generateNodesInfo(node.children, level + 1)
        }
    })

    return info
}

const sendNodesInfo = async () => {
    if (!selectedTgData.value) {
        ElMessage.warning('请选择发送目标')
        return
    }

    try {
        const nodesInfo = generateNodesInfo(treeData.value)
        if (nodesInfo.trim() === '') return ElMessage.warning('没有满足发送条件的节点')
        console.log(nodesInfo)
        await sendMessage(
            selectedTgData.value.bot_token,
            selectedTgData.value.chat_id,
            selectedTgData.value.url,
            nodesInfo
        )

        ElMessage.success('发送成功')
        resetAndClose()
    } catch (error) {
        ElMessage.error('发送失败')
    }
}

const resetAndClose = () => {
    selectedTgData.value = null
    tgDialogVisible.value = false
}

const handleCancel = () => {
    resetAndClose()
}

onMounted(() => {
    fetchNodeTree()
})
</script>

<style scoped>
.node-tree {
    padding: 20px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.header h2 {
    margin: 0;
}

.header-actions {
    display: flex;
    gap: 10px;
}

.action-buttons {
    display: flex;
    gap: 8px;
}

.action-button {
    display: flex;
    align-items: center;
    gap: 4px;
}

.action-button .el-icon {
    margin-right: 2px;
}
</style>