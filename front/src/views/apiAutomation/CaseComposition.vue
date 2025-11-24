<template>
    <div>
        <div class="case-header">
            <el-button type="primary" @click="handleAdd">+新增用例</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="环境">
                    <el-select v-model="formInline.env" placeholder="请选择环境" clearable>
                        <el-option v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="业务">
                    <el-input v-model="formInline.business" placeholder="请输入业务名称" clearable />
                </el-form-item>
                <el-form-item label="用例名称">
                    <el-input v-model="formInline.name" placeholder="请输入用例名称" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                    <el-button @click="resetSearch">重置</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div class="table">
            <el-table :data="caseList" style="width: 100%" height="500px" border v-loading="loading">
                <el-table-column prop="name" label="用例名称" min-width="200" show-overflow-tooltip />
                <el-table-column prop="business" label="所属业务" min-width="150" show-overflow-tooltip />
                <el-table-column prop="env" label="环境" min-width="120">
                    <template #default="scope">
                        {{ getEnvLabel(scope.row.env) }}
                    </template>
                </el-table-column>
                <el-table-column prop="account" label="账户" min-width="120" show-overflow-tooltip />
                <el-table-column prop="api_list" label="接口数量" min-width="100">
                    <template #default="scope">
                        {{ scope.row.api_list.length }}
                    </template>
                </el-table-column>
                <el-table-column prop="run_status" label="运行状态" min-width="100">
                    <template #default="scope">
                        <el-tag :type="scope.row.run_status === 'normal' ? 'success' : 'danger'">
                            {{ scope.row.run_status === 'normal' ? '正常' : '异常' }}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="update_time" label="更新时间" min-width="180">
                    <template #default="scope">
                        {{ formatDate(scope.row.update_time) }}
                    </template>
                </el-table-column>
                <el-table-column fixed="right" label="操作" min-width="280">
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button type="success" size="small" @click="handleDebug(scope.row)">调试</el-button>
                        <el-button type="primary" size="small" @click="handleExecute(scope.row)">执行</el-button>
                        <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" background layout="total, prev, pager, next" :total="config.total"
                :page-size="config.pageSize" @current-change="changePage" />
        </div>

        <!-- 右侧抽屉 -->
        <el-drawer v-model="drawerVisible" :title="drawerTitle" direction="rtl" size="60%">
            <el-form :model="formCase" ref="caseForm" label-width="120px" :rules="formRules">
                <el-form-item label="用例名称" prop="name">
                    <el-input v-model="formCase.name" placeholder="请输入用例名称" />
                </el-form-item>
                <el-form-item label="所属业务" prop="business">
                    <el-input v-model="formCase.business" placeholder="请输入所属业务" />
                </el-form-item>
                <el-form-item label="环境" prop="env">
                    <el-select v-model="formCase.env" placeholder="请选择环境">
                        <el-option v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="账户" prop="account">
                    <el-select v-model="formCase.account" placeholder="请选择账户" filterable>
                        <el-option v-for="item in accountOptions" :key="item.username" :label="item.username" :value="item.username" />
                    </el-select>
                </el-form-item>

                <!-- 接口列表 -->
                <div class="api-list-section">
                    <div class="section-header">
                        <h3>接口列表</h3>
                        <el-button type="primary" @click="handleAddApi">添加接口</el-button>
                    </div>
                    <el-table :data="formCase.api_list" style="width: 100%" border>
                        <el-table-column type="index" label="序号" width="50" />
                        <el-table-column label="接口名称" min-width="200">
                            <template #default="scope">
                                <el-select 
                                    v-if="!scope.row.api_id" 
                                    v-model="scope.row.api_id" 
                                    placeholder="请选择接口"
                                    filterable
                                    @change="(val) => handleApiSelect(val, scope.$index)">
                                    <el-option 
                                        v-for="item in availableApis" 
                                        :key="item.id" 
                                        :label="item.api_name" 
                                        :value="item.id" />
                                </el-select>
                                <span v-else>{{ scope.row.api_name }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="api_path" label="接口路径" min-width="200" show-overflow-tooltip />
                        <el-table-column prop="req_method" label="请求方法" width="100" />
                        <el-table-column prop="req_header" label="请求头" min-width="150" show-overflow-tooltip>
                            <template #default="scope">
                                <el-tooltip 
                                    effect="dark" 
                                    placement="top" 
                                    :content="formatJson(scope.row.req_header)">
                                    <span>{{ formatJson(scope.row.req_header) }}</span>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column prop="req_body" label="请求体" min-width="150" show-overflow-tooltip>
                            <template #default="scope">
                                <el-tooltip 
                                    effect="dark" 
                                    placement="top" 
                                    :content="formatJson(scope.row.req_body)">
                                    <span>{{ formatJson(scope.row.req_body) }}</span>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column prop="assert_body" label="断言值" min-width="150" show-overflow-tooltip>
                            <template #default="scope">
                                <el-tooltip 
                                    effect="dark" 
                                    placement="top" 
                                    :content="formatJson(scope.row.assert_body)">
                                    <span>{{ formatJson(scope.row.assert_body) }}</span>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column prop="extract_value" label="提取值" min-width="150" show-overflow-tooltip>
                            <template #default="scope">
                                <el-tooltip 
                                    effect="dark" 
                                    placement="top" 
                                    :content="formatJson(scope.row.extract_value)">
                                    <span>{{ formatJson(scope.row.extract_value) }}</span>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column fixed="right" label="操作" width="150">
                            <template #default="scope">
                                <el-button 
                                    v-if="scope.row.api_id"
                                    size="small" 
                                    @click="handleConfigApi(scope.row, scope.$index)">编辑</el-button>
                                <el-button 
                                    type="danger" 
                                    size="small" 
                                    @click="handleRemoveApi(scope.$index)">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>

                <div class="drawer-footer">
                    <el-button @click="drawerVisible = false">取消</el-button>
                    <el-button type="primary" @click="onSubmit" :loading="submitLoading">保存</el-button>
                </div>
            </el-form>
        </el-drawer>

        <!-- 添加接口弹窗 -->
        <el-dialog v-model="apiDialogVisible" title="添加接口" width="60%">
            <el-form :inline="true" :model="apiSearchForm">
                <el-form-item label="接口名称">
                    <el-input v-model="apiSearchForm.api_name" placeholder="请输入接口名称" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="getAvailableApis">搜索</el-button>
                </el-form-item>
            </el-form>
            <el-table 
                ref="apiTable"
                :data="availableApis" 
                style="width: 100%" 
                height="400px" 
                border
                @selection-change="handleSelectionChange">
                <el-table-column type="selection" width="55" />
                <el-table-column prop="api_name" label="接口名称" show-overflow-tooltip />
                <el-table-column prop="api_path" label="接口路径" show-overflow-tooltip />
                <el-table-column prop="req_method" label="请求方法" width="100" />
            </el-table>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="apiDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="confirmAddApis">确定</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- 接口配置弹窗 -->
        <el-dialog v-model="configDialogVisible" title="接口配置" width="60%">
            <el-form :model="currentApiConfig" label-width="120px">
                <el-tabs v-model="configActiveTab">
                    <el-tab-pane label="请求头" name="header">
                        <el-form-item label="请求头">
                            <el-input type="textarea" v-model="currentApiConfig.req_header" :rows="8" 
                                placeholder="请输入请求头（JSON格式）" />
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="请求体" name="body">
                        <el-form-item label="请求体">
                            <el-input type="textarea" v-model="currentApiConfig.req_body" :rows="8" 
                                placeholder="请输入请求体（JSON格式）" />
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="断言" name="assert">
                        <el-form-item label="断言体">
                            <el-input type="textarea" v-model="currentApiConfig.assert_body" :rows="8" 
                                placeholder="请输入断言体（JSON格式）" />
                        </el-form-item>
                    </el-tab-pane>
                    <el-tab-pane label="提取" name="extract">
                        <el-form-item label="提取值">
                            <el-input type="textarea" v-model="currentApiConfig.extract_value" :rows="8" 
                                placeholder="请输入需要提取的值" />
                        </el-form-item>
                    </el-tab-pane>
                </el-tabs>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="configDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="saveApiConfig">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted, getCurrentInstance, computed, watch } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default defineComponent({
    name: 'CaseComposition',
    setup() {
        const { proxy } = getCurrentInstance();
        const caseList = ref([]);
        const drawerVisible = ref(false);
        const apiDialogVisible = ref(false);
        const configDialogVisible = ref(false);
        const submitLoading = ref(false);
        const loading = ref(false);
        const configActiveTab = ref('header');
        const currentApiIndex = ref(-1);
        const selectedApis = ref([]);

        // 环境选项
        const envOptions = [
            { value: 'TEST', label: '测试环境' },
            { value: 'DEV', label: '开发环境' },
            { value: 'PROD', label: '生产环境' }
        ];

        // 分页配置
        const config = reactive({
            total: 0,
            totalPages: 0,
            page: 1,
            pageSize: 10
        });

        // 搜索表单
        const formInline = reactive({
            env: '',
            business: '',
            name: ''
        });

        // 新增/编辑表单
        const formCase = reactive({
            name: '',
            business: '',
            env: '',
            account: '',
            api_list: [],
            execution_body: {},
            extract_body: {},
            assert_body: {}
        });

        // API搜索表单
        const apiSearchForm = reactive({
            api_name: ''
        });

        // 当前配置的API
        const currentApiConfig = reactive({
            req_header: '',
            req_body: '',
            assert_body: '',
            extract_value: ''
        });

        // 可用的API列表
        const availableApis = ref([]);
        const accountOptions = ref([]);

        // 表单验证规则
        const formRules = {
            name: [{ required: true, message: '请输入用例名称', trigger: 'blur' }],
            business: [{ required: true, message: '请输入所属业务', trigger: 'blur' }],
            env: [{ required: true, message: '请选择环境', trigger: 'change' }],
            account: [{ required: true, message: '请选择账户', trigger: 'change' }]
        };

        const drawerTitle = computed(() => formCase.id ? '编辑用例' : '新增用例');

        // 获取用例列表
        const getCaseList = async () => {
            loading.value = true;
            try {
                const params = {
                    page: config.page,
                    page_size: config.pageSize,
                    ...(formInline.env && { env: formInline.env }),
                    ...(formInline.business && { business: formInline.business }),
                    ...(formInline.name && { name: formInline.name })
                };
                
                const res = await proxy.$api.getTestCases(params);
                if (res.code === 200) {
                    caseList.value = res.data;
                    config.total = res.total;
                    config.totalPages = res.total_pages;
                } else {
                    ElMessage.error(res.msg || '获取用例列表失败');
                }
            } catch (error) {
                console.error('获取用例列表失败:', error);
                ElMessage.error('获取用例列表失败');
            } finally {
                loading.value = false;
            }
        };

        // 获取账户列表
        const getAccountList = async () => {
            try {
                const res = await proxy.$api.getAccounts({
                    env: formCase.env,
                    page_size: 1000
                });
                if (res.code === 200) {
                    accountOptions.value = res.data;
                }
            } catch (error) {
                console.error('获取账户列表失败:', error);
            }
        };

        // 获取可用接口列表
        const getAvailableApis = async () => {
            try {
                const params = {
                    page: 1,
                    page_size: 10,
                    ...(apiSearchForm.api_name && { api_name: apiSearchForm.api_name }),
                    ...(formCase.env && { env: formCase.env })
                };
                const res = await proxy.$api.getAvailableApis(params);
                if (res.code === 200) {
                    availableApis.value = res.data;
                }
            } catch (error) {
                console.error('获取可用接口列表失败:', error);
                ElMessage.error('获取可用接口列表失败');
            }
        };

        // 获取环境标签
        const getEnvLabel = (value) => {
            const option = envOptions.find(item => item.value === value);
            return option ? option.label : value;
        };

        // 格式化日期
        const formatDate = (dateStr) => {
            if (!dateStr) return '';
            const date = new Date(dateStr);
            return date.toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            }).replace(/\//g, '-');
        };

        // 搜索
        const handleSearch = () => {
            config.page = 1;
            getCaseList();
        };

        // 重置搜索
        const resetSearch = () => {
            formInline.env = '';
            formInline.business = '';
            formInline.name = '';
            config.page = 1;
            getCaseList();
        };

        // 分页变化
        const changePage = (page) => {
            config.page = page;
            getCaseList();
        };

        // 新增用例
        const handleAdd = () => {
            Object.keys(formCase).forEach(key => {
                if (Array.isArray(formCase[key])) {
                    formCase[key] = [];
                } else if (typeof formCase[key] === 'object') {
                    formCase[key] = {};
                } else {
                    formCase[key] = '';
                }
            });
            drawerVisible.value = true;
        };

        // 编辑用例
        const handleEdit = (row) => {
            Object.assign(formCase, row);
            drawerVisible.value = true;
        };

        // 调试用例
        const handleDebug = async (row) => {
            try {
                const res = await proxy.$api.debugTestCase(row.id);
                if (res.code === 200) {
                    ElMessage.success('调试成功');
                } else {
                    ElMessage.error(res.msg || '调试失败');
                }
            } catch (error) {
                ElMessage.error('调试失败');
            }
        };

        // 执行用例
        const handleExecute = async (row) => {
            try {
                const res = await proxy.$api.executeTestCase(row.id);
                if (res.code === 200) {
                    ElMessage.success('执行成功');
                } else {
                    ElMessage.error(res.msg || '执行失败');
                }
            } catch (error) {
                ElMessage.error('执行失败');
            }
        };

        // 删除用例
        const handleDelete = (row) => {
            ElMessageBox.confirm('确认删除该用例？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                try {
                    const res = await proxy.$api.deleteTestCase(row.id);
                    if (res.code === 200) {
                        ElMessage.success('删除成功');
                        getCaseList();
                    } else {
                        ElMessage.error(res.msg || '删除失败');
                    }
                } catch (error) {
                    ElMessage.error('删除失败');
                }
            });
        };

        // 添加接口
        const handleAddApi = () => {
            if (!formCase.env) {
                ElMessage.warning('请先选择环境');
                return;
            }
            // 获取可选接口列表
            getAvailableApis();
            // 打开选择接口对话框
            apiDialogVisible.value = true;
        };

        // 确认添加选中的接口
        const confirmAddApis = () => {
            if (selectedApis.value.length === 0) {
                ElMessage.warning('请选择要添加的接口');
                return;
            }

            // 将选中的接口添加到列表中
            selectedApis.value.forEach(api => {
                formCase.api_list.push({
                    api_id: api.id,
                    api_name: api.api_name,
                    api_path: api.api_path,
                    req_method: api.req_method,
                    req_header: api.req_header || '',
                    req_body: api.req_body || '',
                    assert_body: '',
                    extract_value: ''
                });
            });

            // 清空选中状态并关闭对话框
            selectedApis.value = [];
            apiDialogVisible.value = false;
        };

        // 选择接口后的处理
        const handleApiSelect = async (apiId, index) => {
            try {
                const res = await proxy.$api.getApiDetail(apiId);
                if (res.code === 200) {
                    const apiData = res.data;
                    // 更新当前行的数据
                    formCase.api_list[index] = {
                        api_id: apiId,
                        api_name: apiData.api_name,
                        api_path: apiData.api_path,
                        req_method: apiData.req_method,
                        req_header: apiData.req_header || '',
                        req_body: apiData.req_body || '',
                        assert_body: '',
                        extract_value: ''
                    };
                }
            } catch (error) {
                ElMessage.error('获取接口详情失败');
                formCase.api_list.splice(index, 1);
            }
        };

        // 格式化JSON
        const formatJson = (value) => {
            if (!value) return '';
            try {
                if (typeof value === 'string') {
                    return JSON.stringify(JSON.parse(value), null, 2);
                }
                return JSON.stringify(value, null, 2);
            } catch (e) {
                return value;
            }
        };

        // 配置接口
        const handleConfigApi = (api, index) => {
            currentApiIndex.value = index;
            Object.assign(currentApiConfig, {
                req_header: api.req_header || '',
                req_body: api.req_body || '',
                assert_body: api.assert_body || '',
                extract_value: api.extract_value || ''
            });
            configDialogVisible.value = true;
        };

        // 保存接口配置
        const saveApiConfig = () => {
            if (currentApiIndex.value > -1) {
                const currentApi = formCase.api_list[currentApiIndex.value];
                Object.assign(currentApi, {
                    req_header: currentApiConfig.req_header,
                    req_body: currentApiConfig.req_body,
                    assert_body: currentApiConfig.assert_body,
                    extract_value: currentApiConfig.extract_value
                });
            }
            configDialogVisible.value = false;
        };

        // 提交表单
        const onSubmit = () => {
            proxy.$refs.caseForm.validate(async (valid) => {
                if (valid) {
                    submitLoading.value = true;
                    try {
                        const submitData = { ...formCase };
                        const res = formCase.id
                            ? await proxy.$api.updateTestCase(formCase.id, submitData)
                            : await proxy.$api.createTestCase(submitData);
                        
                        if (res.code === 200) {
                            ElMessage.success(formCase.id ? '更新成功' : '创建成功');
                            drawerVisible.value = false;
                            getCaseList();
                        } else {
                            ElMessage.error(res.msg || (formCase.id ? '更新失败' : '创建失败'));
                        }
                    } catch (error) {
                        ElMessage.error(formCase.id ? '更新失败' : '创建失败');
                    } finally {
                        submitLoading.value = false;
                    }
                }
            });
        };

        // 移除接口
        const handleRemoveApi = (index) => {
            formCase.api_list.splice(index, 1);
        };

        // 监听环境变化
        watch(() => formCase.env, (newVal) => {
            if (newVal) {
                getAccountList();
            }
        });

        // 处理表格选择变化
        const handleSelectionChange = (selection) => {
            selectedApis.value = selection;
        };

        onMounted(() => {
            getCaseList();
        });

        return {
            caseList,
            envOptions,
            accountOptions,
            config,
            drawerVisible,
            apiDialogVisible,
            configDialogVisible,
            formInline,
            formCase,
            apiSearchForm,
            currentApiConfig,
            availableApis,
            submitLoading,
            loading,
            formRules,
            drawerTitle,
            configActiveTab,
            getEnvLabel,
            formatDate,
            handleSearch,
            resetSearch,
            changePage,
            handleAdd,
            handleEdit,
            handleDebug,
            handleExecute,
            handleDelete,
            handleAddApi,
            getAvailableApis,
            handleRemoveApi,
            handleConfigApi,
            saveApiConfig,
            onSubmit,
            handleSelectionChange,
            confirmAddApis,
            formatJson
        };
    }
});
</script>

<style lang="less" scoped>
.case-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.table {
    position: relative;
    height: 520px;

    .pager {
        position: absolute;
        right: 0;
        bottom: -20px;
    }
}

.api-list-section {
    margin: 20px 0;
    padding: 20px;
    background-color: #f5f7fa;
    border-radius: 4px;

    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;

        h3 {
            margin: 0;
        }
    }
}

.drawer-footer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 20px;
    background-color: #fff;
    text-align: right;
    border-top: 1px solid #e4e7ed;
}

:deep(.el-drawer__body) {
    padding: 20px;
    padding-bottom: 80px;
}

pre {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 4px;
    margin: 0;
    white-space: pre-wrap;
    word-wrap: break-word;
}

:deep(.el-table) {
    .el-select {
        width: 100%;
    }
}

:deep(.el-tooltip__trigger) {
    display: inline-block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>


