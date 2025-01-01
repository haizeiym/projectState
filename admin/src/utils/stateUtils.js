// 状态标签映射
export const getStateLabel = (state) => {
    const labels = {
        0: '未开始',
        1: '进行中',
        2: '已完成',
        3: '已取消'
    }
    return labels[state] || '未知状态'
} 