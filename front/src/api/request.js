import axios from 'axios'
import config from '../config'
import { ElMessage } from 'element-plus'
import store from '../store'

const NETWORK_ERROR = '网络请求错误，请稍后重试...'

// 创建一个axios实例对象
const service = axios.create({
    baseURL: config.baseApi,
    timeout: 5000,
    withCredentials: true,
})

// 在请求之前做一些统一处理
service.interceptors.request.use((req) => {
    // 打印请求信息
    console.log('请求配置:', {
        url: req.url,
        method: req.method,
        params: req.params,
        data: req.data
    });

    const token = store.getters.token || store.state.token

    // 如果 token 存在，则添加到请求头中
    if (token) {
        req.headers.Authorization = `Bearer ${token}`
    }
    return req
}, error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
})

// 在请求之后可以做一些统一处理
service.interceptors.response.use((res) => {
    console.log('响应数据:', res.data);

    // 如果是文件下载请求，直接返回响应
    if (res.config.responseType === 'blob') {
        return res;
    }
    
    if (res.status === 200) {
        return res.data
    } else {
        ElMessage.error(res.data?.msg || NETWORK_ERROR)
        return Promise.reject(res.data?.msg || NETWORK_ERROR)
    }
}, error => {
    console.error('响应错误:', error);
    
    // 添加更详细的错误信息
    if (error.code === 'ERR_NETWORK') {
        ElMessage.error('无法连接到服务器，请确认服务器是否启动');
        return Promise.reject(new Error('无法连接到服务器，请确认服务器是否启动'));
    }
    
    // 处理文件下载错误
    if (error.config?.responseType === 'blob') {
        return Promise.reject(new Error('文件下载失败'));
    }
    
    ElMessage.error(error.message || NETWORK_ERROR);
    return Promise.reject(error);
})

// 封装的核心函数
function request(options) {
    options.method = options.method || 'get'
    
    // 修改这里的参数处理逻辑
    if (options.method.toLowerCase() === 'get') {
        // 如果是 GET 请求，使用传入的 params
        options.params = options.params || {}
    } else {
        // 非 GET 请求使用 data
        options.data = options.data || {}
    }

    // 对mock的处理：如果单独的配置存在mock，则用单独的配置
    let isMock = config.mock 
    if (typeof options.mock !== 'undefined') {
        isMock = options.mock
    }

    // 对线上环境判断处理，如果是线上环境，则不走mock
    if (config.env == 'prod'){
        service.defaults.baseURL = config.baseApi
    } else {
        service.defaults.baseURL = isMock ? config.mockApi : config.baseApi
    }

    return service(options)
}

export default request