import { createStore } from 'vuex'
import Cookie from 'js-cookie'

// 封装动态导入函数
const loadView = (url) => {
    /* @vite-ignore */
    return import(`../views/${url}.vue`)
}

export default createStore({
    state: {
        isCollapse: false,
        currentMenu: null,
        tabsList: [
            {
                path: '/',
                name: 'home',
                label: '首页',
                icon: 'home'
            }
        ],
        menu: [],
        token: '',
        userInfo: {},
        connection_info: {},
    },
    mutations: {
        updateIsCollapse(state, payload) {
            state.isCollapse = !state.isCollapse
        },

        selectMenu(state, val) {
            if (val.name == 'home') {
                state.currentMenu = null
            } else {
                state.currentMenu = val
                let result = state.tabsList.findIndex(item => item.name === val.name)
                result == -1 ? state.tabsList.push(val) : ''
            }
        },

        closeTab(state, val) {
            let res = state.tabsList.findIndex(item => item.name === val.name)
            state.tabsList.splice(res, 1)
        },

        setMenu(state, val) {
            state.menu = val
            localStorage.setItem('menu', JSON.stringify(val))
        },

        addMenu(state, router) {
            if (!localStorage.getItem('menu')) {
                return
            }
            const menu = JSON.parse(localStorage.getItem('menu'))
            state.menu = menu

            // 动态路由部分
            const menuArray = []
            if (Array.isArray(menu)) {
                menu.forEach(item => {
                    if (item.children) {
                        item.children = item.children.map(item => {
                            item.component = () => loadView(item.url)
                            return item
                        })
                        menuArray.push(...item.children)
                    } else {
                        item.component = () => loadView(item.url)
                        menuArray.push(item)
                    }
                })
            }

            menuArray.forEach(item => {
                router.addRoute('home1', item)
            })
        },

        cleanMenu(state) {
            state.menu = []
            localStorage.removeItem('menu')
        },

        setToken(state, val) {
            state.token = val
            Cookie.set('token', val)
        },

        clearToken(state) {
            state.token = ''
            Cookie.remove('token')
        },

        getToken(state) {
            state.token = state.token || Cookie.get('token')
        },

        setUserInfo(state, val) {
            state.userInfo = val
            localStorage.setItem('userinfo', JSON.stringify(val))
        },
        cleanUserInfo(state) {
            state.menu = []
            localStorage.removeItem('userinfo')
        },

        setConnectInfo(state, val) {
            state.connection_info = val
            localStorage.setItem('connection_info', JSON.stringify(val))
        },
        cleanConnectInfo(state) {
            state.connection_info = []
            localStorage.removeItem('connection_info')
        },
    }
})