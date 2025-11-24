import request from '../request'

// 首页看板模块接口
export default {
    // 获取首页统计数据
    getHomeData() {
        return request({
            url: '/home/counts',
            method: 'get'
        })
    },
    
    // 获取趋势数据
    getTrendData() {
        return request({
            url: '/home/trends',
            method: 'get'
        })
    },

    // 获取接口分布数据
    getApiDistribution() {
        return request({
            url: '/home/api-distribution',
            method: 'get'
        })
    },

    // 获取用例执行分布数据
    getCaseDistribution() {
        return request({
            url: '/home/case-distribution',
            method: 'get'
        })
    }
} 