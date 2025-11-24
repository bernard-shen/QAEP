import request from '../request'

// 接口资产模块接口
export default {
    // 获取接口列表
    getApiList(params) {
        return request({
            url: '/apis',
            method: 'get',
            params
        })
    },

    // 创建接口
    createApi(data) {
        return request({
            url: '/apis/create/',
            method: 'post',
            data
        })
    },

    // 获取接口详情
    getApiDetail(id) {
        return request({
            url: `/apis/${id}/`,
            method: 'get'
        })
    },

    // 更新接口
    updateApi(id, data) {
        return request({
            url: `/apis/${id}/update/`,
            method: 'put',
            data
        })
    },

    // 删除接口
    deleteApi(id) {
        return request({
            url: `/apis/${id}/delete/`,
            method: 'delete'
        })
    }
} 