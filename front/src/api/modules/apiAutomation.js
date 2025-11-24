import request from '../request'

const apiAutomation = {
    // 环境管理接口
    getEnvironments(params) {
        return request({
            url: '/api-automation/environments/',
            method: 'get',
            params
        })
    },
    
    createEnvironment(data) {
        return request({
            url: '/api-automation/environments/create/',
            method: 'post',
            data
        })
    },
    
    updateEnvironment(id, data) {
        return request({
            url: `/api-automation/environments/${id}/update/`,
            method: 'put',
            data
        })
    },
    
    deleteEnvironment(id) {
        return request({
            url: `/api-automation/environments/${id}/delete/`,
            method: 'delete'
        })
    },

    // 账号管理接口
    getAccounts(params) {
        return request({
            url: '/api-automation/accounts/',
            method: 'get',
            params
        })
    },
    
    createAccount(data) {
        return request({
            url: '/api-automation/accounts/create/',
            method: 'post',
            data
        })
    },
    
    updateAccount(id, data) {
        return request({
            url: `/api-automation/accounts/${id}/update/`,
            method: 'put',
            data
        })
    },
    
    deleteAccount(id) {
        return request({
            url: `/api-automation/accounts/${id}/delete/`,
            method: 'delete'
        })
    },

    // 测试用例管理接口
    getTestCases(params) {
        return request({
            url: '/api-automation/test-cases/',
            method: 'get',
            params
        })
    },
    
    createTestCase(data) {
        return request({
            url: '/api-automation/test-cases/create/',
            method: 'post',
            data
        })
    },
    
    updateTestCase(id, data) {
        return request({
            url: `/api-automation/test-cases/${id}/update/`,
            method: 'post',
            data
        })
    },
    
    deleteTestCase(id) {
        return request({
            url: `/api-automation/test-cases/${id}/delete/`,
            method: 'post'
        })
    },

    debugTestCase(id) {
        return request({
            url: `/api-automation/test-cases/${id}/debug/`,
            method: 'post'
        })
    },

    executeTestCase(id) {
        return request({
            url: `/api-automation/test-cases/${id}/execute/`,
            method: 'post'
        })
    },

    // 获取可用接口列表（用于测试用例选择）
    getAvailableApis(params) {
        return request({
            url: '/apis/',
            method: 'get',
            params
        })
    },

    // 获取接口详情
    getApiDetail(id) {
        return request({
            url: `/apis/${id}/`,
            method: 'get'
        })
    }
}

export default apiAutomation 