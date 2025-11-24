<template>
    <div class="mock-business">
        <div class="mock-content">
            <!-- 左侧造数区域 -->
            <div class="mock-forms">
                <!-- 预入职造数卡片 -->
                <el-card class="mock-card">
                    <div class="card-content">
                        <!-- 左侧表单 -->
                        <div class="form-section">
                            <div class="section-header">
                                <span>预入职造数</span>
                            </div>
                            <el-form :model="preHireForm" ref="preHireFormRef" label-width="120px">
                                <el-form-item label="造数类型" prop="mock_type" :rules="[
                                    { required: true, message: '请选择造数类型' }
                                ]">
                                    <el-radio-group v-model="preHireForm.mock_type">
                                        <el-radio label="single">单条造数</el-radio>
                                        <el-radio label="batch">批量造数</el-radio>
                                    </el-radio-group>
                                </el-form-item>

                                <template v-if="preHireForm.mock_type === 'single'">
                                    <el-form-item label="用户名" prop="username" :rules="[
                                        { required: true, message: '请输入用户名' }
                                    ]">
                                        <el-input v-model="preHireForm.username" placeholder="请输入用户名" />
                                    </el-form-item>

                                    <el-form-item label="手机号" prop="phone" :rules="[
                                        { required: true, message: '请输入手机号' },
                                        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' }
                                    ]">
                                        <el-input v-model="preHireForm.phone" placeholder="请输入手机号" />
                                    </el-form-item>

                                    <el-form-item>
                                        <div class="switch-group">
                                            <div class="switch-item">
                                                <span>执行入职</span>
                                                <el-switch v-model="preHireForm.execute_hire" />
                                            </div>
                                            <div class="switch-item">
                                                <span>天门解封</span>
                                                <el-switch v-model="preHireForm.unlock_tianmen" />
                                            </div>
                                        </div>
                                    </el-form-item>
                                </template>

                                <template v-else>
                                    <el-form-item label="批量数据" prop="batch_data" :rules="[
                                        { required: true, message: '请输入批量数据' }
                                    ]">
                                        <el-input
                                            v-model="preHireForm.batch_data"
                                            type="textarea"
                                            :rows="6"
                                            placeholder="请输入批量数据，每行一条记录，格式：用户名,手机号"
                                        />
                                        <div class="tip-text">示例：张三,13800138000</div>
                                    </el-form-item>

                                    <el-form-item>
                                        <div class="switch-group">
                                            <div class="switch-item">
                                                <span>执行入职</span>
                                                <el-switch v-model="preHireForm.execute_hire" />
                                            </div>
                                            <div class="switch-item">
                                                <span>天门解封</span>
                                                <el-switch v-model="preHireForm.unlock_tianmen" />
                                            </div>
                                        </div>
                                    </el-form-item>
                                </template>

                                <el-form-item class="form-buttons">
                                    <el-button type="primary" @click="handlePreHireSubmit" :loading="preHireLoading">
                                        确认
                                    </el-button>
                                    <el-button @click="resetPreHireForm">重置</el-button>
                                </el-form-item>
                            </el-form>
                        </div>
                        
                        <!-- 右侧结果 -->
                        <div class="result-section">
                            <div class="section-header">
                                <span>执行结果</span>
                                <el-button type="primary" link @click="clearPreHireResults">清空</el-button>
                            </div>
                            <div class="result-content">
                                <div v-if="preHireResults.length === 0" class="no-result">
                                    暂无执行结果
                                </div>
                                <div v-else class="result-list">
                                    <div 
                                        v-for="(result, index) in preHireResults" 
                                        :key="index"
                                        class="result-item"
                                        :class="result.status"
                                    >
                                        <div class="result-time">{{ result.time }}</div>
                                        <div class="result-message">{{ result.message }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </el-card>

                <!-- OA造数卡片 -->
                <el-card class="mock-card">
                    <div class="card-content">
                        <!-- 左侧表单 -->
                        <div class="form-section">
                            <div class="section-header">
                                <span>OA造数</span>
                            </div>
                            <el-form :model="oaForm" ref="oaFormRef" label-width="120px">
                                <el-form-item label="流程名称" prop="flow_name_type" :rules="[
                                    { required: true, message: '请选择流程名称类型' }
                                ]">
                                    <el-radio-group v-model="oaForm.flow_name_type">
                                        <el-radio label="manual">手动输入</el-radio>
                                        <el-radio label="auto">自动生成</el-radio>
                                    </el-radio-group>
                                </el-form-item>

                                <el-form-item 
                                    v-if="oaForm.flow_name_type === 'manual'"
                                    label="流程名称" 
                                    prop="flow_name"
                                    :rules="[{ required: true, message: '请输入流程名称' }]"
                                >
                                    <el-input v-model="oaForm.flow_name" placeholder="请输入流程名称" />
                                </el-form-item>

                                <el-form-item label="流程类型" prop="flow_type" :rules="[
                                    { required: true, message: '请选择流程类型' }
                                ]">
                                    <el-select v-model="oaForm.flow_type" placeholder="请选择流程类型">
                                        <el-option 
                                            v-for="item in flowTypes" 
                                            :key="item.value" 
                                            :label="item.label" 
                                            :value="item.value"
                                        />
                                    </el-select>
                                </el-form-item>

                                <el-form-item class="form-buttons">
                                    <el-button type="primary" @click="handleOaSubmit" :loading="oaLoading">
                                        确认
                                    </el-button>
                                    <el-button @click="resetOaForm">重置</el-button>
                                </el-form-item>
                            </el-form>
                        </div>
                        
                        <!-- 右侧结果 -->
                        <div class="result-section">
                            <div class="section-header">
                                <span>执行结果</span>
                                <el-button type="primary" link @click="clearOaResults">清空</el-button>
                            </div>
                            <div class="result-content">
                                <div v-if="oaResults.length === 0" class="no-result">
                                    暂无执行结果
                                </div>
                                <div v-else class="result-list">
                                    <div 
                                        v-for="(result, index) in oaResults" 
                                        :key="index"
                                        class="result-item"
                                        :class="result.status"
                                    >
                                        <div class="result-time">{{ result.time }}</div>
                                        <div class="result-message">{{ result.message }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </el-card>

                <!-- 应收造数卡片 -->
                <el-card class="mock-card">
                    <div class="card-content">
                        <!-- 左侧表单 -->
                        <div class="form-section">
                            <div class="section-header">
                                <span>应收造数</span>
                            </div>
                            <el-form :model="financeForm" ref="financeFormRef" label-width="120px">
                                <el-form-item label="DSP名称" prop="dsp_name" :rules="[
                                    { required: true, message: '请输入DSP名称' }
                                ]">
                                    <el-input v-model="financeForm.dsp_name" placeholder="请输入DSP名称" />
                                </el-form-item>

                                <el-form-item label="DSP类型" prop="dsp_type" :rules="[
                                    { required: true, message: '请输入DSP类型' }
                                ]">
                                    <el-input v-model="financeForm.dsp_type" placeholder="请输入DSP类型" />
                                </el-form-item>

                                <el-form-item label="代理商" prop="agent" :rules="[
                                    { required: true, message: '请输入代理商' }
                                ]">
                                    <el-input v-model="financeForm.agent" placeholder="请输入代理商" />
                                </el-form-item>

                                <el-form-item label="日期列表" prop="date_list" :rules="[
                                    { required: true, message: '请选择日期范围' }
                                ]">
                                    <el-date-picker
                                        v-model="financeForm.date_list"
                                        type="daterange"
                                        range-separator="至"
                                        start-placeholder="开始日期"
                                        end-placeholder="结束日期"
                                        value-format="YYYY-MM-DD"
                                    />
                                </el-form-item>

                                <el-form-item label="收入" prop="income" :rules="[
                                    { required: true, message: '请输入收入' }
                                ]">
                                    <el-input-number 
                                        v-model="financeForm.income" 
                                        :min="0"
                                        :precision="2"
                                        :step="100"
                                        placeholder="请输入收入"
                                    />
                                </el-form-item>

                                <el-form-item label="点击" prop="clicks" :rules="[
                                    { required: true, message: '请输入点击数' }
                                ]">
                                    <el-input-number 
                                        v-model="financeForm.clicks" 
                                        :min="0"
                                        :precision="0"
                                        :step="100"
                                        placeholder="请输入点击数"
                                    />
                                </el-form-item>

                                <el-form-item class="form-buttons">
                                    <el-button type="primary" @click="handleFinanceSubmit" :loading="financeLoading">
                                        确认
                                    </el-button>
                                    <el-button @click="resetFinanceForm">重置</el-button>
                                </el-form-item>
                            </el-form>
                        </div>
                        
                        <!-- 右侧结果 -->
                        <div class="result-section">
                            <div class="section-header">
                                <span>执行结果</span>
                                <el-button type="primary" link @click="clearFinanceResults">清空</el-button>
                            </div>
                            <div class="result-content">
                                <div v-if="financeResults.length === 0" class="no-result">
                                    暂无执行结果
                                </div>
                                <div v-else class="result-list">
                                    <div 
                                        v-for="(result, index) in financeResults" 
                                        :key="index"
                                        class="result-item"
                                        :class="result.status"
                                    >
                                        <div class="result-time">{{ result.time }}</div>
                                        <div class="result-message">{{ result.message }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent, ref, reactive, getCurrentInstance, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default defineComponent({
    name: 'MockBusiness',
    setup() {
        const { proxy } = getCurrentInstance()
        const preHireResults = ref([])
        const oaResults = ref([])
        const financeResults = ref([])

        const addPreHireResult = (message, status = 'success') => {
            preHireResults.value.unshift({
                time: new Date().toLocaleTimeString(),
                message,
                status
            })
        }

        // 预入职表单数据
        const preHireForm = reactive({
            mock_type: 'single',
            username: '',
            phone: '',
            execute_hire: false,
            unlock_tianmen: false,
            batch_data: ''
        })
        const preHireLoading = ref(false)
        const preHireFormRef = ref(null)

        // OA表单数据
        const oaForm = reactive({
            flow_name_type: 'auto',
            flow_name: '',
            flow_type: ''
        })
        const oaLoading = ref(false)
        const oaFormRef = ref(null)
        const flowTypes = ref([])

        // 应收表单数据
        const financeForm = reactive({
            dsp_name: '',
            dsp_type: '',
            agent: '',
            date_list: [],
            income: null,
            clicks: null
        })
        const financeLoading = ref(false)
        const financeFormRef = ref(null)

        // 获取OA流程类型列表
        const getFlowTypes = async () => {
            try {
                const res = await proxy.$api.getOaFlowTypes()
                if (res.code === 200) {
                    flowTypes.value = res.data
                }
            } catch (error) {
                console.error('获取流程类型失败:', error)
            }
        }

        // 预入职提交
        const handlePreHireSubmit = () => {
            preHireFormRef.value.validate(async (valid) => {
                if (valid) {
                    try {
                        preHireLoading.value = true
                        const res = await proxy.$api.mockDataCorehr(preHireForm)
                        if (res.code === 200) {
                            ElMessage.success('预入职造数成功')
                            addPreHireResult('执行成功')
                            resetPreHireForm()
                        } else {
                            ElMessage.error(res.msg || '预入职造数失败')
                            addPreHireResult(res.msg || '执行失败', 'error')
                        }
                    } catch (error) {
                        console.error('预入职造数错误:', error)
                        ElMessage.error('预入职造数失败')
                        addPreHireResult('执行出错', 'error')
                    } finally {
                        preHireLoading.value = false
                    }
                }
            })
        }

        // 重置预入职表单
        const resetPreHireForm = () => {
            preHireFormRef.value.resetFields()
        }

        // OA提交
        const handleOaSubmit = () => {
            oaFormRef.value.validate(async (valid) => {
                if (valid) {
                    try {
                        oaLoading.value = true
                        const res = await proxy.$api.mockDataOa(oaForm)
                        if (res.code === 200) {
                            ElMessage.success('OA造数成功')
                            resetOaForm()
                        } else {
                            ElMessage.error(res.msg || 'OA造数失败')
                        }
                    } catch (error) {
                        console.error('OA造数错误:', error)
                        ElMessage.error('OA造数失败')
                    } finally {
                        oaLoading.value = false
                    }
                }
            })
        }

        // 重置OA表单
        const resetOaForm = () => {
            oaFormRef.value.resetFields()
        }

        // 应收提交
        const handleFinanceSubmit = () => {
            financeFormRef.value.validate(async (valid) => {
                if (valid) {
                    try {
                        financeLoading.value = true
                        const res = await proxy.$api.mockDataFinance(financeForm)
                        if (res.code === 200) {
                            ElMessage.success('应收造数成功')
                            resetFinanceForm()
                        } else {
                            ElMessage.error(res.msg || '应收造数失败')
                        }
                    } catch (error) {
                        console.error('应收造数错误:', error)
                        ElMessage.error('应收造数失败')
                    } finally {
                        financeLoading.value = false
                    }
                }
            })
        }

        // 重置应收表单
        const resetFinanceForm = () => {
            financeFormRef.value.resetFields()
        }

        onMounted(() => {
            getFlowTypes()
        })

        return {
            preHireForm,
            preHireLoading,
            preHireFormRef,
            handlePreHireSubmit,
            resetPreHireForm,

            oaForm,
            oaLoading,
            oaFormRef,
            flowTypes,
            handleOaSubmit,
            resetOaForm,

            financeForm,
            financeLoading,
            financeFormRef,
            handleFinanceSubmit,
            resetFinanceForm,

            preHireResults,
            oaResults,
            financeResults,
            addPreHireResult
        }
    }
})
</script>

<style lang="less" scoped>
.mock-business {
    padding: 20px;
    display: flex;
    flex-direction: column;

    .mock-card {
        margin-bottom: 12px;

        &:last-child {
            margin-bottom: 0;  // 最后一个卡片不需要底部边距
        }

        .card-content {
            display: flex;
            gap: 20px;

            .form-section {
                flex: 3;
                min-width: 600px;
            }

            .result-section {
                flex: 1;
                width: 25%;
                min-width: 250px;
                border-left: 1px solid #EBEEF5;
                padding-left: 20px;
            }
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            
            span {
                font-size: 16px;
                font-weight: bold;
            }
        }

        .result-content {
            height: 300px;
            overflow-y: auto;
            position: relative;

            .no-result {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: #909399;
                white-space: nowrap;
            }

            .result-list {
                .result-item {
                    padding: 8px;
                    border-bottom: 1px solid #EBEEF5;
                    
                    &.success {
                        border-left: 3px solid #67C23A;
                    }

                    &.error {
                        border-left: 3px solid #F56C6C;
                    }

                    .result-time {
                        font-size: 12px;
                        color: #909399;
                    }

                    .result-message {
                        color: #606266;
                        margin-top: 4px;
                    }
                }
            }
        }
    }

    .el-form {
        max-width: 600px;
        margin: 0 auto;
    }

    .el-date-picker {
        width: 100%;
    }

    .switch-group {
        display: flex;
        gap: 20px;

        .switch-item {
            display: flex;
            align-items: center;
            gap: 8px;

            span {
                color: #606266;
                font-size: 14px;
            }
        }
    }

    .tip-text {
        margin-top: 5px;
        color: #909399;
        font-size: 12px;
    }

    .form-buttons {
        margin-bottom: 0;
        
        :deep(.el-form-item__content) {
            justify-content: center;
            margin-left: 0 !important;
        }
    }
}
</style>
