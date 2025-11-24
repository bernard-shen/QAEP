<template>
    <div>
        <div class="account-header">
            <el-button type="primary" @click="handleAdd">+新增账号</el-button>
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
            <el-table :data="accountList" style="width: 100%" height="500px" border v-loading="loading">
                <el-table-column prop="business" label="所属业务" width="120" />
                <el-table-column prop="env" label="环境" width="100">
                    <template #default="scope">
                        {{ getEnvLabel(scope.row.env) }}
                    </template>
                </el-table-column>
                <el-table-column prop="username" label="用户名" width="150" />
                <el-table-column prop="remark" label="备注" min-width="200" show-overflow-tooltip />
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
            <el-form :model="formAccount" ref="accountForm" label-width="100px" :rules="formRules">
                <el-form-item label="所属业务" prop="business">
                    <el-input v-model="formAccount.business" placeholder="请输入所属业务" />
                </el-form-item>
                <el-form-item label="环境" prop="env">
                    <el-select v-model="formAccount.env" placeholder="请选择环境">
                        <el-option v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-form-item>
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="formAccount.username" placeholder="请输入用户名" />
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="formAccount.password" type="password" placeholder="请输入密码" 
                        :required="!formAccount.id"/>
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
    name: 'AccountMng',
    setup() {
        const { proxy } = getCurrentInstance();
        const accountList = ref([]);
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
        const formAccount = reactive({
            business: '',
            env: '',
            username: '',
            password: ''
        });

        // 表单验证规则
        const formRules = {
            business: [{ required: true, message: '请输入所属业务', trigger: 'blur' }],
            env: [{ required: true, message: '请选择环境', trigger: 'change' }],
            username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
            password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
        };

        const dialogTitle = computed(() => {
            const currentRow = accountList.value.find(item => 
                item.business === formAccount.business && 
                item.env === formAccount.env && 
                item.username === formAccount.username
            );
            return currentRow ? '编辑账号' : '新增账号';
        });

        // 获取账号列表
        const getAccountList = async () => {
            loading.value = true;
            try {
                const params = {
                    page: config.page,
                    page_size: config.pageSize,
                    ...(formInline.env && { env: formInline.env }),
                    ...(formInline.business && { business: formInline.business })
                };
                
                const res = await proxy.$api.getAccounts(params);
                if (res.code === 200) {
                    accountList.value = res.data;
                    config.total = res.total;
                    config.totalPages = res.total_pages;
                } else {
                    ElMessage.error(res.msg || '获取账号列表失败');
                }
            } catch (error) {
                console.error('获取账号列表失败:', error);
                ElMessage.error('获取账号列表失败');
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
            getAccountList();
        };

        // 重置搜索
        const resetSearch = () => {
            formInline.env = '';
            formInline.business = '';
            config.page = 1;
            getAccountList();
        };

        // 分页变化
        const changePage = (page) => {
            config.page = page;
            getAccountList();
        };

        // 新增账号
        const handleAdd = () => {
            Object.keys(formAccount).forEach(key => formAccount[key] = '');
            dialogVisible.value = true;
        };

        // 编辑账号
        const handleEdit = (row) => {
            const { business, env, username } = row;
            Object.assign(formAccount, { 
                business, 
                env, 
                username,
                password: '' // 编辑时不显示密码
            });
            dialogVisible.value = true;
        };

        // 删除账号
        const handleDelete = (row) => {
            ElMessageBox.confirm('确认删除该账号？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                try {
                    const res = await proxy.$api.deleteAccount(row.id);
                    if (res.code === 200) {
                        ElMessage.success('删除成功');
                        getAccountList();
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
            proxy.$refs.accountForm.validate(async (valid) => {
                if (valid) {
                    submitLoading.value = true;
                    try {
                        const currentRow = accountList.value.find(item => 
                            item.business === formAccount.business && 
                            item.env === formAccount.env && 
                            item.username === formAccount.username
                        );
                        
                        // 如果是编辑且没有修改密码，则不传密码字段
                        const submitData = { ...formAccount };
                        if (currentRow && !submitData.password) {
                            delete submitData.password;
                        }

                        const res = currentRow
                            ? await proxy.$api.updateAccount(currentRow.id, submitData)
                            : await proxy.$api.createAccount(submitData);
                        
                        if (res.code === 200) {
                            ElMessage.success(currentRow ? '更新成功' : '创建成功');
                            dialogVisible.value = false;
                            getAccountList();
                        } else {
                            ElMessage.error(res.msg || (currentRow ? '更新失败' : '创建失败'));
                        }
                    } catch (error) {
                        console.error('提交失败:', error);
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
            proxy.$refs.accountForm.resetFields();
        };

        // 关闭对话框
        const handleClose = (done) => {
            ElMessageBox.confirm('确认关闭？未保存的内容将会丢失')
                .then(() => {
                    proxy.$refs.accountForm.resetFields();
                    done();
                })
                .catch(() => {});
        };

        onMounted(() => {
            getAccountList();
        });

        return {
            accountList,
            envOptions,
            config,
            dialogVisible,
            formInline,
            formAccount,
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
.account-header {
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