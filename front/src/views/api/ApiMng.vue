<template>
    <div>
        <div class="api-header">
            <el-button type="primary" @click="handleAdd">+新增接口</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="环境">
                    <el-select v-model="formInline.env" placeholder="请选择环境" clearable>
                        <el-option v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="业务">
                    <el-input v-model="formInline.business" placeholder="请输入业务名称" clearable />
                </el-form-item>
                <el-form-item label="接口名称">
                    <el-input v-model="formInline.api_name" placeholder="请输入接口名称" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                    <el-button @click="resetSearch">重置</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div class="table">
            <el-table :data="apiList" style="width: 100%" height="500px" border v-loading="loading">
                <el-table-column v-for="item in tableLabel" 
                    :key="item.prop" 
                    :label="item.label" 
                    :prop="item.prop" 
                    :width="item.width"
                    :show-overflow-tooltip="item.showOverflowTooltip">
                    <template #default="scope" v-if="item.prop === 'env'">
                        {{ getEnvLabel(scope.row.env) }}
                    </template>
                    <template #default="scope" v-else-if="item.prop === 'body_type'">
                        {{ getBodyTypeLabel(scope.row.body_type) }}
                    </template>
                </el-table-column>
                <el-table-column fixed="right" label="操作" width="200">
                    <template #default="scope">
                        <el-button size="small" @click="handleView(scope.row)">查看</el-button>
                        <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" background layout="total, prev, pager, next" :total="config.total"
                :page-size="config.pageSize" @current-change="changePage" />
        </div>

        <el-dialog v-model="dialogVisible" :title="dialogTitle" width="70%" :before-close="handleClose">
            <el-form :model="formApi" ref="apiForm" label-width="120px" :rules="formRules">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="环境" prop="env">
                            <el-select v-model="formApi.env" placeholder="请选择环境">
                                <el-option v-for="item in envOptions" :key="item.value" :label="item.label"
                                    :value="item.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="所属业务" prop="of_business">
                            <el-input v-model="formApi.of_business" placeholder="请输入所属业务" />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="域名地址" prop="host">
                            <el-input v-model="formApi.host" placeholder="请输入域名地址" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="接口名称" prop="api_name">
                            <el-input v-model="formApi.api_name" placeholder="请输入接口名称" />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="接口路径" prop="api_path">
                            <el-input v-model="formApi.api_path" placeholder="请输入接口路径" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="请求方法" prop="req_method">
                            <el-select v-model="formApi.req_method" placeholder="请选择请求方法">
                                <el-option label="GET" value="GET" />
                                <el-option label="POST" value="POST" />
                                <el-option label="PUT" value="PUT" />
                                <el-option label="DELETE" value="DELETE" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item label="请求体类型" prop="body_type">
                            <el-select v-model="formApi.body_type" placeholder="请选择请求体类型">
                                <el-option v-for="item in bodyTypeOptions" :key="item.value" :label="item.label"
                                    :value="item.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-form-item label="请求头" prop="req_header">
                    <el-input type="textarea" v-model="formApi.req_header" :rows="4" placeholder="请输入请求头（JSON格式）" />
                </el-form-item>

                <el-form-item label="请求参数" prop="req_params">
                    <el-input type="textarea" v-model="formApi.req_params" :rows="4" placeholder="请输入请求参数（JSON格式）" />
                </el-form-item>

                <el-form-item label="请求体" prop="req_body">
                    <el-input type="textarea" v-model="formApi.req_body" :rows="4" placeholder="请输入请求体（JSON格式）" />
                </el-form-item>

                <el-form-item label="响应示例" prop="resp_demo">
                    <el-input type="textarea" v-model="formApi.resp_demo" :rows="4" placeholder="请输入响应示例（JSON格式）" />
                </el-form-item>

                <el-form-item label="提取值" prop="extr_value">
                    <el-input type="textarea" v-model="formApi.extr_value" :rows="3" placeholder="请输入需要提取的值" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleCancel">取消</el-button>
                    <el-button type="primary" @click="onSubmit" :loading="submitLoading">确定</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- 查看详情弹窗 -->
        <el-dialog v-model="viewDialogVisible" title="接口详情" width="70%">
            <el-descriptions :column="2" border>
                <el-descriptions-item label="环境">{{ getEnvLabel(viewData.env) }}</el-descriptions-item>
                <el-descriptions-item label="所属业务">{{ viewData.of_business }}</el-descriptions-item>
                <el-descriptions-item label="域名地址">{{ viewData.host }}</el-descriptions-item>
                <el-descriptions-item label="接口名称">{{ viewData.api_name }}</el-descriptions-item>
                <el-descriptions-item label="接口路径">{{ viewData.api_path }}</el-descriptions-item>
                <el-descriptions-item label="请求方法">{{ viewData.req_method }}</el-descriptions-item>
                <el-descriptions-item label="请求体类型">{{ getBodyTypeLabel(viewData.body_type) }}</el-descriptions-item>
                <el-descriptions-item label="创建时间">{{ viewData.create_time }}</el-descriptions-item>
            </el-descriptions>
            <el-divider />
            <el-tabs v-model="activeTab">
                <el-tab-pane label="请求头" name="header">
                    <pre>{{ formatJson(viewData.req_header) }}</pre>
                </el-tab-pane>
                <el-tab-pane label="请求参数" name="params">
                    <pre>{{ formatJson(viewData.req_params) }}</pre>
                </el-tab-pane>
                <el-tab-pane label="请求体" name="body">
                    <pre>{{ formatJson(viewData.req_body) }}</pre>
                </el-tab-pane>
                <el-tab-pane label="响应示例" name="response">
                    <pre>{{ formatJson(viewData.resp_demo) }}</pre>
                </el-tab-pane>
                <el-tab-pane label="提取值" name="extract">
                    <pre>{{ viewData.extr_value }}</pre>
                </el-tab-pane>
            </el-tabs>
        </el-dialog>
    </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted, getCurrentInstance, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default defineComponent({
    name: 'ApiMng',
    setup() {
        const { proxy } = getCurrentInstance();
        const apiList = ref([]);
        const dialogVisible = ref(false);
        const viewDialogVisible = ref(false);
        const submitLoading = ref(false);
        const activeTab = ref('header');
        const loading = ref(false);

        // 环境选项
        const envOptions = [
            { value: 'TEST', label: '测试环境' },
            { value: 'DEV', label: '开发环境' },
            { value: 'PROD', label: '生产环境' }
        ];

        // 请求体类型选项
        const bodyTypeOptions = [
            { value: 'FORM', label: 'Form表单' },
            { value: 'JSON', label: 'JSON' },
            { value: 'XML', label: 'XML' },
            { value: 'TEXT', label: '纯文本' }
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
            api_name: ''
        });

        // 新增/编辑表单
        const formApi = reactive({
            id: '',
            env: '',
            of_business: '',
            host: '',
            api_name: '',
            api_path: '',
            req_method: '',
            body_type: '',
            req_header: '',
            req_params: '',
            req_body: '',
            resp_demo: '',
            extr_value: ''
        });

        // 查看详情数据
        const viewData = reactive({
            env: '',
            of_business: '',
            host: '',
            api_name: '',
            api_path: '',
            req_method: '',
            body_type: '',
            req_header: '',
            req_params: '',
            req_body: '',
            resp_demo: '',
            extr_value: '',
            create_time: ''
        });

        // 表单验证规则
        const formRules = {
            env: [{ required: true, message: '请选择环境', trigger: 'change' }],
            of_business: [{ required: true, message: '请输入所属业务', trigger: 'blur' }],
            host: [{ required: true, message: '请输入域名地址', trigger: 'blur' }],
            api_name: [{ required: true, message: '请输入接口名称', trigger: 'blur' }],
            api_path: [{ required: true, message: '请输入接口路径', trigger: 'blur' }],
            req_method: [{ required: true, message: '请选择请求方法', trigger: 'change' }],
            body_type: [{ required: true, message: '请选择请求体类型', trigger: 'change' }]
        };

        // 表格列定义
        const formatTableJson = (value) => {
            try {
                if (!value) return '';
                const parsed = JSON.parse(value);
                return JSON.stringify(parsed, null, 2)  // 使用2个空格缩进
                    .replace(/\\n/g, '\n')  // 处理换行符
                    .replace(/\\"/g, '"');  // 处理引号
            } catch (e) {
                return value || '';
            }
        };

        const tableLabel = [
            { prop: "of_business", label: "所属业务", width: 120 },
            { prop: "env", label: "环境", width: 100 },
            { prop: "host", label: "域名地址", width: 180, showOverflowTooltip: true },
            { prop: "api_name", label: "接口名称", width: 160, showOverflowTooltip: true },
            { prop: "api_path", label: "接口路径", width: 200, showOverflowTooltip: true },
            { prop: "req_method", label: "请求方法", width: 100 },
            { 
                prop: "req_header", 
                label: "请求头", 
                width: 150, 
                showOverflowTooltip: true,
                formatter: (row) => formatTableJson(row.req_header)
            },
            { 
                prop: "req_body", 
                label: "请求体", 
                width: 150,
                showOverflowTooltip: true,
                formatter: (row) => formatTableJson(row.req_body)
            },
            { prop: "body_type", label: "请求体类型", width: 120 },
            { 
                prop: "req_params", 
                label: "请求参数", 
                width: 150, 
                showOverflowTooltip: true,
                formatter: (row) => formatTableJson(row.req_params)
            },
            { 
                prop: "extr_value", 
                label: "提取值", 
                width: 150, 
                showOverflowTooltip: true,
                formatter: (row) => formatTableJson(row.extr_value)
            },
            { 
                prop: "update_time", 
                label: "更新时间", 
                width: 160,
                formatter: (row) => {
                    if (!row.update_time) return '';
                    const date = new Date(row.update_time);
                    return date.toLocaleString('zh-CN', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit'
                    }).replace(/\//g, '-');
                }
            }
        ];

        // 在 setup 函数中添加
        const dialogTitle = computed(() => formApi.id ? '编辑接口' : '新增接口');

        // 获取接口列表
        const getApiList = async () => {
            loading.value = true;
            try {
                const params = {
                    page: config.page,
                    page_size: config.pageSize,
                    ...(formInline.env && { env: formInline.env }),
                    ...(formInline.business && { of_business: formInline.business }),
                    ...(formInline.api_name && { api_name: formInline.api_name })
                };
                
                const res = await proxy.$api.getApiList(params);
                if (res.code === 200) {
                    apiList.value = res.data;
                    config.total = res.total;
                    config.totalPages = res.total_pages;
                } else {
                    ElMessage.error(res.msg || '获取接口列表失败');
                }
            } catch (error) {
                console.error('获取接口列表失败:', error);
                ElMessage.error('获取接口列表失败');
            } finally {
                loading.value = false;
            }
        };

        // 获取环境标签
        const getEnvLabel = (value) => {
            const option = envOptions.find(item => item.value === value);
            return option ? option.label : value;
        };

        // 获取请求体类型标签
        const getBodyTypeLabel = (value) => {
            const option = bodyTypeOptions.find(item => item.value === value);
            return option ? option.label : value;
        };

        // 格式化JSON
        const formatJson = (value) => {
            try {
                return value ? JSON.stringify(JSON.parse(value), null, 2) : '';
            } catch (e) {
                return value;
            }
        };

        // 搜索
        const handleSearch = () => {
            config.page = 1;
            getApiList();
        };

        // 重置搜索
        const resetSearch = () => {
            formInline.env = '';
            formInline.business = '';
            formInline.api_name = '';
            config.page = 1;
            getApiList();
        };

        // 分页变化
        const changePage = (page) => {
            config.page = page;
            getApiList();
        };

        // 新增接口
        const handleAdd = () => {
            Object.keys(formApi).forEach(key => formApi[key] = '');
            dialogVisible.value = true;
        };

        // 编辑接口
        const handleEdit = async (row) => {
            try {
                const res = await proxy.$api.getApiDetail(row.id);
                if (res.code === 200) {
                    // 清空表单
                    Object.keys(formApi).forEach(key => formApi[key] = '');
                    // 使用接口返回的数据更新表单
                    Object.assign(formApi, res.data);
                    // 打开弹窗
                    dialogVisible.value = true;
                } else {
                    ElMessage.error(res.msg || '获取接口详情失败');
                }
            } catch (error) {
                console.error('获取接口详情失败:', error);
                ElMessage.error('获取接口详情失败');
            }
        };

        // 查看详情
        const handleView = async (row) => {
            try {
                const res = await proxy.$api.getApiDetail(row.id);
                if (res.code === 200) {
                    // 清空数据
                    Object.keys(viewData).forEach(key => viewData[key] = '');
                    // 使用接口返回的数据更新视图
                    Object.assign(viewData, res.data);
                    viewDialogVisible.value = true;
                } else {
                    ElMessage.error(res.msg || '获取接口详情失败');
                }
            } catch (error) {
                console.error('获取接口详情失败:', error);
                ElMessage.error('获取接口详情失败');
            }
        };

        // 删除接口
        const handleDelete = (row) => {
            ElMessageBox.confirm('确认删除该接口？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                try {
                    await proxy.$api.deleteApi(row.id);
                    ElMessage.success('删除成功');
                    getApiList();
                } catch (error) {
                    ElMessage.error('删除失败');
                }
            });
        };

        // 提交表单
        const onSubmit = () => {
            proxy.$refs.apiForm.validate(async (valid) => {
                if (valid) {
                    submitLoading.value = true;
                    try {
                        if (formApi.id) {
                            await proxy.$api.updateApi(formApi.id, formApi);
                            ElMessage.success('更新成功');
                        } else {
                            await proxy.$api.createApi(formApi);
                            ElMessage.success('创建成功');
                        }
                        dialogVisible.value = false;
                        getApiList();
                    } catch (error) {
                        ElMessage.error(formApi.id ? '更新失败' : '创建失败');
                    } finally {
                        submitLoading.value = false;
                    }
                }
            });
        };

        // 取消
        const handleCancel = () => {
            dialogVisible.value = false;
            proxy.$refs.apiForm.resetFields();
        };

        // 关闭对话框
        const handleClose = (done) => {
            ElMessageBox.confirm('确认关闭？未保存的内容将会丢失')
                .then(() => {
                    proxy.$refs.apiForm.resetFields();
                    done();
                })
                .catch(() => {});
        };

        onMounted(() => {
            getApiList();
        });

        return {
            apiList,
            envOptions,
            bodyTypeOptions,
            config,
            dialogVisible,
            viewDialogVisible,
            formInline,
            formApi,
            viewData,
            activeTab,
            submitLoading,
            formRules,
            dialogTitle,
            getEnvLabel,
            getBodyTypeLabel,
            formatJson,
            handleSearch,
            resetSearch,
            changePage,
            handleAdd,
            handleEdit,
            handleView,
            handleDelete,
            handleCancel,
            handleClose,
            onSubmit,
            loading,
            tableLabel
        };
    }
});
</script>

<style lang="less" scoped>
.api-header {
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

:deep(.el-descriptions) {
    margin-bottom: 20px;
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
    .el-tooltip__trigger {
        max-width: 500px;  // 减小tooltip最大宽度
        white-space: pre-wrap !important;
    }
}

:deep(.el-popper) {
    max-width: 400px !important;  // 减小弹出框最大宽度
    white-space: pre-wrap !important;
    word-break: break-all;
    line-height: 1.5;
    font-family: monospace;
    
    .el-popper__content {
        padding: 12px;
        background: #f8f9fa;
        border-radius: 4px;
        font-size: 12px;  // 稍微减小字体大小
    }
}
</style> 