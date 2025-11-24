<template>
    <div class="idcard-container">
        <el-card class="idcard-form">
            <template #header>
                <div class="card-header">
                    <span>身份证号码生成器</span>
                </div>
            </template>
            
            <el-form :model="formData" label-width="120px">
                <el-form-item label="出生日期">
                    <el-date-picker
                        v-model="formData.birthday"
                        type="date"
                        placeholder="选择出生日期"
                        format="YYYY-MM-DD"
                        value-format="YYYYMMDD"
                    />
                </el-form-item>
                
                <el-form-item label="性别">
                    <el-radio-group v-model="formData.gender">
                        <el-radio :label="1">男</el-radio>
                        <el-radio :label="2">女</el-radio>
                    </el-radio-group>
                </el-form-item>
                
                <el-form-item label="地区">
                    <el-cascader
                        v-model="formData.region"
                        :options="regionOptions"
                        placeholder="请选择地区"
                    />
                </el-form-item>
                
                <el-form-item label="生成数量">
                    <el-input-number 
                        v-model="formData.count" 
                        :min="1" 
                        :max="100"
                        controls-position="right"
                    />
                </el-form-item>
                
                <el-form-item>
                    <el-button type="primary" @click="generateIds">生成身份证号</el-button>
                    <el-button @click="resetForm">重置</el-button>
                </el-form-item>
            </el-form>
        </el-card>

        <el-card class="result-list" v-if="generatedIds.length">
            <template #header>
                <div class="card-header">
                    <span>生成结果</span>
                    <el-button type="primary" link @click="copyToClipboard">
                        复制全部
                    </el-button>
                </div>
            </template>
            
            <el-table :data="generatedIds" style="width: 100%">
                <el-table-column prop="id" label="身份证号码" />
                <el-table-column prop="gender" label="性别" width="100" />
                <el-table-column prop="birthday" label="出生日期" width="120" />
                <el-table-column prop="region" label="地区" width="200" />
                <el-table-column fixed="right" label="操作" width="120">
                    <template #default="scope">
                        <el-button type="primary" link @click="copyId(scope.row.id)">
                            复制
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>
    </div>
</template>

<script>
import { defineComponent, ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';

export default defineComponent({
    name: 'IdCard',
    setup() {
        const formData = reactive({
            birthday: '',
            gender: 1,
            region: [],
            count: 1
        });

        const generatedIds = ref([]);

        // 示例地区数据，实际使用时需要完整的地区数据
        const regionOptions = [
            {
                value: '110000',
                label: '北京市',
                children: [{
                    value: '110100',
                    label: '北京市',
                    children: [{
                        value: '110101',
                        label: '东城区'
                    }]
                }]
            }
            // ... 其他地区数据
        ];

        // 生成身份证号
        const generateIds = () => {
            if (!formData.birthday || !formData.region.length) {
                ElMessage.warning('请填写完整信息');
                return;
            }

            const results = [];
            for (let i = 0; i < formData.count; i++) {
                const id = generateSingleId();
                results.push({
                    id,
                    gender: formData.gender === 1 ? '男' : '女',
                    birthday: formatDate(formData.birthday),
                    region: formData.region.map(r => 
                        findRegionLabel(r, regionOptions)
                    ).join(' / ')
                });
            }
            generatedIds.value = results;
        };

        // 生成单个身份证号
        const generateSingleId = () => {
            const areaCode = formData.region[formData.region.length - 1];
            const birthday = formData.birthday;
            const randomNum = String(Math.floor(Math.random() * 999)).padStart(3, '0');
            const genderNum = formData.gender === 1 ? 
                String(Math.floor(Math.random() * 5) * 2 + 1) : 
                String(Math.floor(Math.random() * 5) * 2);
            
            const base = `${areaCode}${birthday}${randomNum}${genderNum}`;
            return base + generateCheckCode(base);
        };

        // 生成校验码
        const generateCheckCode = (id17) => {
            const weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
            const codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
            
            let sum = 0;
            for (let i = 0; i < 17; i++) {
                sum += parseInt(id17[i]) * weights[i];
            }
            
            return codes[sum % 11];
        };

        // 格式化日期
        const formatDate = (dateStr) => {
            return `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6)}`;
        };

        // 查找地区标签
        const findRegionLabel = (value, options) => {
            for (const option of options) {
                if (option.value === value) return option.label;
                if (option.children) {
                    const label = findRegionLabel(value, option.children);
                    if (label) return label;
                }
            }
            return '';
        };

        // 复制单个身份证号
        const copyId = async (id) => {
            try {
                await navigator.clipboard.writeText(id);
                ElMessage.success('复制成功');
            } catch (err) {
                ElMessage.error('复制失败');
            }
        };

        // 复制所有身份证号
        const copyToClipboard = async () => {
            try {
                const text = generatedIds.value
                    .map(item => item.id)
                    .join('\n');
                await navigator.clipboard.writeText(text);
                ElMessage.success('复制成功');
            } catch (err) {
                ElMessage.error('复制失败');
            }
        };

        // 重置表单
        const resetForm = () => {
            formData.birthday = '';
            formData.gender = 1;
            formData.region = [];
            formData.count = 1;
            generatedIds.value = [];
        };

        return {
            formData,
            regionOptions,
            generatedIds,
            generateIds,
            copyId,
            copyToClipboard,
            resetForm
        };
    }
});
</script>

<style lang="less" scoped>
.idcard-container {
    padding: 20px;
    
    .idcard-form {
        margin-bottom: 20px;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .result-list {
        margin-top: 20px;
    }
}
</style>
