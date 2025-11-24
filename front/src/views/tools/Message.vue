<template>
    <div class="message-container">
        <div class="message-header">
            <el-button type="primary" @click="handleAdd">+新增消息</el-button>
            <el-form :inline="true" :model="formInline">
                <el-form-item label="请输入">
                    <el-input v-model="formInline.keyword" placeholder="请输入消息描述" clearable />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">搜索</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div class="table">
            <el-table :data="messageList" style="width: 100%" height="500px">
                <el-table-column prop="description" label="消息描述" min-width="120" />
                <el-table-column prop="content" label="消息体" min-width="200">
                    <template #default="scope">
                        <div v-html="scope.row.content"></div>
                    </template>
                </el-table-column>
                <el-table-column prop="target" label="推送目标" min-width="120" />
                <el-table-column prop="cron" label="推送频率" min-width="120" />
                <el-table-column prop="create_time" label="创建时间" min-width="160" />
                <el-table-column fixed="right" label="操作" width="120">
                    <template #default="scope">
                        <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination class="pager" background layout="prev, pager, next" :total="config.total"
                @current-change="changePage" />
        </div>

        <el-dialog v-model="dialogVisible" title="新增消息" width="60%" :before-close="handleClose">
            <el-form :model="formMessage" ref="messageForm" label-width="100px">
                <el-form-item label="消息描述" prop="description" :rules="[
                    { required: true, message: '请输入消息描述', trigger: 'blur' }
                ]">
                    <el-input v-model="formMessage.description" placeholder="请输入消息描述" />
                </el-form-item>

                <el-form-item label="消息体" prop="content" :rules="[
                    { required: true, message: '请输入消息内容', trigger: 'blur' }
                ]">
                    <el-upload
                        class="upload-demo"
                        action="#"
                        :auto-upload="false"
                        :on-change="handleImageUpload"
                        :show-file-list="false">
                        <el-button type="primary">点击上传图片</el-button>
                    </el-upload>
                    <div class="editor-container">
                        <el-input
                            type="textarea"
                            v-model="formMessage.content"
                            :rows="6"
                            placeholder="请输入消息内容"
                        />
                    </div>
                </el-form-item>

                <el-form-item label="推送目标" prop="target" :rules="[
                    { required: true, message: '请选择推送目标', trigger: 'change' }
                ]">
                    <el-select v-model="formMessage.target" placeholder="请选择推送目标" multiple>
                        <el-option v-for="item in targetOptions" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>

                <el-form-item label="推送频率" required>
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
    name: 'Message',
    setup() {
        const { proxy } = getCurrentInstance();
        const messageList = ref([]);
        const targetOptions = ref(['效率工程群', '测试小分队', 'shenpf', '李亮']);
        
        const config = reactive({
            total: 0,
            page: 1,
            name: ''
        });

        const dialogVisible = ref(false);
        const formInline = reactive({
            keyword: ''
        });

        const formMessage = reactive({
            description: '',
            content: '',
            target: [],
            cron: ''
        });

        const cronForm = reactive({
            minute: '*',
            hour: '*',
            day: '*',
            month: '*',
            week: '*'
        });

        // 获取消息列表
        const getMessageList = async (config) => {
            try {
                // 模拟数据，实际需要调用接口
                messageList.value = [
                    {
                        id: 1,
                        description: '每日提醒',
                        content: '请及时更新日报',
                        target: '效率工程群',
                        cron: '0 18 * * *',
                        create_time: '2024-01-20 10:00:00'
                    }
                ];
                config.total = 1;
            } catch (error) {
                console.error('获取消息列表失败:', error);
                ElMessage.error('获取消息列表失败');
            }
        };

        // 处理图片上传
        const handleImageUpload = (file) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                formMessage.content += `<img src="${e.target.result}" style="max-width:100%;" />`;
            };
            reader.readAsDataURL(file.raw);
        };

        // 生成crontab表达式
        const generateCron = () => {
            return `${cronForm.minute} ${cronForm.hour} ${cronForm.day} ${cronForm.month} ${cronForm.week}`;
        };

        // 提交表单
        const onSubmit = () => {
            proxy.$refs.messageForm.validate(async (valid) => {
                if (valid) {
                    formMessage.cron = generateCron();
                    // TODO: 调用创建消息接口
                    ElMessage.success('创建成功');
                    dialogVisible.value = false;
                    getMessageList(config);
                }
            });
        };

        // 删除消息
        const handleDelete = (row) => {
            ElMessageBox.confirm('确认删除该消息?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async () => {
                // TODO: 调用删除接口
                ElMessage.success('删除成功');
                getMessageList(config);
            });
        };

        // 分页处理
        const changePage = (page) => {
            config.page = page;
            getMessageList(config);
        };

        // 搜索处理
        const handleSearch = () => {
            config.page = 1;
            config.name = formInline.keyword;
            getMessageList(config);
        };

        // 新增消息
        const handleAdd = () => {
            dialogVisible.value = true;
        };

        // 取消操作
        const handleCancel = () => {
            dialogVisible.value = false;
            proxy.$refs.messageForm.resetFields();
        };

        // 关闭对话框
        const handleClose = () => {
            ElMessageBox.confirm('确认关闭？未保存的内容将会丢失')
                .then(() => {
                    dialogVisible.value = false;
                    proxy.$refs.messageForm.resetFields();
                })
                .catch(() => {});
        };

        onMounted(() => {
            getMessageList(config);
        });

        return {
            messageList,
            targetOptions,
            config,
            dialogVisible,
            formInline,
            formMessage,
            cronForm,
            handleSearch,
            handleAdd,
            handleDelete,
            handleCancel,
            handleClose,
            onSubmit,
            changePage,
            handleImageUpload
        };
    }
});
</script>

<style lang="less" scoped>
.message-container {
    padding: 20px;

    .message-header {
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

    .editor-container {
        margin-top: 10px;
    }

    :deep(.el-upload) {
        margin-bottom: 10px;
    }
}
</style>
