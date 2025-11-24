<template>
    <div>
        <div class="apply-header">
            <el-form :inline="true" :model="formInline">
                <el-form-item label="申请人">
                    <el-input v-model="formInline.keyword" placeholder="请输入申请人" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                    <el-button @click="resetSearch">重置</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div class="table">
            <el-table :data="list" style="width: 100%" height="500px" v-loading="loading">
                <el-table-column v-for="item in tableLabel" 
                    :key="item.prop" 
                    :label="item.label" 
                    :prop="item.prop"
                    :formatter="item.formatter"
                    :min-width="item.width || 120" />
                <el-table-column fixed="right" label="操作" width="200">
                    <template #default="scope">
                        <el-button 
                            type="success" 
                            size="small" 
                            @click="handleApprove(scope.row, true)"
                            :disabled="scope.row.approval_status !== '0'">
                            通过
                        </el-button>
                        <el-button 
                            type="danger" 
                            size="small" 
                            @click="handleApprove(scope.row, false)"
                            :disabled="scope.row.approval_status !== '0'">
                            拒绝
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination 
                class="pager" 
                background 
                layout="total, prev, pager, next" 
                :total="config.total"
                :current-page="config.page"
                @current-change="changePage" />
        </div>
    </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted, getCurrentInstance } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default defineComponent({
    name: 'DeviceApply',
    setup() {
        const { proxy } = getCurrentInstance();
        const list = ref([]);
        const loading = ref(false);
        
        const config = reactive({
            total: 0,
            page: 1,
            name: ''
        });

        const formInline = reactive({
            keyword: ''
        });

        // 表格列定义
        const tableLabel = [
            { prop: "device_model", label: "设备型号" },
            { prop: "device_asset_code", label: "资产编号" },
            { prop: "apply_user", label: "申请人" },
            { 
                prop: "approval_status", 
                label: "状态",
                formatter: (row) => {
                    const statusMap = {
                        '0': '待审批',
                        '1': '已通过',
                        '2': '已拒绝'
                    };
                    return statusMap[row.approval_status] || row.approval_status;
                }
            },
            { 
                prop: "apply_time", 
                label: "申请时间",
                width: 160,
                formatter: (row) => {
                    if (!row.apply_time) return '';
                    return row.apply_time;  // 后端已经格式化好了时间
                }
            },
            { 
                prop: "approval_time", 
                label: "审批时间",
                width: 160,
                formatter: (row) => {
                    if (!row.approval_time) return '';
                    return row.approval_time;
                }
            },
            { 
                prop: "approval_user", 
                label: "审批人",
                width: 100
            }
        ];

        // 获取申请列表
        const getApplyList = async () => {
            loading.value = true;
            try {
                const params = {
                    page: config.page,
                    keyword: config.name || ''
                };
                const res = await proxy.$api.getApplyList(params);
                if (res.code === 200) {
                    list.value = res.data;
                    config.total = res.total || 0;
                } else {
                    ElMessage.error('获取申请列表失败');
                }
            } catch (error) {
                console.error('获取申请列表错误:', error);
                ElMessage.error('获取申请列表失败');
            } finally {
                loading.value = false;
            }
        };

        // 审批处理
        const handleApprove = (row, isApprove) => {
            const action = isApprove ? '通过' : '拒绝';
            ElMessageBox.confirm(`是否确认${action}该申请?`, '提示', {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                try {
                    await proxy.$api.approveApply(row.id, {
                        approval_status: isApprove ? '1' : '2'
                    });
                    ElMessage.success(`${action}成功！`);
                    getApplyList();
                } catch (error) {
                    ElMessage.error(`${action}失败，请重试！`);
                }
            }).catch(() => {});
        };

        // 搜索
        const handleSearch = () => {
            config.page = 1;
            config.name = formInline.keyword;
            getApplyList();
        };

        // 重置搜索
        const resetSearch = () => {
            formInline.keyword = '';
            config.page = 1;
            config.name = '';
            getApplyList();
        };

        // 分页
        const changePage = (page) => {
            config.page = page;
            getApplyList();
        };

        onMounted(() => {
            getApplyList();
        });

        return {
            list,
            loading,
            config,
            formInline,
            tableLabel,
            handleSearch,
            resetSearch,
            changePage,
            handleApprove
        };
    }
});
</script>

<style lang="less" scoped>
.apply-header {
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