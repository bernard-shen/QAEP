// 环境配置文件

// 取当前环境，取不到默认线上环境
const env = import.meta.env.MODE || 'prod'

// 定义三种环境的 baseApi 和 mockApi
const EnvConfig = {
    development: {
        baseApi: 'http://127.0.0.1:8000',
        mockApi: 'http://127.0.0.1:8000'
    },
    test: {
        baseApi: '/',
        mockApi: 'http://127.0.0.1:8000'
        // mockApi: 'https://www.fastmock.site/mock/a6f3eb2811945bdaa1bc09998ca70cb8/bernard'

    },
    prod: {
        baseApi: 'asjkdf/api',
        mockApi: 'https:/asdklfskd/api'
    },
}

export default {
    env,
    mock: false,
    ...EnvConfig[env] //es6语法，解构出来的摸一个环境的配置内容
}