<template>
    <div>
        <div class="user-header">
            <el-button type="primary" @click="handleAdd">+新增</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="请输入">
                    <el-input v-model="formInline.keyword" placeholder="请输入角色名" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="table">
            <el-table :data="role_list" style="width: 100%" height="500px ">
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
        <el-dialog v-model="dialogVisible" :title="action == 'add' ? '新增角色' : '编辑角色'" width="40%"
            :before-close="handleClose">
            <el-form :inline="true" :model="formUser" ref="userForm">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="角色名" prop="role" :rules="[
                            { required: true, message: '请输入角色名', trigger: 'blur' },
                            { min: 3, max: 20, message: '角色名长度在3~20之间', trigger: 'blur' },]">
                            <el-input v-model="formUser.role" placeholder="请输入角色名" clearable />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="权限标识" prop="permissions" :rules="[
                            { required: true, message: '权限标识', trigger: 'blur' },]">
                            <el-input v-model="formUser.permissions" placeholder="请输入权限标识" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="相关描述" prop="tips" :rules="[
                            { required: false, message: '请输入描述', trigger: 'blur' },
                            { min: 0, max: 200, message: '角色名长度在0~200之间', trigger: 'blur' },]">
                            <el-input v-model="formUser.tips" placeholder="请输入描述" clearable />
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
        const getRoleData = async (config) => {
            try {
                const params = {
                    page: config.page,
                    keyword: config.name || ''
                };
                const res = await proxy.$api.getRoleList(params);
                if (res.code === 200) {
                    role_list.value = res.data;
                    config.total = res.total || 0;
                    config.total_pages = res.total_pages || 1;
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
                prop: "role_id",
                label: "编号"
            },
            {
                prop: "role_name",
                label: "角色名"
            },
            {
                prop: "role_permissions",
                label: "权限标识"
            },
            {
                prop: "tips",
                label: "相关描述"
            }
        ]);
        const formUser = reactive({
            role_id: '',
            role_name: '',
            role_permissions: '',
            tips: ''
        });
        const changePage = (page) => {
            config.page = page;
            getRoleData(config);
        };
        const handleSearch = () => {
            config.page = 1;  // 搜索时重置页码
            config.name = formInline.keyword;
            getRoleData(config);
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
                    await proxy.$api.delRole({
                        id: row.id,
                    });
                ElMessage({
                    showClose: true,
                    message: "删除成功！",
                    type: "success",
                });
                getRoleData(config);
            })
            .catch(() => {
                // catch error
            });
        };
        const onSubmit = () => {
            proxy.$refs.userForm.validate(async (vaild) => {
                if (vaild) {
                    if (action.value == 'add') {
                        let res = await proxy.$api.addRole(formUser);
                        if (res) {
                            proxy.$refs.userForm.resetFields();
                            dialogVisible.value = false; //ref对象要通过value赋值更新
                            getRoleData(config);
                        }
                    } else {
                        let res1 = await proxy.$api.updateRole(formUser);
                        if (res1) {
                            proxy.$refs.userForm.resetFields();
                            dialogVisible.value = false; //ref对象要通过value赋值更新
                            getRoleData(config);}
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
                formUser.role_id = row.role_id;
                formUser.role_name = row.role_name;
                formUser.role_permissions = row.role_permissions;
                formUser.tips = row.tips;
            });
        };
        onMounted(() => {
            getRoleData(config);
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

