<template>
    <div class="qrcode-container">
        <el-card class="qrcode-form">
            <template #header>
                <div class="card-header">
                    <span>二维码生成器</span>
                </div>
            </template>
            
            <el-form :model="formData" label-width="120px">
                <el-form-item label="内容类型">
                    <el-radio-group v-model="formData.type">
                        <el-radio label="text">文本</el-radio>
                        <el-radio label="url">链接</el-radio>
                    </el-radio-group>
                </el-form-item>
                
                <el-form-item 
                    :label="formData.type === 'url' ? '链接地址' : '文本内容'"
                    prop="content"
                    :rules="[
                        { required: true, message: '请输入内容', trigger: 'blur' },
                        { validator: validateContent, trigger: 'blur' }
                    ]"
                >
                    <el-input
                        v-model="formData.content"
                        :type="formData.type === 'text' ? 'textarea' : 'text'"
                        :rows="3"
                        :placeholder="formData.type === 'url' ? '请输入链接地址' : '请输入文本内容'"
                    />
                </el-form-item>
                
                <el-form-item label="二维码大小">
                    <el-slider
                        v-model="formData.size"
                        :min="100"
                        :max="400"
                        :step="10"
                        show-input
                    />
                </el-form-item>
                
                <el-form-item label="容错级别">
                    <el-select v-model="formData.errorLevel">
                        <el-option label="低" value="L" />
                        <el-option label="中" value="M" />
                        <el-option label="高" value="Q" />
                        <el-option label="最高" value="H" />
                    </el-select>
                </el-form-item>
                
                <el-form-item>
                    <el-button type="primary" @click="generateQRCode" :disabled="!formData.content">
                        生成二维码
                    </el-button>
                    <el-button @click="resetForm">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>

        <el-card class="qrcode-result" v-if="showQRCode">
            <template #header>
                <div class="card-header">
                    <span>生成结果</span>
                    <el-button type="primary" link @click="downloadQRCode">
                        下载二维码
                    </el-button>
                </div>
            </template>
            
            <div class="qrcode-wrapper" ref="qrcodeWrapper">
                <qrcode-vue
                    :value="formData.content"
                    :size="formData.size"
                    :level="formData.errorLevel"
                    render-as="svg"
                />
            </div>
        </el-card>
    </div>
</template>

<script>
import { defineComponent, ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import QrcodeVue from 'qrcode.vue';

export default defineComponent({
    name: 'QRCode',
    components: {
        QrcodeVue
    },
    setup() {
        const formData = reactive({
            type: 'text',
            content: '',
            size: 200,
            errorLevel: 'M'
        });

        const showQRCode = ref(false);
        const qrcodeWrapper = ref(null);

        // 验证输入内容
        const validateContent = (rule, value, callback) => {
            if (formData.type === 'url') {
                try {
                    new URL(value);
                    callback();
                } catch (err) {
                    callback(new Error('请输入有效的URL地址'));
                }
            } else {
                callback();
            }
        };

        // 生成二维码
        const generateQRCode = () => {
            if (!formData.content) {
                ElMessage.warning('请输入内容');
                return;
            }
            showQRCode.value = true;
        };

        // 下载二维码
        const downloadQRCode = () => {
            try {
                const svg = qrcodeWrapper.value.querySelector('svg');
                const svgData = new XMLSerializer().serializeToString(svg);
                const blob = new Blob([svgData], { type: 'image/svg+xml' });
                const url = URL.createObjectURL(blob);
                
                const link = document.createElement('a');
                link.href = url;
                link.download = 'qrcode.svg';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                
                ElMessage.success('下载成功');
            } catch (err) {
                ElMessage.error('下载失败');
            }
        };

        // 重置表单
        const resetForm = () => {
            formData.type = 'text';
            formData.content = '';
            formData.size = 200;
            formData.errorLevel = 'M';
            showQRCode.value = false;
        };

        return {
            formData,
            showQRCode,
            qrcodeWrapper,
            validateContent,
            generateQRCode,
            downloadQRCode,
            resetForm
        };
    }
});
</script>

<style lang="less" scoped>
.qrcode-container {
    padding: 20px;
    
    .qrcode-form {
        margin-bottom: 20px;
        
        .el-form-item {
            margin-bottom: 22px;
        }
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .qrcode-result {
        margin-top: 20px;
        
        .qrcode-wrapper {
            display: flex;
            justify-content: center;
            padding: 20px;
        }
    }
}
</style>
