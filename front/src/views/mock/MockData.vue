<template>
    <div>
        <div class="user-header">
            <el-button type="primary" @click="handleAdd">+新增</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="连接名">
                    <el-input v-model="formInline.connect_name" placeholder="请输入连接名" clearable />
                </el-form-item>
                <el-form-item label="sql类型">
                    <el-select v-model="formInline.sql_type" placeholder="请选择sql类型" clearable>
                        <el-option v-for="sqlItem in sql_list" :key="sqlItem.name" :label="sqlItem.name"
                            :value="sqlItem.value" />
                    </el-select>
                    <!-- <el-input v-model="formInline.keyword" placeholder="请输入sql类型" clearable /> -->
                </el-form-item>
                <el-form-item label="连接地址">
                    <el-input v-model="formInline.host" placeholder="请输入连接地址" clearable />
                </el-form-item>
                <el-form-item label="连接状态">
                    <el-select v-model="formInline.connect_status" placeholder="请选择连接状态" clearable>
                        <el-option v-for="statusItem in status_list" :key="statusItem.name" :label="statusItem.name"
                            :value="statusItem.value" />
                    </el-select>
                    <!-- <el-input v-model="formInline.keyword" placeholder="请输入连接状态" clearable /> -->
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="table">
            <el-table :data="list" style="width: 100%" height="500px">
                <el-table-column v-for="item in tableLabel" :key="item.prop" :label="item.label" :prop="item.prop"
                    :min-width="item.width ? item.width : 125" :formatter="item.formatter" />
                <el-table-column fixed="right" label="操作" width="320" class="operation">
                    <!-- 通过scope插槽获取待编辑数据 -->
                    <template #default="scope">
                        <el-button size="small" @click="handleTestConnect(scope.row)">测试连接</el-button>
                        <el-button size="small" @click="handleMockData(scope.row)">一键造数</el-button>
                        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button type="primary" size="small" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" background layout="prev, pager, next" :total="config.total"
                @current-change="changePage" />
        </div>
        <el-dialog v-model="dialogVisible" :title="action == 'add' ? '新增连接' : '编辑连接'" width="40%"
            :before-close="handleClose">
            <el-form :inline="true" :model="formUser" ref="userForm">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="连接名称" prop="connect_name" :rules="[
                            { required: true, message: '请输入连接名', trigger: 'blur' },
                            { min: 3, max: 20, message: '连接名长度在3~20之间', trigger: 'blur' },]">
                            <el-input v-model="formUser.connect_name" placeholder="请输入连接名" clearable />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="类型" prop="sql_type" :rules="[
                            { required: true, message: '请输入sql类型', trigger: 'blur' },]">
                            <el-select v-model="formUser.sql_type" placeholder="请输入sql类型" clearable>
                                <el-option v-for="sqlItem in sql_list" :key="sqlItem.name" :label="sqlItem.sqlItem"
                                    :value="sqlItem.value" />
                            </el-select>
                            <!-- <el-input v-model="formUser.sql_type" placeholder="请输入sql类型" clearable /> -->
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="连接地址" prop="host" :rules="[
                            { required: true, message: '请输入连接地址', trigger: 'blur' }]">
                            <el-input v-model="formUser.host" placeholder="请输入连接地址" clearable />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="端口" prop="port" :rules="[
                            { required: true, message: '请输入端口号', trigger: 'blur' },]">
                            <el-input-number v-model="formUser.port" placeholder="请输入端口号" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row>
                    <el-col :span="12">
                        <el-form-item label="数据库名" prop="db" :rules="[
                            { required: true, message: '请输入数据库名称', trigger: 'blur' }]">
                            <el-input v-model="formUser.db" placeholder="请输入数据库名称" clearable />
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="用户" prop="username" :rules="[
                            { required: true, message: '请输入用户名', trigger: 'blur' }]">
                            <el-input v-model="formUser.username" placeholder="请输入用户名" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row>
                    <el-form-item label="用户密码" prop="password" :rules="[
                        { required: true, message: '请输入用户密码', trigger: 'blur' }]">
                        <el-input 
                            v-model="formUser.password" 
                            type="password"
                            placeholder="请输入用户密码" 
                            show-password
                            clearable 
                        />
                    </el-form-item>
                    <el-col :span="12">
                        <el-form-item label="创建时间" prop="date" :rules="[
                            { required: false }]">
                            <el-date-picker v-model="formUser.date" type="date" placeholder="请选择时间" clearable
                                value-format="YYYY-MM-DD" />
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleCancel">取消</el-button>
                    <el-button type="primary" @click="onSubmit">确定</el-button>
                </span>
            </template>
        </el-dialog>
        <el-dialog v-model="mockDialogVisible" title="一键造数" width="40%" :before-close="handleClose1">
            <el-form :inline="true" :model="formMock" ref="mockForm">
                <el-row style="margin-left: 15px;">
                    <el-col :span="12">
                        <!-- prop="dbname" -->
                        <el-form-item label="指定库名">
                            <el-select v-model="formMock.dbname" placeholder="请输入或选择库名" filterable allow-create clearable
                                @change="handleVisibleChange">
                                <el-option v-for="choiceItem in db_list" :key="choiceItem.name" :label="choiceItem.name"
                                    :value="choiceItem.value" />
                            </el-select>
                            <!-- <el-input v-model="formMock.dbname" placeholder="请输入数据库名" clearable /> -->
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <!-- prop="defaultDb" -->
                        <el-form-item label="默认库名" prop="defaultDb">
                            <el-select v-model="formMock.defaultDb" placeholder="是否使用默认" clearable>
                                <el-option v-for="choiceItem in choice_list" :key="choiceItem.name" :label="choiceItem.name"
                                    :value="choiceItem.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row style="margin-left: 15px;">
                    <el-col :span="12">
                        <el-form-item label="指定表名" prop="table_name">
                            <el-select v-model="formMock.table_name" placeholder="请输入或选择表名" filterable allow-create
                                clearable>
                                <el-option v-for="choiceItem in table_list" :key="choiceItem.name" :label="choiceItem.name"
                                    :value="choiceItem.value" />
                            </el-select>
                            <!-- <el-input v-model="formMock.table_name" placeholder="请输入表名" clearable /> -->
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="生成表名" prop="defaultTable">
                            <el-select v-model="formMock.defaultTable" placeholder="是否使用默认" clearable>
                                <el-option v-for="choiceItem in choice_list" :key="choiceItem.name" :label="choiceItem.name"
                                    :value="choiceItem.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row style="margin-left: 15px;">
                    <el-col :span="12">
                        <el-form-item label="指定字段" prop="column_list">
                            <el-select v-model="formMock.column_list" placeholder="请选择字段名" clearable multiple collapse-tags>
                                <el-option v-for="choiceItem in columns_list" :key="choiceItem.name"
                                    :label="choiceItem.name" :value="choiceItem.value" />
                            </el-select>
                            <!-- <el-input v-model="formMock.column_list" placeholder="请输入字段名称" clearable /> -->
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="默认字段" prop="defaultColumns">
                            <el-select v-model="formMock.defaultColumns" placeholder="是否使用默认" clearable>
                                <el-option v-for="choiceItem in choice_list" :key="choiceItem.name" :label="choiceItem.name"
                                    :value="choiceItem.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row style="margin-left: 15px;">
                    <el-col :span="12">
                        <el-form-item label="指定隐私" prop="secret_list">
                            <el-select v-model="formMock.secret_list" placeholder="请选择隐私类型" clearable multiple
                                collapse-tags>
                                <el-option v-for="choiceItem in secrets_list" :key="choiceItem.name"
                                    :label="choiceItem.name" :value="choiceItem.value" />
                            </el-select>
                            <!-- <el-input v-model="formMock.secret_list" placeholder="请指定隐私类型" clearable /> -->
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="默认隐私" prop="defineSecrets">
                            <el-select v-model="formMock.defineSecrets" placeholder="是否使用默认" clearable>
                                <el-option v-for="choiceItem in choice_list" :key="choiceItem.name" :label="choiceItem.name"
                                    :value="choiceItem.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row style="margin-left: 15px;">
                    <el-col :span="12">
                        <el-form-item label="造数行数" prop="dataLines" :rules="[
                            { required: true, message: '请输入造数行数' },
                            { type: 'number', message: '请输入数字' },
                        ]">
                            <el-input v-model.number="formMock.dataLines" placeholder="请输入造数行数" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row style="margin-left: 15px; margin-top: 20px">
                    <el-col :span="12" style="color: rgb(191, 8, 8);">
                        <p>Tips: 使用已有表造数时，将默认使用已有表的字段...</p>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <span class="dialog-footer1">
                    <el-button @click="handleMockCancel">取消</el-button>
                    <el-button type="primary" @click="onSubmitMock">确定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

// 页面数据如果要做双向绑定，可以通过ref和reactive;

<script>
import { defineComponent, getCurrentInstance, onMounted, ref, reactive } from 'vue';
import { useStore } from 'vuex';
import { ElMessageBox, ElMessage } from 'element-plus';
export default defineComponent({
    setup() {
        const store = useStore();
        const list = ref([]);
        const config = reactive({
            total: 0,
            page: 1,
            connect_id: '',
            connect_name: '',
            sql_type: '',
            host: '',
            connect_status: ''
        });
        const db_list = ref([]);
        const table_list = ref([]);
        const columns_list = ref([]);
        const secrets_list = ref([]);
        const getDbList = async () => {
            let res1 = await proxy.$api.getDbList();
            db_list.value = res1.data;
            console.log(db_list, 'db_list');
        };
        const sql_list = ref([
            { name: "mysql", value: 'mysql' },
            { name: "oracle", value: 'oracle' },
            { name: "hive", value: 'hive' },
            { name: "db2", value: 'db2' },
            { name: "presto", value: 'presto' },
            { name: "postgrep", value: 'postgrep' }
        ]);
        const choice_list = ref([
            { name: '是', value: '1' },
            { name: '否', value: '0' },
        ]);
        const status_list = ref([
            { name: "正常", value: 'normal' },
            { name: "异常", value: 'abnormal' },
        ]);
        const dialogVisible = ref(false);
        const mockDialogVisible = ref(false);
        const { proxy } = getCurrentInstance();
        const formInline = reactive({
            connect_name: '',
            sql_type: '',
            host: '',
            connect_status: ''
        });
        const handleMockData = async (row) => {
            try {
                if (localStorage.getItem('connection_info')) {
                    store.commit('cleanConnectInfo');
                }
                proxy.formMock.dbname = '';
                let res1 = await proxy.$api.getDbList(row);
                if (res1.code === 200) {
                    store.commit('setConnectInfo', row);
                    mockDialogVisible.value = true;
                    db_list.value = res1.data;
                    let res2 = await proxy.$api.getColumnList();
                    if (res2.code === 200) {
                        columns_list.value = res2.data;
                    } else {
                        ElMessage.error(res2.msg || '获取字段列表失败');
                    }
                    let res3 = await proxy.$api.getSecretList();
                    if (res3.code === 200) {
                        secrets_list.value = res3.data;
                    } else {
                        ElMessage.error(res3.msg || '获取隐私字段列表失败');
                    }
                } else {
                    ElMessage.error(res1.msg || '获取数据库列表失败');
                }
            } catch (error) {
                console.error('获取数据错误:', error);
                ElMessage.error('操作失败，请稍后重试');
            }
        };
        const handleVisibleChange = async (formMock) => {
            if (!localStorage.getItem('connection_info')) return;
            if (!formMock) return;
            
            try {
                const connection_info = JSON.parse(localStorage.getItem('connection_info'));
                connection_info.db = formMock;
                let res = await proxy.$api.getTableList(connection_info);
                if (res.code === 200) {
                    table_list.value = res.data;
                } else {
                    ElMessage.error(res.msg || '获取表列表失败');
                }
            } catch (error) {
                console.error('获取表列表错误:', error);
                ElMessage.error('获取表列表失败，请稍后重试');
            }
        };
        const getConnectionData = async (config) => {
            try {
                let res = await proxy.$api.getConnectionList(config);
                if (res.code === 200) {
                    list.value = res.data.map((item) => {
                        item.connect_status = item.connect_status === "normal" ? "正常" : "异常";
                        return item;
                    });
                    config.total = res.count;
                } else {
                    ElMessage.error(res.msg || '获取列表失败');
                }
            } catch (error) {
                console.error('获取列表错误:', error);
                ElMessage.error('获取列表失败');
            }
        };

        const tableLabel = reactive([
            { prop: "connect_name", label: "连接名", width: 180 },
            { prop: "sql_type", label: "sql类型", width: 100 },
            { prop: "host", label: "连接地址", width: 140 },
            { prop: "port", label: "端口", width: 120 },
            { prop: "db", label: "数据库", width: 120 },
            { prop: "username", label: "用户名", width: 120 },
            { 
                prop: "password", 
                label: "密码", 
                width: 100,
                formatter: (row) => {
                    return row.password ? '******' : '';
                }
            },
            { prop: "connect_status", label: "连接状态", width: 100 },
        ]);
        const formUser = reactive({
            connect_id: '',
            connect_name: '',
            sql_type: '',
            host: '',
            port: '',
            db: '',
            username: '',
            password: '',
            create_time: '',
        });
        const formMock = reactive({
            dbname: '',
            table_name: '',
            column_list: [],
            secret_list: [],
            defaultDb: '',
            defaultTable: '',
            defaultColumns: '',
            defineSecrets: '',
            dataLines: ''
        });
        const changePage = (page) => {
            config.page = page;
            getConnectionData(config);
        };
        const handleSearch = () => {
            config.connect_id = formInline.connect_id;
            config.connect_name = formInline.connect_name;
            config.sql_type = formInline.sql_type;
            config.host = formInline.host;
            config.connect_status = formInline.connect_status;
            console.log(config, 'config');
            getConnectionData(config);
        };
        const handleCancel = () => {
            dialogVisible.value = false;
            proxy.$refs.userForm.resetFields();
        };
        const handleMockCancel = () => {
            mockDialogVisible.value = false;
            proxy.$refs.mockForm.resetFields();
        };
        const handleClose = () => {
            ElMessageBox.confirm('是否确认关闭?')
                .then(() => {
                    proxy.$refs.userForm.resetFields();
                    dialogVisible.value = false;
                })
                .catch(() => {
                    // catch error
                })
        };
        const handleClose1 = () => {
            ElMessageBox.confirm('是否确认关闭?')
                .then(() => {
                    proxy.$refs.mockForm.resetFields();
                    mockDialogVisible.value = false;
                })
                .catch(() => {
                    // catch error
                })
        };
        const handleDelete = (row) => {
            ElMessageBox.confirm('是否确认删除?').then(async () => {
                await proxy.$api.deleteConnection(row.connect_id);
                ElMessage.success('删除成功！');
                getConnectionData(config);
            });
        };
        const onSubmitMock = async () => {
            if (!localStorage.getItem('connection_info')) {
                return
            };
            let connection_info1 = JSON.parse(localStorage.getItem('connection_info'));
            // // 为对象新增属性和值
            // Vue.set(obj, 'b', 2);
            // Object.assign()方法将两个对象合并和覆盖，相同属性后面的对象覆盖前面的；
            console.log(connection_info1, 'connection_info1');
            console.log(formMock, 'formMock');
            const mergedObj = Object.assign({}, connection_info1, formMock);
            console.log(mergedObj, '合并后的对象为：')

            let res = await proxy.$api.mockConnectData(mergedObj);
            if (res.code == 200) {
                ElMessage({
                    showClose: true,
                    message: "造数成功！",
                    type: "success",
                });
            } else {
                ElMessage({
                    showClose: true,
                    message: res.msg,
                    type: "error",
                });
            }

            proxy.$refs.mockForm.resetFields();
            mockDialogVisible.value = false;
        };
        const onSubmit = () => {
            proxy.$refs.userForm.validate(async (valid) => {
                if (valid) {
                    try {
                        if (action.value === 'add') {
                            let res = await proxy.$api.addConnection(formUser);
                            if (res.code === 200) {
                                proxy.$refs.userForm.resetFields();
                                dialogVisible.value = false;
                                getConnectionData(config);
                                ElMessage.success('添加成功');
                            } else {
                                ElMessage.error(res.msg || '添加失败');
                            }
                        } else {
                            let res1 = await proxy.$api.updateConnection(formUser.connect_id, formUser);
                            if (res1.code === 200) {
                                proxy.$refs.userForm.resetFields();
                                dialogVisible.value = false;
                                getConnectionData(config);
                                ElMessage.success('更新成功');
                            } else {
                                ElMessage.error(res1.msg || '更新失败');
                            }
                        }
                    } catch (error) {
                        console.error('提交表单错误:', error);
                        ElMessage.error('操作失败，请稍后重试');
                    }
                } else {
                    ElMessage.error('请输入正确的内容');
                }
            });
        };

        const action = ref('add');
        const handleAdd = () => {
            action.value = 'add';
            dialogVisible.value = true;
        };
        const handleEdit = (row) => {
            console.log(row, 'row')
            action.value = 'edit';
            dialogVisible.value = true;
            // 在DOM更新完成后再执行相关操作，以避免出现不一致的情况。
            proxy.$nextTick(() => {
                console.log(row, 'row');
                Object.assign(formUser, row); //浅拷贝
            });
        };

        const handleTestConnect = async (row) => {
            try {
                let res_test = await proxy.$api.testConnection(row);
                if (res_test.code === 200) {
                    ElMessage.success('连接成功！');
                } else {
                    ElMessage.error('连接失败，请确认环境是否可用！');
                }
            } catch (error) {
                console.error('测试连接错误:', error);
                ElMessage.error('测试连接失败，请稍后重试');
            }
        };

        onMounted(() => {
            getConnectionData(config);
        });

        return {
            tableLabel,
            list,
            config,
            changePage,
            formInline,
            handleSearch,
            dialogVisible,
            mockDialogVisible,
            handleClose,
            formUser,
            onSubmit,
            handleCancel,
            handleEdit,
            action,
            handleAdd,
            handleDelete,
            getConnectionData,
            sql_list,
            status_list,
            handleTestConnect,
            formMock,
            handleMockCancel,
            onSubmitMock,
            handleMockData,
            choice_list,
            db_list,
            table_list,
            getDbList,
            handleVisibleChange,
            store,
            columns_list,
            secrets_list,
            handleClose1,

        };
    }
})
</script>

<style lang="less" scoped>
.table {
    position: relative;
    height: 520px;

    .pager {
        position: absolute;
        right: 0;
        bottom: -20px; //相对于其父元素底部的偏移量,
    }

    .el-table {
        display: flex; //盒子布局
        justify-content: space-between;
    }
}

.user-header {
    display: flex; //盒子布局
    justify-content: space-between;
}
</style>

