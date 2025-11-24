<template>
    <div class="mock-files">
        <div class="mock-form">
            <div class="form-title">文件造数</div>

            <el-form :model="formData" ref="mockForm" label-width="120px">
                <el-form-item label="文件类型" prop="file_type" :rules="[
                    { required: true, message: '请选择文件类型' }
                ]">
                    <el-radio-group v-model="formData.file_type">
                        <el-radio label="csv">CSV</el-radio>
                        <el-radio label="xlsx">Excel</el-radio>
                    </el-radio-group>
                </el-form-item>

                <el-form-item label="造数字段" prop="column_list" :rules="[
                    { required: true, message: '请选择至少一个字段', type: 'array' }
                ]">
                    <el-select 
                        v-model="formData.column_list" 
                        multiple 
                        collapse-tags 
                        placeholder="请选择造数字段"
                        style="width: 400px"
                    >
                        <el-option-group label="常用类型">
                            <el-option 
                                v-for="item in privacyColumns" 
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            />
                        </el-option-group>
                        <el-option-group label="其他类型">
                            <el-option 
                                v-for="item in commonColumns" 
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            />
                        </el-option-group>
                    </el-select>
                </el-form-item>

                <el-form-item label="造数条数" prop="data_lines" :rules="[
                    { required: true, message: '请输入造数条数' },
                    { 
                        validator: (rule, value, callback) => {
                            if (value === undefined || value === '') {
                                callback(new Error('请输入造数条数'));
                            } else if (!Number.isInteger(value)) {
                                callback(new Error('请输入整数'));
                            } else if (value < 1 || value > 10000) {
                                callback(new Error('条数范围在1-10000之间'));
                            } else {
                                callback();
                            }
                        },
                        trigger: 'change'
                    }
                ]">
                    <el-input-number 
                        v-model="formData.data_lines" 
                        :min="1" 
                        :max="10000"
                        style="width: 400px"
                        controls-position="right"
                        placeholder="请输入造数条数"
                        @change="validateDataLines"
                    />
                    <div class="tip-text">生成范围在1-10000之间</div>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="handleSubmit" :loading="loading">生成文件</el-button>
                    <el-button @click="resetForm" style="margin-left: 10px">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
import { defineComponent, ref, reactive, getCurrentInstance } from 'vue'
import { ElMessage } from 'element-plus'

export default defineComponent({
    name: 'MockFiles',
    setup() {
        const { proxy } = getCurrentInstance()
        const loading = ref(false)

        // 表单数据
        const formData = reactive({
            file_type: 'csv',
            column_list: [],
            data_lines: null
        })

        // 隐私类型字段
        const privacyColumns = [
            { label: '中文姓名', value: 'name' },
            { label: '手机号', value: 'phone_number' },
            { label: '电子邮件', value: 'email' },
            { label: '中文地址', value: 'address' },
            { label: '银行卡号', value: 'bank_card' },
            { label: '企业名称', value: 'company_name' },
            { label: '身份证号', value: 'id_no' },
            { label: '固定电话', value: 'fix_phone' },
            { label: '邮政编码', value: 'post_code' },
            { label: '车牌号', value: 'car_no' },
            { label: '社会信用代码', value: 'social_credit_code' },
            { label: '汽车车架号', value: 'car_code' },
            { label: '护照号', value: 'passport' },
            { label: '税务登记证号', value: 'tax_code' },
            { label: '组织机构代码', value: 'organization' },
            { label: '营业执照代码', value: 'enterprise_code' },
            { label: '单体商户名称', value: 'individual_business' },
            { label: '军官警官证编号', value: 'officer_card' }
        ]

        // 常用类型字段
        const commonColumns = [
            { label: '随机整数', value: 'number' },
            { label: '随机字符串', value: 'character' },
            { label: '文章', value: 'description' },
            { label: '带换行符的文章', value: 'change_line_description' },
            { label: '创建时间', value: 'create_time' },
            { label: '更新时间', value: 'update_time' },
            { label: '时间戳', value: 'timestamp' },
            { label: '职位', value: 'job' },
            { label: '完整信用卡信息', value: 'full_credit_card' },
            { label: '日期', value: 'date' },
            { label: '星期', value: 'weekday' },
            { label: '时间', value: 'time' },
            { label: '时区', value: 'timezone' },
            { label: '国家', value: 'country' },
            { label: '省份', value: 'province' },
            { label: '街道', value: 'street' },
            { label: '颜色', value: 'color' },
            { label: '文件路径', value: 'file_path' },
            { label: '主机名', value: 'hostname' },
            { label: 'URL', value: 'url' },
            { label: '图片URL', value: 'image_url' },
            { label: 'IPv4', value: 'ipv4' },
            { label: 'IPv6', value: 'ipv6' },
            { label: 'MAC地址', value: 'mac_address' },
            { label: '用户名', value: 'user_name' },
            { label: '密码', value: 'password' },
            { label: 'MD5', value: 'md5' },
            { label: '字典', value: 'dictionary' },
            { label: '列表', value: 'list' },
            { label: '少数民族姓名', value: 'special_name' },
            { label: 'UUID', value: 'uuid' },
            { label: 'UID', value: 'uid' }
        ]

        // 添加验证方法
        const validateDataLines = () => {
            proxy.$refs.mockForm.validateField('data_lines');
        };

        // 提交表单
        const handleSubmit = () => {
            proxy.$refs.mockForm.validate(async (valid) => {
                if (valid) {
                    try {
                        loading.value = true;
                        const requestData = {
                            column_list: formData.column_list,
                            data_lines: Number(formData.data_lines),
                            file_type: formData.file_type.toLowerCase()
                        };
                        console.log('发送请求数据:', requestData);
                        const response = await proxy.$api.mockDataFile(requestData);
                        console.log('响应头:', response.headers);
                        console.log('响应数据类型:', typeof response.data);
                        console.log('响应数据大小:', response.data.size);

                        // 从响应头获取文件名
                        const contentDisposition = response.headers['content-disposition'];
                        console.log('Content-Disposition:', contentDisposition);
                        const filename = contentDisposition
                            ? contentDisposition.split('filename=')[1].replace(/"/g, '')
                            : `mock_data_${new Date().getTime()}.${formData.file_type.toLowerCase()}`;
                        console.log('文件名:', filename);

                        // 从响应头获取内容类型
                        const contentType = response.headers['content-type'];
                        console.log('Content-Type:', contentType);

                        // 创建 Blob
                        const blob = new Blob([response.data], {
                            type: contentType || 'text/csv;charset=utf-8-sig'
                        });
                        console.log('Blob 大小:', blob.size);

                        if (blob.size === 0) {
                            throw new Error('生成的文件内容为空');
                        }

                        // 创建下载链接
                        const url = window.URL.createObjectURL(blob);
                        const link = document.createElement('a');
                        link.href = url;
                        link.download = filename;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        window.URL.revokeObjectURL(url);

                        ElMessage.success('文件生成成功');
                    } catch (error) {
                        console.error('生成文件失败:', error);
                        // 如果是 Blob 响应中的错误信息
                        if (error.response?.data instanceof Blob) {
                            const reader = new FileReader();
                            reader.onload = () => {
                                try {
                                    const errorData = JSON.parse(reader.result);
                                    ElMessage.error(errorData.msg || '生成文件失败');
                                } catch (e) {
                                    ElMessage.error('生成文件失败');
                                }
                            };
                            reader.readAsText(error.response.data);
                        } else {
                            ElMessage.error(error.message || '生成文件失败');
                        }
                    } finally {
                        loading.value = false;
                    }
                }
            });
        };

        // 重置表单
        const resetForm = () => {
            proxy.$refs.mockForm.resetFields()
        }

        return {
            formData,
            loading,
            privacyColumns,
            commonColumns,
            handleSubmit,
            resetForm,
            validateDataLines
        }
    }
})
</script>

<style lang="less" scoped>
.mock-files {
    padding: 20px;

    .mock-form {
        margin: 0 auto;
        background-color: #fff;
        padding: 20px;

        .form-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 20px;
            padding-left: 10px;
        }

        .tip-text {
            margin-top: 5px;
            color: #909399;
            font-size: 12px;
        }
    }
}
</style>