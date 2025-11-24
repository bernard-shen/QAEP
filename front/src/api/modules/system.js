import request from '../request'

// 系统管理模块接口
export default {
    // 用户管理
    getUserList(params) {
        return request({
            url: '/users/',
            method: 'get',
            params
        })
    },
    getUserDetail(params) {
        return request({
            url: '/users/detail/',
            method: 'get',
            params  // 直接传递 params 对象
        })
    },
    createUser(data) {
        return request({
            url: '/users/create/',
            method: 'post',
            data
        })
    },
    updateUser(userId, data) {
        return request({
            url: `/users/${userId}/update/`,
            method: 'put',
            data
        })
    },
    deleteUser(userId) {
        return request({
            url: `/users/${userId}/delete/`,
            method: 'delete'
        })
    },

    // 角色管理
    getRoleList(params) {
        return request({
            url: '/roles/',
            method: 'get',
            params
        })
    },
    createRole(data) {
        return request({
            url: '/roles/create/',
            method: 'post',
            data
        })
    },
    updateRole(roleId, data) {
        return request({
            url: `/roles/${roleId}/update/`,
            method: 'put',
            data
        })
    },
    deleteRole(roleId) {
        return request({
            url: `/roles/${roleId}/delete/`,
            method: 'delete'
        })
    },

    // 菜单管理
    getMenuList(params) {
        return request({
            url: '/menus/',
            method: 'get',
            params
        })
    },
    getUserMenu() {
        return request({
            url: '/users/menu',
            method: 'get'
        })
    },
    createMenu(data) {
        return request({
            url: '/menus/create/',
            method: 'post',
            data
        })
    },
    updateMenu(menuId, data) {
        return request({
            url: `/menus/${menuId}/update/`,
            method: 'put',
            data
        })
    },
    deleteMenu(menuId) {
        return request({
            url: `/menus/${menuId}/delete/`,
            method: 'delete'
        })
    }
} 