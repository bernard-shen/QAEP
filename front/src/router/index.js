import { createRouter, createWebHashHistory } from 'vue-router'

// 服了，试了很多次才明白，Main.vue是路由页面的主入口，
// 其他页面路由都要在Main.vue页面的children下配置路由，包括多层嵌套；不然子页面展示时布局就会不正确；
// 官网展示只是简单的demo, 实战应用才能获得宝贵经验。
const routes = [
    {
        path: '/',
        component:() => import('../views/Main.vue'),
        redirect: '/home',
        name: 'home1',
        // 注释掉固定路由，准备使用动态路由：1、主路由name不能和子路由name重复 2、children设为空，存放动态路由
        // children: [
        //     {
        //         path: '/home',
        //         name: 'home',
        //         component:() => import('../views/home/Home.vue')
        //     },
        //     {
        //         path: '/tools',
        //         name: 'tools',
        //         component: () => import('../views/tools/Tools.vue')
        //     },
        //     {
        //         path: '/mock',
        //         redirect: '/mock/mock_data',
        //         children: [
        //             {
        //                 path: '/mock/mock_data',
        //                 name: 'mock_data',
        //                 component:() => import('../views/mock/Connect.vue')
        //             },
        //             {
        //                 path: '/mock/mock_file',
        //                 name: 'mock_file',
        //                 component:() => import('../views/mock/MockFiles.vue')
        //             }
        //         ]
        //     },
        //     {
        //         path: '/api',
        //         redirect: '/api/manage',
        //         children: [
        //             {
        //                 path: '/api/manage',
        //                 name: 'api_manage',
        //                 component:() => import('../views/apis/ApiList.vue')
        //             },
        //             {
        //                 path: '/api/test',
        //                 name: 'api_test',
        //                 component:() => import('../views/apis/ApiFailTest.vue')
        //             },
        //             {
        //                 path: '/api/flow',
        //                 name: 'api_flow',
        //                 component:() => import('../views/apis/Flow.vue')
        //             },
        //             {
        //                 path: '/api/report',
        //                 name: 'api_report',
        //                 component:() => import('../views/apis/Report.vue')
        //             }
        //         ]
        //     },
        //     {
        //         path: '/sys',
        //         redirect: '/sys/users',
        //         children: [
        //             {
        //                 path: '/sys/roles',
        //                 name: 'sys_roles',
        //                 component:() => import('../views/system/Role.vue')
        //             },
        //             {
        //                 path: '/sys/users',
        //                 name: 'sys_users',
        //                 component:() => import('../views/system/User.vue')
        //             }
        //         ]
        //     },
        //     // {
        //     // path: '*',
        //     // name: '',
        //     // component: () => import('../views/NotFound.vue') // 自定义的页面或重定向到其他页面
        //     // }
        // ]

        children: []
    },
    {        
        path: '/login',
        name: 'login',
        component:() => import('../views/Login.vue'),
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router