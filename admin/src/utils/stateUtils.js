import axios from 'axios';

let stateCache = null;

export const getStateLabel = async (state) => {
    if (!stateCache) {
        try {
            const response = await axios.get('/api/statecode/list');
            stateCache = response.data.reduce((acc, item) => {
                acc[item.state_code] = item.state_name;
                return acc;
            }, {});
            return stateCache[state] || '未知状态';
        } catch (error) {
            console.error('Failed to fetch state codes:', error);
            return '未知状态';
        }
    }
    return stateCache[state] || '未知状态';
};

export const getStateCache = async () => {
    if (!stateCache) {
        try {
            const response = await axios.get('/api/statecode/list');
            stateCache = response.data.reduce((acc, item) => {
                acc[item.state_code] = item.state_name;
                return acc;
            }, {});
            return stateCache;
        } catch (error) {
            console.error('Failed to get state codes:', error);
            return {};
        }
    }
    return stateCache;
};

export const updateStateLabel = async (stateData) => {
    if (stateData) {
        stateCache = stateData.reduce((acc, item) => {
            acc[item.state_code] = item.state_name;
            return acc;
        }, {});
        return
    }
    try {
        const response = await axios.get('/api/statecode/list');
        stateCache = response.data.reduce((acc, item) => {
            acc[item.state_code] = item.state_name;
            return acc;
        }, {});
    } catch (error) {
        console.error('Failed to fetch state codes:', error);
    }
};

// 状态类型映射
export const getStateType = (state) => {
    if (typeof state === 'string') {
        state = Number(state)
    }
    if (state >= 1000 && state < 2000) {
        return 'info'
    } else if (state >= 2000 && state < 3000) {
        return 'warning'
    } else if (state >= 3000 && state < 4000) {
        return 'success'
    } else if (state >= 4000 && state < 5000) {
        return 'danger'
    }
    return 'info'
}