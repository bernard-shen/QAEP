import request from '../request'

// Mock数据管理模块接口
export default {
    // 获取连接列表
    getConnectionList(params) {
        return request({
            url: '/mockdata/connections/',
            method: 'get',
            params
        })
    },

    // 检查连接名是否存在
    checkConnectName(params) {
        return request({
            url: '/mockdata/connections/check-name/',
            method: 'get',
            params
        })
    },

    // 新增连接
    addConnection(data) {
        return request({
            url: '/mockdata/connections/create/',
            method: 'post',
            data
        })
    },

    // 删除连接
    deleteConnection(connectId) {
        return request({
            url: `/mockdata/connections/${connectId}/delete/`,
            method: 'delete'
        })
    },

    // 更新连接
    updateConnection(connectId, data) {
        return request({
            url: `/mockdata/connections/${connectId}/update/`,
            method: 'put',
            data
        })
    },

    // 测试连接
    testConnection(data) {
        return request({
            url: '/mockdata/connections/test/',
            method: 'post',
            data
        })
    },

    // 执行造数
    mockConnectData(data) {
        return request({
            url: '/mockdata/mock-data/',
            method: 'post',
            data,
            timeout: 60000
        })
    },

    // 获取数据库列表
    getDbList(params) {
        return request({
            url: '/mockdata/db-list/',
            method: 'get',
            params
        })
    },

    // 获取表列表
    getTableList(params) {
        return request({
            url: '/mockdata/table-list/',
            method: 'get',
            params
        })
    },

    // 获取字段列表
    getColumnList(params) {
        return request({
            url: '/mockdata/column-list/',
            method: 'get',
            params
        })
    },

    // 获取隐私字段列表
    getSecretList(params) {
        return request({
            url: '/mockdata/secret-list/',
            method: 'get',
            params
        })
    },

    // 文件造数
    mockDataFile(data) {
        return request({
            url: '/mockdata/mock-data-file/',
            method: 'post',
            data,
            timeout: 60000,  // 设置超时时间为1分钟
            responseType: 'blob',
            headers: {
                'Content-Type': 'application/json',
                'Accept': '*/*'
            }
        })
    }
} 