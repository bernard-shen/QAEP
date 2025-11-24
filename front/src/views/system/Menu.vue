<template>
    <div>
        <div class="menu-header">
            <el-button type="primary" @click="handleAdd">+新增</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="请输入">
                    <el-input v-model="formInline.keyword" placeholder="请输入菜单名称" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="table">
            <el-table :data="list" style="width: 100%" height="500px">
                <el-table-column v-for="item in tableLabel" :key="item.prop" :label="item.label" :prop="item.prop"
                    :min-width="item.width ? item.width : 125" />
                <el-table-column fixed="right" label="操作" width="180" class="operation">
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" background layout="prev, pager, next" :total="config.total"
                @current-change="changePage" />
        </div>

        <el-dialog v-model="dialogVisible" :title="action == 'add' ? '新增菜单' : '编辑菜单'" width="40%"
            :before-close="handleClose">
            <el-form :model="formMenu" ref="menuForm" label-width="100px">
                <el-form-item label="菜单名称" prop="name" :rules="[
                    { required: true, message: '请输入菜单名称', trigger: 'blur' },
                    { min: 2, max: 20, message: '长度在2~20个字符', trigger: 'blur' }
                ]">
                    <el-input v-model="formMenu.name" placeholder="请输入菜单名称" />
                </el-form-item>
                <el-form-item label="菜单路径" prop="url" :rules="[
                    { required: true, message: '请输入菜单路径', trigger: 'blur' }
                ]">
                    <el-input v-model="formMenu.url" placeholder="请输入菜单路径" />
                </el-form-item>
                <el-form-item label="上级菜单" prop="parent_id">
                    <el-select v-model="formMenu.parent_id" placeholder="请选择上级菜单" clearable>
                        <el-option label="无" :value="0" />
                        <el-option v-for="item in parentMenus" :key="item.id" :label="item.name" :value="item.id" />
                    </el-select>
                </el-form-item>
                <el-form-item label="菜单图标" prop="icon">
                    <el-input v-model="formMenu.icon" placeholder="请输入菜单图标" />
                </el-form-item>
                <el-form-item label="排序" prop="sort">
                    <el-input-number v-model="formMenu.sort" :min="1" :max="999" />
                </el-form-item>
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

<script>
import { defineComponent, getCurrentInstance, onMounted, ref, reactive } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';

export default defineComponent({
    setup() {
        const { proxy } = getCurrentInstance();
        const list = ref([]);
        const parentMenus = ref([]);
        const config = reactive({
            total: 0,
            page: 1,
            name: ''
        });

        const dialogVisible = ref(false);
        const formInline = reactive({
            keyword: '',
        });

        // 表格列定义
        const tableLabel = reactive([
            { prop: "menu_id", label: "菜单ID" },
            { prop: "name", label: "菜单名称" },
            { prop: "label", label: "菜单标签" },
            { prop: "path", label: "路由路径" },
            { prop: "url", label: "接口地址" },
            { prop: "icon", label: "图标" },
            { 
                prop: "is_base_menu", 
                label: "菜单类型",
                formatter: (row) => {
                    return row.is_base_menu ? '基础菜单' : '子菜单';
                }
            },
            { 
                prop: "sub_menu", 
                label: "子菜单",
                formatter: (row) => {
                    return row.sub_menu ? row.sub_menu.length + '个' : '无';
                }
            }
        ]);

        // 表单数据
        const formMenu = reactive({
            menu_id: '',
            name: '',
            label: '',
            path: '',
            url: '',
            icon: '',
            is_base_menu: true,
            sub_menu: []
        });

        // 获取菜单列表
        const getMenuData = async (config) => {
            try {
                // 添加分页参数
                const params = {
                    page: config.page,
                    keyword: config.name || ''
                };
                
                const res = await proxy.$api.getMenuList(params);
                if (res.code === 200) {
                    list.value = res.data;
                    config.total = res.total || 0;  // 设置总数
                    config.total_pages = res.total_pages || 1;  // 设置总页数
                    // 过滤出可作为父菜单的选项
                    parentMenus.value = res.data.filter(item => !item.parent_id);
                } else {
                    ElMessage.error('获取菜单列表失败');
                }
            } catch (error) {
                console.error('获取菜单列表错误:', error);
                ElMessage.error('获取菜单列表失败');
            }
        };

        // 修改分页处理函数
        const changePage = (page) => {
            config.page = page;
            getMenuData(config);  // 传入配置对象
        };

        // 修改搜索处理函数
        const handleSearch = () => {
            config.page = 1;  // 搜索时重置页码
            config.name = formInline.keyword;
            getMenuData(config);
        };

        // 取消操作
        const handleCancel = () => {
            dialogVisible.value = false;
            proxy.$refs.menuForm.resetFields();
        };

        // 关闭对话框
        const handleClose = () => {
            ElMessageBox.confirm('是否确认关闭?')
                .then(() => {
                    proxy.$refs.menuForm.resetFields();
                    dialogVisible.value = false;
                })
                .catch(() => {});
        };

        // 删除菜单
        const handleDelete = (row) => {
            ElMessageBox.confirm('是否确认删除该菜单?')
                .then(async () => {
                    await proxy.$api.deleteMenu(row.id);
                    ElMessage.success('删除成功！');
                    getMenuData(config);
                })
                .catch(() => {});
        };

        // 提交表单
        const onSubmit = () => {
            proxy.$refs.menuForm.validate(async (valid) => {
                if (valid) {
                    try {
                        if (action.value === 'add') {
                            await proxy.$api.createMenu(formMenu);
                            ElMessage.success('添加成功！');
                        } else {
                            await proxy.$api.updateMenu(formMenu.id, formMenu);
                            ElMessage.success('更新成功！');
                        }
                        proxy.$refs.menuForm.resetFields();
                        dialogVisible.value = false;
                        getMenuData(config);
                    } catch (error) {
                        ElMessage.error('操作失败，请重试！');
                    }
                }
            });
        };

        const action = ref('add');

        // 添加菜单
        const handleAdd = () => {
            action.value = 'add';
            formMenu.parent_id = 0;
            dialogVisible.value = true;
        };

        // 编辑菜单
        const handleEdit = (row) => {
            action.value = 'edit';
            dialogVisible.value = true;
            proxy.$nextTick(() => {
                // 使用解构赋值来复制需要的字段
                const {
                    menu_id,
                    name,
                    label,
                    path,
                    url,
                    icon,
                    is_base_menu,
                    sub_menu
                } = row;
                Object.assign(formMenu, {
                    menu_id,
                    name,
                    label,
                    path,
                    url,
                    icon,
                    is_base_menu,
                    sub_menu
                });
            });
        };

        onMounted(() => {
            getMenuData(config);
        });

        return {
            list,
            config,
            tableLabel,
            formInline,
            formMenu,
            dialogVisible,
            action,
            parentMenus,
            handleSearch,
            handleAdd,
            handleEdit,
            handleDelete,
            handleCancel,
            handleClose,
            onSubmit,
            changePage
        };
    }
});
</script>

<style lang="less" scoped>
.menu-header {
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
