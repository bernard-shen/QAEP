<template>
    <div class="timer-container">
        <div class="timer-header">
            <el-button type="primary" @click="handleAdd">+新增定时任务</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="请输入">
                    <el-input v-model="formInline.keyword" placeholder="请输入任务名称" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div class="table">
            <el-table :data="timerList" style="width: 100%" height="500px">
                <el-table-column prop="name" label="任务名称" min-width="120" />
                <el-table-column prop="description" label="任务描述" min-width="200" />
                <el-table-column prop="type" label="任务类型" min-width="120">
                    <template #default="scope">
                        {{ scope.row.type === 'script' ? '脚本' : '回归任务' }}
                    </template>
                </el-table-column>
                <el-table-column prop="cron" label="执行频率" min-width="120" />
                <el-table-column prop="create_time" label="创建时间" min-width="160" />
                <el-table-column fixed="right" label="操作" width="180">
                    <template #default="scope">
                        <el-button type="primary" size="small" @click="handleRun(scope.row)">执行</el-button>
                        <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" background layout="prev, pager, next" :total="config.total"
                @current-change="changePage" />
        </div>

        <el-dialog v-model="dialogVisible" title="新增定时任务" width="60%" :before-close="handleClose">
            <el-form :model="formTimer" ref="timerForm" label-width="100px">
                <el-form-item label="任务名称" prop="name" :rules="[
                    { required: true, message: '请输入任务名称', trigger: 'blur' }
                ]">
                    <el-input v-model="formTimer.name" placeholder="请输入任务名称" />
                </el-form-item>

                <el-form-item label="任务描述" prop="description" :rules="[
                    { required: true, message: '请输入任务描述', trigger: 'blur' }
                ]">
                    <el-input type="textarea" v-model="formTimer.description" :rows="3" placeholder="请输入任务描述" />
                </el-form-item>

                <el-form-item label="任务类型" prop="type" :rules="[
                    { required: true, message: '请选择任务类型', trigger: 'change' }
                ]">
                    <el-radio-group v-model="formTimer.type">
                        <el-radio label="script">Python脚本</el-radio>
                        <el-radio label="regression">回归任务</el-radio>
                    </el-radio-group>
                </el-form-item>

                <el-form-item v-if="formTimer.type === 'script'" label="脚本文件" prop="script" :rules="[
                    { required: true, message: '请上传脚本文件', trigger: 'change' }
                ]">
                    <el-upload
                        class="upload-demo"
                        action="#"
                        :auto-upload="false"
                        :on-change="handleScriptUpload"
                        :show-file-list="true"
                        accept=".py">
                        <el-button type="primary">点击上传</el-button>
                        <template #tip>
                            <div class="el-upload__tip">只能上传 .py 文件</div>
                        </template>
                    </el-upload>
                </el-form-item>

                <el-form-item v-else label="回归任务" prop="regression_id" :rules="[
                    { required: true, message: '请选择回归任务', trigger: 'change' }
                ]">
                    <el-select v-model="formTimer.regression_id" placeholder="请选择回归任务">
                        <el-option v-for="item in regressionOptions" :key="item.id" :label="item.name" :value="item.id" />
                    </el-select>
                </el-form-item>

                <el-form-item label="执行频率" required>
                    <el-row :gutter="20">
                        <el-col :span="4">
                            <el-form-item prop="minute">
                                <el-select v-model="cronForm.minute" placeholder="分">
                                    <el-option label="每分钟" value="*" />
                                    <el-option v-for="i in 59" :key="i" :label="i" :value="i" />
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="4">
                            <el-form-item prop="hour">
                                <el-select v-model="cronForm.hour" placeholder="时">
                                    <el-option label="每小时" value="*" />
                                    <el-option v-for="i in 23" :key="i" :label="i" :value="i" />
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="4">
                            <el-form-item prop="day">
                                <el-select v-model="cronForm.day" placeholder="天">
                                    <el-option label="每天" value="*" />
                                    <el-option v-for="i in 31" :key="i" :label="i" :value="i" />
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="4">
                            <el-form-item prop="month">
                                <el-select v-model="cronForm.month" placeholder="月">
                                    <el-option label="每月" value="*" />
                                    <el-option v-for="i in 12" :key="i" :label="i" :value="i" />
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="4">
                            <el-form-item prop="week">
                                <el-select v-model="cronForm.week" placeholder="周">
                                    <el-option label="每周" value="*" />
                                    <el-option label="周一" value="1" />
                                    <el-option label="周二" value="2" />
                                    <el-option label="周三" value="3" />
                                    <el-option label="周四" value="4" />
                                    <el-option label="周五" value="5" />
                                    <el-option label="周六" value="6" />
                                    <el-option label="周日" value="0" />
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
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
import { defineComponent, ref, reactive, onMounted, getCurrentInstance } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default defineComponent({
    name: 'Timer',
    setup() {
        const { proxy } = getCurrentInstance();
        const timerList = ref([]);
        const regressionOptions = ref([
            { id: 1, name: 'OA-主流程回归1' },
            { id: 2, name: '汇金-定时任务回归1' }
        ]);
        
        const config = reactive({
            total: 0,
            page: 1,
            name: ''
        });

        const dialogVisible = ref(false);
        const formInline = reactive({
            keyword: ''
        });

        const formTimer = reactive({
            name: '',
            description: '',
            type: 'script',
            script: null,
            regression_id: '',
            cron: ''
        });

        const cronForm = reactive({
            minute: '*',
            hour: '*',
            day: '*',
            month: '*',
            week: '*'
        });

        // 获取定时任务列表
        const getTimerList = async (config) => {
            try {
                // 模拟数据，实际需要调用接口
                timerList.value = [
                    {
                        id: 1,
                        name: '每日回归',
                        description: '每天晚上执行主流程回归',
                        type: 'regression',
                        regression_id: 1,
                        cron: '0 20 * * *',
                        create_time: '2024-01-20 10:00:00'
                    }
                ];
                config.total = 1;
            } catch (error) {
                console.error('获取定时任务列表失败:', error);
                ElMessage.error('获取定时任务列表失败');
            }
        };

        // 处理脚本上传
        const handleScriptUpload = (file) => {
            formTimer.script = file.raw;
        };

        // 生成crontab表达式
        const generateCron = () => {
            return `${cronForm.minute} ${cronForm.hour} ${cronForm.day} ${cronForm.month} ${cronForm.week}`;
        };

        // 立即执行任务
        const handleRun = (row) => {
            ElMessageBox.confirm('确认立即执行该任务?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                // TODO: 调用执行接口
                ElMessage.success('任务已开始执行');
            });
        };

        // 提交表单
        const onSubmit = () => {
            proxy.$refs.timerForm.validate(async (valid) => {
                if (valid) {
                    formTimer.cron = generateCron();
                    // TODO: 调用创建定时任务接口
                    ElMessage.success('创建成功');
                    dialogVisible.value = false;
                    getTimerList(config);
                }
            });
        };

        // 删除任务
        const handleDelete = (row) => {
            ElMessageBox.confirm('确认删除该任务?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                // TODO: 调用删除接口
                ElMessage.success('删除成功');
                getTimerList(config);
            });
        };

        // 分页处理
        const changePage = (page) => {
            config.page = page;
            getTimerList(config);
        };

        // 搜索处理
        const handleSearch = () => {
            config.page = 1;
            config.name = formInline.keyword;
            getTimerList(config);
        };

        // 新增任务
        const handleAdd = () => {
            dialogVisible.value = true;
        };

        // 取消操作
        const handleCancel = () => {
            dialogVisible.value = false;
            proxy.$refs.timerForm.resetFields();
        };

        // 关闭对话框
        const handleClose = () => {
            ElMessageBox.confirm('确认关闭？未保存的内容将会丢失')
                .then(() => {
                    dialogVisible.value = false;
                    proxy.$refs.timerForm.resetFields();
                })
                .catch(() => {});
        };

        onMounted(() => {
            getTimerList(config);
        });

        return {
            timerList,
            regressionOptions,
            config,
            dialogVisible,
            formInline,
            formTimer,
            cronForm,
            handleSearch,
            handleAdd,
            handleDelete,
            handleCancel,
            handleClose,
            onSubmit,
            changePage,
            handleScriptUpload,
            handleRun
        };
    }
});
</script>

<style lang="less" scoped>
.timer-container {
    padding: 20px;

    .timer-header {
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

    :deep(.el-upload) {
        margin-bottom: 10px;
    }
}
</style>
