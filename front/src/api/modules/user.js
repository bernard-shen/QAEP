import request from '../request'

// 用户认证相关接口
export default {
    // 用户登录
    login(data) {
        return request({
            url: '/auth/login/',
            method: 'post',
            data
        })
    },

    // 用户注册
    register(data) {
        return request({
            url: '/auth/register/',
            method: 'post',
            data
        })
    },

    // 重置密码
    resetPassword(data) {
        return request({
            url: '/auth/reset-password/',
            method: 'post',
            data
        })
    }
} 