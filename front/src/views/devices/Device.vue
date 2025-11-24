<template>
    <div>
        <div class="device-header">
            <el-button type="primary" @click="handleAdd">+新增设备</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="请输入">
                    <el-input v-model="formInline.keyword" placeholder="请输入设备名称" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="table">
            <el-table :data="list" style="width: 100%" height="500px">
                <el-table-column v-for="item in tableLabel" :key="item.prop" :label="item.label" :prop="item.prop"
                    :formatter="item.formatter" :min-width="item.width ? item.width : 125" />
                <el-table-column fixed="right" label="操作" width="280" class="operation">
                    <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
                        <el-button type="success" size="small" @click="handleApply(scope.row)" 
                            :disabled="scope.row.status !== '0'">申请</el-button>
                        <el-button type="warning" size="small" @click="handleRelease(scope.row)"
                            :disabled="scope.row.status !== '1'">释放</el-button>
                        <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" background layout="prev, pager, next" :total="config.total"
                @current-change="changePage" />
        </div>

        <el-dialog v-model="dialogVisible" :title="action == 'add' ? '新增设备' : '编辑设备'" width="40%"
            :before-close="handleClose">
            <el-form :inline="true" :model="formDevice" ref="deviceForm">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="设备名称" prop="device_model" :rules="formRules.device_model">
                            <el-input v-model="formDevice.device_model" placeholder="请输入设备名称" clearable />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="设备类型" prop="device_type" :rules="formRules.device_type">
                            <el-select v-model="formDevice.device_type" placeholder="请选择设备类型">
                                <el-option label="Android" value="Android" />
                                <el-option label="IOS" value="IOS" />
                                <el-option label="Mac" value="Mac" />
                                <el-option label="Windows" value="Windows" />
                                <el-option label="HarmonyOS" value="harmonyOS" />
                                <el-option label="其他" value="other" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="操作系统" prop="os_name">
                            <el-input v-model="formDevice.os_name" placeholder="请输入操作系统" clearable />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="系统版本" prop="os_version">
                            <el-input v-model="formDevice.os_version" placeholder="请输入系统版本" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form-item label="资产编号" prop="asset_code">
                            <el-input v-model="formDevice.asset_code" placeholder="请输入资产编号" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form-item label="所属人" prop="owner">
                            <el-input v-model="formDevice.owner" placeholder="请输入所属人" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form-item label="备注" prop="notes">
                            <el-input v-model="formDevice.notes" type="textarea" placeholder="请输入备注信息" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form-item label="芯片处理器" prop="processor">
                            <el-input v-model="formDevice.processor" placeholder="请输入芯片处理器" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form-item label="锁屏密码" prop="screen_lock_password">
                            <el-input v-model="formDevice.screen_lock_password" placeholder="请输入锁屏密码" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form-item label="安装密码" prop="install_password">
                            <el-input v-model="formDevice.install_password" placeholder="请输入安装密码" clearable />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-form-item label="购入日期" prop="buy_time">
                            <el-date-picker
                                v-model="formDevice.buy_time"
                                type="date"
                                placeholder="请选择购入日期"
                                format="YYYY-MM-DD"
                                value-format="YYYY-MM-DD"
                            />
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

<script>
import { defineComponent, getCurrentInstance, onMounted, ref, reactive } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';

export default defineComponent({
    setup() {
        const { proxy } = getCurrentInstance();
        const list = ref([]);
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
            { prop: "device_type", label: "设备类型" },
            { prop: "os_name", label: "系统名称" },
            { prop: "os_version", label: "系统版本" },
            { prop: "device_model", label: "设备型号" },
            { prop: "asset_code", label: "资产编号" },
            { prop: "owner", label: "设备负责人" },
            { prop: "current_user", label: "当前使用者" },
            { 
                prop: "status", 
                label: "状态",
                formatter: (row) => {
                    const statusMap = {
                        '0': '空闲',
                        '1': '占用',
                        '2': '领用中'
                    };
                    return statusMap[row.status] || row.status;
                }
            },
            { 
                prop: "update_time", 
                label: "更新时间",
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
        ]);

        // 表单数据
        const formDevice = reactive({
            id: '',
            device_model: '',     // 设备名称/型号
            device_type: '',      // 设备类型
            os_name: '',         // 操作系统
            os_version: '',      // 系统版本
            asset_code: '',      // 资产编码
            owner: '',          // 所属人
            notes: '',          // 备注
            processor: '',      // 芯片处理器
            screen_lock_password: '', // 锁屏密码
            install_password: '',     // 安装密码
            buy_time: ''        // 购入日期
        });

        // 表单验证规则
        const formRules = {
            device_model: [
                { required: true, message: '请输入设备名称', trigger: 'blur' },
                { min: 2, max: 50, message: '名称长度在2~50之间', trigger: 'blur' }
            ],
            device_type: [
                { required: true, message: '请选择设备类型', trigger: 'change' }
            ]
        };

        // 获取设备列表
        const getDeviceData = async (config) => {
            try {
                const params = {
                    page: config.page,
                    keyword: config.name || ''
                };
                const res = await proxy.$api.getDeviceList(params);
                if (res.code === 200) {
                    list.value = res.data;
                    config.total = res.total || 0;
                    // 更新总页数
                    config.total_pages = res.total_pages || 1;
                } else {
                    ElMessage.error('获取设备列表失败');
                }
            } catch (error) {
                console.error('获取设备列表错误:', error);
                ElMessage.error('获取设备列表失败');
            }
        };

        // 分页处理
        const changePage = (page) => {
            config.page = page;
            getDeviceData(config);
        };

        // 搜索处理
        const handleSearch = () => {
            config.name = formInline.keyword;
            getDeviceData(config);
        };

        // 取消操作
        const handleCancel = () => {
            dialogVisible.value = false;
            proxy.$refs.deviceForm.resetFields();
        };

        // 关闭对话框
        const handleClose = () => {
            ElMessageBox.confirm('是否确认关闭?')
                .then(() => {
                    proxy.$refs.deviceForm.resetFields();
                    dialogVisible.value = false;
                })
                .catch(() => {});
        };

        // 删除设备
        const handleDelete = (row) => {
            ElMessageBox.confirm('是否确认删除该设备?', '提示', {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                await proxy.$api.deleteDevice(row.id);
                ElMessage.success('删除成功！');
                getDeviceData(config);
            }).catch(() => {});
        };

        // 申请设备
        const handleApply = (row) => {
            ElMessageBox.confirm('是否确认申请该设备?', '提示', {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                await proxy.$api.applyDevice(row.id, {});
                ElMessage.success('申请成功！');
                getDeviceData(config);
            }).catch(() => {});
        };

        // 释放设备
        const handleRelease = (row) => {
            ElMessageBox.confirm('是否确认释放该设备?', '提示', {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                await proxy.$api.releaseDevice(row.id);
                ElMessage.success('释放成功！');
                getDeviceData(config);
            }).catch(() => {});
        };

        // 提交表单
        const onSubmit = () => {
            proxy.$refs.deviceForm.validate(async (valid) => {
                if (valid) {
                    try {
                        // 直接提交表单数据，字段名已经匹配
                        if (action.value === 'add') {
                            await proxy.$api.createDevice(formDevice);
                            ElMessage.success('添加成功！');
                        } else {
                            await proxy.$api.updateDevice(formDevice.id, formDevice);
                            ElMessage.success('更新成功！');
                        }
                        proxy.$refs.deviceForm.resetFields();
                        dialogVisible.value = false;
                        getDeviceData(config);
                    } catch (error) {
                        ElMessage.error('操作失败，请重试！');
                    }
                }
            });
        };

        const action = ref('add');
        
        // 添加设备
        const handleAdd = () => {
            action.value = 'add';
            dialogVisible.value = true;
        };

        // 编辑设备
        const handleEdit = (row) => {
            action.value = 'edit';
            dialogVisible.value = true;
            proxy.$nextTick(() => {
                // 直接使用后端返回的字段名
                Object.assign(formDevice, {
                    id: row.id,
                    device_model: row.device_model,
                    device_type: row.device_type,
                    os_name: row.os_name,
                    os_version: row.os_version,
                    asset_code: row.asset_code,
                    owner: row.owner,
                    notes: row.notes,
                    processor: row.processor,
                    screen_lock_password: row.screen_lock_password,
                    install_password: row.install_password,
                    buy_time: row.buy_time
                });
            });
        };

        // 更新设备类型选项
        const deviceTypes = [
            { label: 'Android', value: 'Android' },
            { label: 'IOS', value: 'IOS' },
            { label: 'Mac', value: 'Mac' },
            { label: 'Windows', value: 'Windows' },
            { label: 'HarmonyOS', value: 'harmonyOS' },
            { label: '其他', value: 'other' }
        ];

        // 更新状态选项
        const statusOptions = [
            { label: '空闲', value: '0' },
            { label: '占用', value: '1' },
            { label: '领用中', value: '2' }
        ];

        // 状态映射函数
        const getStatusText = (status) => {
            const statusMap = {
                '0': '空闲',
                '1': '占用',
                '2': '领用中'
            };
            return statusMap[status] || status;
        };

        onMounted(() => {
            getDeviceData(config);
        });

        return {
            list,
            config,
            tableLabel,
            formInline,
            formDevice,
            dialogVisible,
            action,
            changePage,
            handleSearch,
            handleAdd,
            handleEdit,
            handleDelete,
            handleApply,
            handleRelease,
            handleCancel,
            handleClose,
            onSubmit,
            deviceTypes,
            statusOptions,
            formRules,
            getStatusText
        };
    }
});
</script>

<style lang="less" scoped>
.device-header {
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

