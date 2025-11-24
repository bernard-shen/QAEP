import userApi from './modules/user'
import systemApi from './modules/system'
import deviceApi from './modules/device'
import assetApi from './modules/asset'
import dashboardApi from './modules/dashboard'
import mockDataApi from './modules/mockData'
import apiAutomationApi from './modules/apiAutomation'

// 命名导出
export {
    userApi,
    systemApi,
    deviceApi,
    assetApi,
    dashboardApi,
    mockDataApi,
    apiAutomationApi
}

// 默认导出 - 展开所有模块的方法
export default {
    ...userApi,
    ...systemApi,
    ...deviceApi,
    ...assetApi,
    ...dashboardApi,
    ...mockDataApi,
    ...apiAutomationApi
} 


