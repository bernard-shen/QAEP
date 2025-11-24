<template>
    <div>
        <div class="user-header">
            <el-button type="primary" @click="handleAdd">+新增</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="请输入">
                    <el-input v-model="formInline.keyword" placeholder="请输入用户名" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="table">
            <el-table :data="list" style="width: 100%" height="500px ">
                <el-table-column v-for="item in tableLabel" :key="item.prop" :label="item.label" :prop="item.prop"
                    :min-width="item.width ? item.width : 125" />
                <el-table-column fixed="right" label="操作" width="180" class="operation">
                    <!-- 通过scope插槽获取待编辑数据 -->
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button type="primary" size="small" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" background layout="prev, pager, next" :total="config.total"
                @current-change="changePage" />
        </div>
        <el-dialog v-model="dialogVisible" :title="action == 'add' ? '新增用户' : '编辑用户'" width="40%"
            :before-close="handleClose">
            <el-form :inline="true" :model="formUser" ref="userForm">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="用户名" prop="username" :rules="[
                            { required: true, message: '请输入用户名', trigger: 'blur' },
                            { min: 3, max: 20, message: '用户名长度在3~20之间', trigger: 'blur' },]">
                            <el-input v-model="formUser.username" placeholder="请输入用户名" clearable />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="密码" prop="password" :rules="[
                            {
                                required: true,
                                message: '请输入密码',
                                trigger: 'blur',
                            }]">
                            <el-input type="password" show-password v-model="formUser.password" placeholder="请输入密码"
                                clearable />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <!-- 待完成：使用第二种验证方法，加判断：在手机号字段为空或未定义时才应用数字验证规则 -->
                        <el-form-item label="手机号" prop="phone" 
                        :rules="[
                            { required: true, message: '请输入手机号' },
                            { type: 'str', message: '手机号只能是11位数字' },
                        ]">
                            <el-input v-model.number="formUser.phone" placeholder="请输入手机号" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="电子邮箱" prop="email" :rules="[
                            {
                                required: true,
                                message: '请输入邮箱地址',
                                trigger: 'blur',
                            },
                            {
                                type: 'email',
                                message: '请输入合法的邮箱',
                                trigger: ['blur', 'change'],
                            },
                        ]">
                            <el-input v-model="formUser.email" placeholder="请输入邮箱" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row>
                    <el-col :span="12">
                        <el-form-item label="角色名" prop="role_id" :rules="[
                            {
                                required: true,
                                message: '请选择角色',
                                trigger: 'blur',
                            }
                        ]">
                            <el-select v-model="formUser.role_id" placeholder="请选择角色" clearable>
                                <el-option v-for="roleItem in role_list" :key="roleItem.id" :label="roleItem.role"
                                    :value="roleItem.id" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="生效时间" prop="date">
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
    </div>
</template>

// 页面数据如果要做双向绑定，可以通过ref和reactive;

<script>
import { defineComponent, getCurrentInstance, onMounted, ref, reactive } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
export default defineComponent({
    setup() {

        const list = ref([]);
        const role_list = ref([]);
        const config = reactive({
            total: 0,
            page: 1,
            name: ''
        });
        const dialogVisible = ref(false);
        const { proxy } = getCurrentInstance();
        const formInline = reactive({
            keyword: '',
        })
        const getUserData = async (config) => {
            try {
                const params = {
                    page: config.page,
                    keyword: config.name || ''
                };
                const res = await proxy.$api.getUserList(params);
                if (res.code === 200) {
                    list.value = res.data.map(item => ({
                        ...item,
                        role_name: item.roles
                    }));
                    config.total = res.total || 0;
                    config.total_pages = res.total_pages || 1;
                } else {
                    ElMessage.error('获取用户列表失败');
                }
            } catch (error) {
                console.error('获取用户列表错误:', error);
                ElMessage.error('获取用户列表失败');
            }
        };
        const getRoleData = async () => {
            try {
                const res = await proxy.$api.getRoleList();
                if (res.code === 200) {
                    role_list.value = res.data;
                    console.log('角色列表:', role_list.value);
                } else {
                    ElMessage.error('获取角色列表失败');
                }
            } catch (error) {
                console.error('获取角色列表错误:', error);
                ElMessage.error('获取角色列表失败');
            }
        };

        const tableLabel = reactive([
            {
                prop: "uid",
                label: "编号"
            },
            {
                prop: "username",
                label: "姓名"
            },
            { 
                prop: "role_name",
                label: "角色" 
            },
            { 
                prop: "phone", 
                label: "手机号码" 
            },
            { 
                prop: "email", 
                label: "电子邮箱", 
                width: 240 
            },
            { 
                prop: "create_time", 
                label: "创建时间", 
                width: 200 
            },
        ]);
        const formUser = reactive({
            uid: '',
            username: '',
            password: '',
            role_id: '',
            phone: '',
            email: '',
            date: ''
        });
        const changePage = (page) => {
            config.page = page;
            getUserData(config);
        };
        const handleSearch = () => {
            config.page = 1;  // 搜索时重置页码
            config.name = formInline.keyword;
            getUserData(config);
        };
        const handleCancel = () => {
            dialogVisible.value = false;
            proxy.$refs.userForm.resetFields();
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
        const handleDelete = (row) => {
            ElMessageBox.confirm('是否确认删除?')
                .then(async () => {
                    await proxy.$api.delUser({
                        uid: row.uid,
                    });
                ElMessage({
                    showClose: true,
                    message: "删除成功！",
                    type: "success",
                });
                getUserData(config);
            })
            .catch(() => {
                // catch error
            });
        };
        const onSubmit = () => {
            proxy.$refs.userForm.validate(async (vaild) => {
                if (vaild) {
                    if (action.value == 'add') {
                        let res = await proxy.$api.addUser(formUser);
                        if (res) {
                            proxy.$refs.userForm.resetFields();
                            dialogVisible.value = false; //ref对象要通过value赋值更新
                            getUserData(config);
                        }
                    } else {
                        let res1 = await proxy.$api.updateUser(formUser);
                        if (res1) {
                            proxy.$refs.userForm.resetFields();
                            dialogVisible.value = false; //ref对象要通过value赋值更新
                            getUserData(config);}
                    }

                } else {
                    ElMessage({
                        showClose: true,
                        message: "请输入正确的内容",
                        type: "error",
                    });
                };
            })
        };

        const action = ref('add');
        const handleAdd = () => {
            action.value = 'add';
            dialogVisible.value = true;
        };
        const handleEdit = (row) => {
            action.value = 'edit';
            dialogVisible.value = true;
            proxy.$nextTick(() => {
                formUser.uid = row.uid;
                formUser.username = row.username;
                formUser.role_id = row.role_id;
                formUser.phone = row.phone;
                formUser.email = row.email;
                formUser.date = row.create_time;
            });
        };
        onMounted(() => {
            getUserData(config);
            getRoleData();
        });

        return {
            tableLabel,
            list,
            config,
            changePage,
            formInline,
            handleSearch,
            dialogVisible,
            handleClose,
            formUser,
            onSubmit,
            getRoleData,
            role_list,
            handleCancel,
            handleEdit,
            action,
            handleAdd,
            handleDelete,
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

