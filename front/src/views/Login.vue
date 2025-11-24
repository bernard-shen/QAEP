<template>
    <div class="login-page">
        <el-form ref="formRef" :model="loginForm" class="login-container">
            <h3>系统登录</h3>
            <el-form-item>
                <el-input type="input" placeholder="请输入账号" v-model="loginForm.username" />
            </el-form-item>
            <el-form-item>
                <el-input type="password" placeholder="请输入密码" v-model="loginForm.password" />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="login">登录</el-button>
                <el-button @click="showRegisterDialog">注册</el-button>
            </el-form-item>
        </el-form>

        <!-- 注册弹窗 -->
        <el-dialog
            v-model="registerVisible"
            title="用户注册"
            width="400px"
            :close-on-click-modal="false"
            @closed="handleDialogClosed"
        >
            <el-form 
                ref="registerFormRef"
                :model="registerForm"
                :rules="registerRules"
                label-width="80px"
            >
                <el-form-item label="用户名" prop="username">
                    <el-input 
                        v-model="registerForm.username" 
                        placeholder="请输入用户名"
                        name="register_username"
                        autocomplete="off" 
                    />
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                    <el-input v-model="registerForm.phone" placeholder="请输入手机号" />
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="registerForm.email" placeholder="请输入邮箱" />
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input 
                        v-model="registerForm.password" 
                        type="password" 
                        placeholder="请输入密码"
                        name="register_password"
                        autocomplete="new-password"
                        show-password 
                    />
                </el-form-item>
                <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input 
                        v-model="registerForm.confirmPassword" 
                        type="password" 
                        placeholder="请再次输入密码"
                        name="register_confirm_password"
                        autocomplete="new-password"
                        show-password 
                    />
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="registerVisible = false">取消</el-button>
                    <el-button type="primary" @click="handleRegister" :loading="registerLoading">
                        确认
                    </el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>


<script>
import { reactive, ref, getCurrentInstance } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { userApi, systemApi } from '@/api'  // 导入需要的API模块

export default {
    setup() {
        const store = useStore()
        const router = useRouter()
        const registerFormRef = ref(null)
        const registerVisible = ref(false)
        const registerLoading = ref(false)

        const loginForm = reactive({
            username: "",
            password: ""
        })
        
        const registerForm = reactive({
            username: '',
            phone: '',
            email: '',
            password: '',
            confirmPassword: ''
        })

        // 注册表单验证规则
        const registerRules = {
            username: [
                { required: true, message: '请输入用户名', trigger: 'blur' },
                { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
            ],
            phone: [
                { required: true, message: '请输入手机号', trigger: 'blur' },
                { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
            ],
            email: [
                { required: true, message: '请输入邮箱', trigger: 'blur' },
                { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
            ],
            password: [
                { required: true, message: '请输入密码', trigger: 'blur' },
                { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
            ],
            confirmPassword: [
                { required: true, message: '请再次输入密码', trigger: 'blur' },
                {
                    validator: (rule, value, callback) => {
                        if (value !== registerForm.password) {
                            callback(new Error('两次输入的密码不一致'))
                        } else {
                            callback()
                        }
                    },
                    trigger: 'blur'
                }
            ]
        }
        
        // 显示注册弹窗
        const showRegisterDialog = () => {
            registerVisible.value = true
        }

        // 处理注册
        const handleRegister = () => {
            registerFormRef.value.validate(async (valid) => {
                if (valid) {
                    try {
                        registerLoading.value = true
                        const res = await userApi.register({
                            username: registerForm.username,
                            password: registerForm.password,
                            phone: registerForm.phone,
                            email: registerForm.email
                        })

                        if (res.code === 200) {
                            ElMessage.success('注册成功！')
                            registerVisible.value = false
                        } else {
                            ElMessage.error(res.message || '注册失败')
                        }
                    } catch (error) {
                        console.error('注册错误:', error)
                        ElMessage.error('注册失败，请稍后重试')
                    } finally {
                        registerLoading.value = false
                    }
                }
            })
        }

        const login = async () => {
            try {
                if (!loginForm.username || !loginForm.password) {
                    ElMessage.error('用户名和密码不能为空');
                    return;
                }

                const login_res = await userApi.login(loginForm);
                console.log('登录返回:', login_res);
                
                if (login_res.code === 200) {
                    store.commit('setMenu', login_res.data.menus);
                    store.commit('addMenu', router);
                    store.commit('setToken', login_res.data.token);
                    
                    // 修改获取用户详情的调用，确保传递正确的参数
                    const params = {
                        username: loginForm.username.trim()  // 添加 trim() 去除可能的空格
                    };
                    console.log('获取用户详情参数:', params);
                    
                    try {
                        const res_user = await systemApi.getUserDetail(params);
                        console.log('用户详情返回:', res_user);
                        
                        if (res_user.code === 200 && res_user.data && res_user.data.length > 0) {
                            store.commit('setUserInfo', res_user.data[0]);
                            console.log('存储用户信息:', res_user.data[0]);
                            
                            router.push({ name: 'home' });
                            ElMessage({
                                showClose: true,
                                message: "登录成功！",
                                type: "success",
                            });
                        } else {
                            // 添加更详细的错误信息
                            console.error('获取用户详情失败: 未找到用户信息');
                            ElMessage.error(`未找到用户 ${params.username} 的详细信息`);
                            return;
                        }
                    } catch (error) {
                        console.error('获取用户详情错误:', error);
                        ElMessage.error('获取用户详情失败');
                        return;
                    }
                } else {
                    ElMessage({
                        showClose: true,
                        message: login_res.message || "用户名或密码错误！",
                        type: "error",
                    });
                }
            } catch (error) {
                console.error('登录错误:', error);
                ElMessage({
                    showClose: true,
                    message: "登录失败，请稍后重试！",
                    type: "error",
                });
            }
        }

        // 弹窗关闭时清空表单
        const handleDialogClosed = () => {
            registerFormRef.value?.resetFields()
        }

        return {
            loginForm,
            registerForm,
            registerFormRef,
            registerVisible,
            registerLoading,
            registerRules,
            login,
            showRegisterDialog,
            handleRegister,
            handleDialogClosed
        }
    }
}
</script>















<style lang="less" scoped>
.login-page {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
}

.login-container {
    width: 350px;
    background-color: #fff;
    border: 1px solid #eaeaea;
    border-radius: 15px;
    padding: 35px 35px 15px 35px;
    box-shadow: 0 0 25px #cacaca;

    h3 {
        text-align: center;
        margin-bottom: 20px;
        color: #505450;
    }

    :deep(.el-form-item__content) {
        justify-content: center;
        
        .el-button {
            margin: 0 8px;  // 稍微调整按钮间距
        }
    }
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
}
</style>