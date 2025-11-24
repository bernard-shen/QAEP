<template>
    <div>
        <div class="env-header">
            <el-button type="primary" @click="handleAdd">+新增环境</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="环境">
                    <el-select v-model="formInline.env" placeholder="请选择环境" clearable>
                        <el-option v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="业务">
                    <el-input v-model="formInline.business" placeholder="请输入业务名称" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                    <el-button @click="resetSearch">重置</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div class="table">
            <el-table :data="envList" style="width: 100%" height="500px" border v-loading="loading">
                <el-table-column prop="business" label="所属业务" width="120" />
                <el-table-column prop="env" label="环境" width="100">
                    <template #default="scope">
                        {{ getEnvLabel(scope.row.env) }}
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="环境名称" width="150" />
                <el-table-column prop="domain" label="域名" min-width="200" show-overflow-tooltip />
                <el-table-column prop="update_time" label="更新时间" width="160">
                    <template #default="scope">
                        {{ formatDate(scope.row.update_time) }}
                    </template>
                </el-table-column>
                <el-table-column fixed="right" label="操作" width="200">
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" background layout="total, prev, pager, next" :total="config.total"
                :page-size="config.pageSize" @current-change="changePage" />
        </div>

        <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px" :before-close="handleClose">
            <el-form :model="formEnv" ref="envForm" label-width="100px" :rules="formRules">
                <el-form-item label="所属业务" prop="business">
                    <el-input v-model="formEnv.business" placeholder="请输入所属业务" />
                </el-form-item>
                <el-form-item label="环境" prop="env">
                    <el-select v-model="formEnv.env" placeholder="请选择环境">
                        <el-option v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="环境名称" prop="name">
                    <el-input v-model="formEnv.name" placeholder="请输入环境名称" />
                </el-form-item>
                <el-form-item label="域名" prop="domain">
                    <el-input v-model="formEnv.domain" placeholder="请输入域名地址" />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleCancel">取消</el-button>
                    <el-button type="primary" @click="onSubmit" :loading="submitLoading">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted, getCurrentInstance, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default defineComponent({
    name: 'EnvMng',
    setup() {
        const { proxy } = getCurrentInstance();
        
        // 调试代码
        console.log('API对象:', proxy.$api);
        if (!proxy.$api || !proxy.$api.getEnvironments) {
            console.error('API方法未正确注册');
        }
        
        const envList = ref([]);
        const dialogVisible = ref(false);
        const submitLoading = ref(false);
        const loading = ref(false);

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
            business: ''
        });

        // 新增/编辑表单
        const formEnv = reactive({
            business: '',
            env: '',
            name: '',
            domain: ''
        });

        // 表单验证规则
        const formRules = {
            business: [{ required: true, message: '请输入所属业务', trigger: 'blur' }],
            env: [{ required: true, message: '请选择环境', trigger: 'change' }],
            name: [{ required: true, message: '请输入环境名称', trigger: 'blur' }],
            domain: [{ required: true, message: '请输入域名地址', trigger: 'blur' }]
        };

        const dialogTitle = computed(() => {
            const currentRow = envList.value.find(item => item.business === formEnv.business && 
                item.env === formEnv.env && item.name === formEnv.name);
            return currentRow ? '编辑环境' : '新增环境';
        });

        // 获取环境列表
        const getEnvList = async () => {
            loading.value = true;
            try {
                const params = {
                    page: config.page,
                    page_size: config.pageSize,
                    ...(formInline.env && { env: formInline.env }),
                    ...(formInline.business && { business: formInline.business })
                };
                
                const res = await proxy.$api.getEnvironments(params);
                if (res.code === 200) {
                    envList.value = res.data;
                    config.total = res.total;
                    config.totalPages = res.total_pages;
                } else {
                    ElMessage.error(res.msg || '获取环境列表失败');
                }
            } catch (error) {
                console.error('获取环境列表失败:', error);
                ElMessage.error('获取环境列表失败');
            } finally {
                loading.value = false;
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
            getEnvList();
        };

        // 重置搜索
        const resetSearch = () => {
            formInline.env = '';
            formInline.business = '';
            config.page = 1;
            getEnvList();
        };

        // 分页变化
        const changePage = (page) => {
            config.page = page;
            getEnvList();
        };

        // 新增环境
        const handleAdd = () => {
            Object.keys(formEnv).forEach(key => formEnv[key] = '');
            dialogVisible.value = true;
        };

        // 编辑环境
        const handleEdit = (row) => {
            const { business, env, name, domain } = row;
            Object.assign(formEnv, { business, env, name, domain });
            dialogVisible.value = true;
        };

        // 删除环境
        const handleDelete = (row) => {
            ElMessageBox.confirm('确认删除该环境配置？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                try {
                    const res = await proxy.$api.deleteEnvironment(row.id);
                    if (res.code === 200) {
                        ElMessage.success('删除成功');
                        getEnvList();
                    } else {
                        ElMessage.error(res.msg || '删除失败');
                    }
                } catch (error) {
                    ElMessage.error('删除失败');
                }
            });
        };

        // 提交表单
        const onSubmit = () => {
            proxy.$refs.envForm.validate(async (valid) => {
                if (valid) {
                    submitLoading.value = true;
                    try {
                        const currentRow = envList.value.find(item => item.business === formEnv.business && 
                            item.env === formEnv.env && item.name === formEnv.name);
                        
                        const res = currentRow
                            ? await proxy.$api.updateEnvironment(currentRow.id, formEnv)
                            : await proxy.$api.createEnvironment(formEnv);
                        
                        if (res.code === 200) {
                            ElMessage.success(currentRow ? '更新成功' : '创建成功');
                            dialogVisible.value = false;
                            getEnvList();
                        } else {
                            ElMessage.error(res.msg || (currentRow ? '更新失败' : '创建失败'));
                        }
                    } catch (error) {
                        ElMessage.error(currentRow ? '更新失败' : '创建失败');
                    } finally {
                        submitLoading.value = false;
                    }
                }
            });
        };

        // 取消
        const handleCancel = () => {
            dialogVisible.value = false;
            proxy.$refs.envForm.resetFields();
        };

        // 关闭对话框
        const handleClose = (done) => {
            ElMessageBox.confirm('确认关闭？未保存的内容将会丢失')
                .then(() => {
                    proxy.$refs.envForm.resetFields();
                    done();
                })
                .catch(() => {});
        };

        onMounted(() => {
            getEnvList();
        });

        return {
            envList,
            envOptions,
            config,
            dialogVisible,
            formInline,
            formEnv,
            submitLoading,
            formRules,
            dialogTitle,
            loading,
            getEnvLabel,
            formatDate,
            handleSearch,
            resetSearch,
            changePage,
            handleAdd,
            handleEdit,
            handleDelete,
            handleCancel,
            handleClose,
            onSubmit
        };
    }
});
</script>

<style lang="less" scoped>
.env-header {
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
</style> 