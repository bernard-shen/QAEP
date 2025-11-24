import request from '../request'

// 设备管理模块接口
export default {
    // 获取设备列表
    getDeviceList(params) {
        return request({
            url: '/devices/',
            method: 'get',
            params
        })
    },

    // 创建设备
    createDevice(data) {
        return request({
            url: '/devices/create/',
            method: 'post',
            data
        })
    },

    // 获取设备详情
    getDeviceDetail(deviceId) {
        return request({
            url: `/devices/${deviceId}/`,
            method: 'get'
        })
    },

    // 更新设备信息
    updateDevice(deviceId, data) {
        return request({
            url: `/devices/${deviceId}/update/`,
            method: 'put',
            data
        })
    },

    // 删除设备
    deleteDevice(deviceId) {
        return request({
            url: `/devices/${deviceId}/delete/`,
            method: 'delete'
        })
    },

    // 占用设备
    occupyDevice(deviceId, data) {
        return request({
            url: `/devices/${deviceId}/occupy/`,
            method: 'post',
            data
        })
    },

    // 申请设备
    applyDevice(deviceId, data) {
        return request({
            url: `/devices/${deviceId}/apply/`,
            method: 'post',
            data
        })
    },

    // 释放设备
    releaseDevice(deviceId) {
        return request({
            url: `/devices/${deviceId}/release/`,
            method: 'post'
        })
    },

    // 接口资产模块接口
    getApiList(params) {
        return request({
            url: '/apis/get_api_list',
            method: 'get',
            params
        })
    },

    // 数据库连接管理
    getConnectionList() {
        return request({
            url: '/mock/mockData/getConnectionList',
            method: 'get'
        })
    },
    addConnection(data) {
        return request({
            url: '/mock/mockData/addConnection',
            method: 'post',
            data
        })
    },
    updateConnection(data) {
        return request({
            url: '/mock/mockData/updateConnection',
            method: 'post',
            data
        })
    },
    deleteConnection(params) {
        return request({
            url: '/mock/mockData/delConnection',
            method: 'get',
            params
        })
    },
    testConnect(data) {
        return request({
            url: '/mock/mockData/testConnect',
            method: 'post',
            data
        })
    },

    // 数据库操作
    getDbList(data) {
        return request({
            url: '/mock/mockData/getDbList',
            method: 'post',
            data
        })
    },
    getTableList(data) {
        return request({
            url: '/mock/mockData/getTableList',
            method: 'post',
            data
        })
    },
    getColumnList() {
        return request({
            url: '/mock/mockData/getColumnList',
            method: 'get'
        })
    },

    // 获取设备申请列表
    getApplyList(params) {
        return request({
            url: '/devices/applies/',
            method: 'get',
            params
        })
    },

    // 审批设备申请
    approveApply(applyId, data) {
        return request({
            url: `/devices/applies/${applyId}/approve/`,
            method: 'post',
            data
        })
    }
}
