<template>
    <el-row class="home" :gutter="20">
        <el-col :span="7" style="margin-top: 20px">
            <el-card shadow="hover">
                <div class="user">
                    <img src="../../assets/images/user.png" alt="" />
                    <div class="user-info">
                        <p class="name" style="margin-bottom: 10px;">{{ userInfo['username'] }}</p>
                        <p class="role">{{ userInfo['role'] }}</p>
                    </div>
                </div>
                <div class="login-info">
                    <p>手机号:<span>{{ userInfo['phone'] }}</span></p>
                    <p>邮箱:<span>{{ userInfo['email'] }}</span></p>
                </div>
            </el-card>
            <el-card class="visitSet" shadow="hover" style="margin-top: 20px" height="450px">
                <p style="margin-bottom: 20px;">快捷导航</p>
                <div class="quick-nav">
                    <div class="nav-item" @click="navigateTo('/api/mng')">
                        <i class="el-icon-connection"></i>
                        <span>接口管理</span>
                    </div>
                    <div class="nav-item" @click="navigateTo('/mock/files')">
                        <i class="el-icon-document"></i>
                        <span>文件造数</span>
                    </div>
                    <div class="nav-item" @click="navigateTo('/mock/business')">
                        <i class="el-icon-data-analysis"></i>
                        <span>业务造数</span>
                    </div>
                    <div class="nav-item" @click="navigateTo('/devices/mng')">
                        <i class="el-icon-monitor"></i>
                        <span>设备管理</span>
                            </div>
                    <div class="nav-item" @click="navigateTo('/scene/mng')">
                        <i class="el-icon-film"></i>
                        <span>场景管理</span>
                            </div>
                    <div class="nav-item" @click="navigateTo('/sys/users')">
                        <i class="el-icon-user"></i>
                        <span>用户管理</span>
                            </div>
                            </div>
                        </el-card>
                    </el-col>

        <el-col :span="17" style="margin-top: 20px" class="right-num">
            <el-card class="statistics-card">
                <el-row :gutter="20">
                    <el-col :span="6">
                        <el-card shadow="hover" class="stat-item">
                            <div class="stat-header">
                                <span>可用接口</span>
                                <el-icon class="icon"><Clock /></el-icon>
                            </div>
                            <div class="stat-content">
                                <div class="current">125</div>

                                <!-- <div class="current">{{ cardSetData['apis'] }}</div> -->
                                <div class="total">接口总数: 362</div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="6">
                        <el-card shadow="hover" class="stat-item">
                            <div class="stat-header">
                                <span>可用设备</span>
                                <el-icon class="icon"><CreditCard /></el-icon>
                            </div>
                            <div class="stat-content">
                                <div class="current">6</div>
                                <div class="total">总设备数: 32</div>
                                <!-- <div class="current">{{ cardSetData['machine_free'] }}</div>
                                <div class="total">总设备数: {{ cardSetData['machine_total'] }}</div> -->
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="6">
                        <el-card shadow="hover" class="stat-item">
                            <div class="stat-header">
                                <span>业务造数</span>
                                <!-- <el-icon class="icon"><Download /></el-icon> -->
                            </div>
                            <div class="stat-content">
                                <div class="current">8,000</div>
                                <div class="total">造数总量: 120,000</div>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="6">
                        <el-card shadow="hover" class="stat-item">
                            <div class="stat-header">
                                <span>场景用例</span>
                                <el-icon class="icon"><PieChart /></el-icon>
                            </div>
                            <div class="stat-content">
                                <div class="current">72</div>
                                <div class="total">总用例数: 1234</div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </el-card>

            <el-card style="height: 260px">
                <div class="chart-header">
                    <div class="chart-title">
                        <span>造数统计</span>
                    </div>
                    <div class="time-filter">
                        <span 
                            :class="{ active: timeUnit === 'day' }" 
                            @click="switchTimeUnit('day')"
                        >按天</span>
                        <span 
                            :class="{ active: timeUnit === 'month' }" 
                            @click="switchTimeUnit('month')"
                        >按月</span>
                    </div>
                </div>
                <div ref="trend_chart" style="height: 220px"></div>
            </el-card>

            <div class="graph">
                <el-card style="height: 260px">
                    <div class="chart-title">接口分布</div>
                    <div ref="api_echart" style="height: 240px"></div>
                </el-card>
                <el-card style="height: 260px">
                    <div class="chart-title">用例分布</div>
                    <div ref="data_echart" style="height: 240px"></div>
                </el-card>
            </div>
        </el-col>
    </el-row>
</template>
<script>
import {
    defineComponent,
    getCurrentInstance,
    onMounted,
    reactive,
    ref,
    onUnmounted,
} from "vue";
import * as echarts from "echarts";
import { Clock, CreditCard, Download, PieChart } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default defineComponent({
    components: {
        Clock,
        CreditCard,
        Download,
        PieChart
    },
    setup() {
        const { proxy } = getCurrentInstance();
        let cardSetData = ref([]);
        const userInfo = ref({});
        const chartData = ref(null);
        const apiChart = ref(null);
        const caseChart = ref(null);
        let lineData = reactive({
            xData: [],
            series: [],
            legend: [],
        });
        let apiData = reactive({
            ydata: []
        });
        let mockData = reactive({
            xdata: [],
            ydata: []
        })
        const timeUnit = ref('day'); // day 或 month
        const trendChart = ref(null);

        // 获取首页count数据
        const getHomeData = async () => {
            try {
                const res = await proxy.$api.getHomeData();
                if (res.code === 200) {
                    // 更新统计数据
                    cardSetData.value = {
                        apis: res.data?.apis || 0,
                        machine_free: res.data?.machine_free || 0,
                        machine_total: res.data?.machine_total || 0,
                        mock_data: res.data?.mock_data || 0,
                        mock_total: res.data?.mock_total || 0,
                        cases: res.data?.cases || 0,
                        case_total: res.data?.case_total || 0
                    };
                } else {
                    ElMessage.error(res.msg || '获取首页数据失败');
                }
            } catch (error) {
                console.error('获取首页数据失败:', error);
                ElMessage.error('获取首页数据失败，请稍后重试');
            }
        };

        const getLineData = async () => {
            let res = await proxy.$api.getLineData({ "choice": "天" });
            console.log(res, 'lineData')
        };

        const getUserInfo = () => {
            if (!localStorage.getItem('userinfo')) {
                return
            }
            const login_info = JSON.parse(localStorage.getItem('userinfo'));
            userInfo.value = login_info;
        };

        const navigateTo = (path) => {
            proxy.$router.push(path);
        };

        // 获取趋势数据
        const getTrendData = async () => {
            try {
                const res = await proxy.$api.getTrendData();
                if (res.code === 200) {
                    // 格式化日期数据
                    const now = new Date();
                    let formattedDates = [];
                    
                    if (timeUnit.value === 'day') {
                        // 获取最近10天的日期
                        for (let i = 9; i >= 0; i--) {
                            const date = new Date(now);
                            date.setDate(date.getDate() - i);
                            const month = String(date.getMonth() + 1).padStart(2, '0');
                            const day = String(date.getDate()).padStart(2, '0');
                            formattedDates.push(`${month}/${day}`);
                        }
                    } else {
                        // 获取最近10个月的日期
                        for (let i = 9; i >= 0; i--) {
                            const date = new Date(now);
                            date.setMonth(date.getMonth() - i);
                            const year = date.getFullYear();
                            const month = String(date.getMonth() + 1).padStart(2, '0');
                            formattedDates.push(`${year}/${month}`);
                        }
                    }

                    // 更新响应数据中的日期列表
                    res.data.date_list = formattedDates;
                    res.data.month_list = formattedDates;

                    // 更新图表数据
                    chartData.value = res.data;
                    renderChart(res.data);
                } else {
                    ElMessage.error(res.msg || '获取趋势数据失败');
                }
            } catch (error) {
                console.error('获取趋势数据失败:', error);
                ElMessage.error('获取趋势数据失败，请稍后重试');
            }
        };

        // 切换时间单位
        const switchTimeUnit = (unit) => {
            timeUnit.value = unit;
            getTrendData();
        };

        // 渲染图表
        const renderChart = (data) => {
            if (!proxy.$refs.trend_chart) return;
            const chart = echarts.init(proxy.$refs.trend_chart);
            const option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    }
                },
                legend: {
                    data: ['数据库造数', '文件造数', '业务造数']
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '15%',
                    top: '10%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    axisLabel: {
                        show: true,
                        interval: 0,
                        rotate: 45,
                        textStyle: {
                            fontSize: 12
                        },
                    },
                    data: timeUnit.value === 'day' 
                        ? data.date_list 
                        : data.month_list
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '数据库造数',
                        type: 'line',
                        data: timeUnit.value === 'day' 
                            ? data.sql_mock_list_by_day 
                            : data.sql_mock_list_by_month,
                        smooth: true,
                        lineStyle: { width: 2 },
                        itemStyle: { color: '#409EFF' }
                    },
                    {
                        name: '文件造数',
                        type: 'line',
                        data: timeUnit.value === 'day' 
                            ? data.file_mock_list_by_day 
                            : data.file_mock_list_by_month,
                        smooth: true,
                        lineStyle: { width: 2 },
                        itemStyle: { color: '#67C23A' }
                    },
                    {
                        name: '业务造数',
                        type: 'line',
                        data: timeUnit.value === 'day' 
                            ? data.bz_mock_list_by_day 
                            : data.bz_mock_list_by_month,
                        smooth: true,
                        lineStyle: { width: 2 },
                        itemStyle: { color: '#E6A23C' }
                    }
                ]
            };

            chart.setOption(option);
            
            // 添加窗口大小改变时的自适应
            window.addEventListener('resize', () => {
                chart.resize();
            });
        };

        // 获取并渲染接口分布数据
        const getApiDistribution = async () => {
            try {
                const res = await proxy.$api.getApiDistribution();
                if (res.code === 200) {
                    renderApiChart(res.data);
                } else {
                    ElMessage.error(res.msg || '获取接口分布数据失败');
                }
            } catch (error) {
                console.error('获取接口分布数据失败:', error);
                ElMessage.error('获取接口分布数据失败，请稍后重试');
            }
        };

        // 渲染接口分布饼图
        const renderApiChart = (data) => {
            if (!proxy.$refs.api_echart) return;
            
            const chart = echarts.init(proxy.$refs.api_echart);
            const option = {
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    left: 10,
                    top: 'center'
                },
                series: [
                    {
                        name: '接口分布',
                        type: 'pie',
                        radius: ['40%', '70%'],  // 环形图
                        avoidLabelOverlap: false,
                        itemStyle: {
                            borderRadius: 10,
                            borderColor: '#fff',
                            borderWidth: 2
                        },
                        label: {
                            show: true,
                            formatter: '{b}: {d}%'  // 显示名称和百分比
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: 20,
                                fontWeight: 'bold'
                            }
                        },
                        data: data.map(item => ({
                            name: item.business,
                            value: item.count
                        }))
                    }
                ]
            };

            chart.setOption(option);
            
            // 添加窗口大小改变时的自适应
            window.addEventListener('resize', () => {
                chart.resize();
            });
        };

        // 获取并渲染用例执行数据
        const getCaseDistribution = async () => {
            try {
                const res = await proxy.$api.getCaseDistribution();
                if (res.code === 200) {
                    renderCaseChart(res.data);
                } else {
                    ElMessage.error(res.msg || '获取用例执行数据失败');
                }
            } catch (error) {
                console.error('获取用例执行数据失败:', error);
                ElMessage.error('获取用例执行数据失败，请稍后重试');
            }
        };

        // 渲染用例执行柱状图
        const renderCaseChart = (data) => {
            if (!proxy.$refs.data_echart) return;
            
            const chart = echarts.init(proxy.$refs.data_echart);
            // 检查数据是否为空
            if (!data || data.length === 0) {
                const option = {
                    title: {
                        text: '暂无数据',
                        x: 'center',
                        y: 'center',
                        textStyle: {
                            fontSize: 14,
                            color: '#909399'
                        }
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        top: '3%',
                        containLabel: true
                    }
                };
                chart.setOption(option);
                return;
            }

            const option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '15%',
                    top: '10%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: data.map(item => item.business),
                    axisLabel: {
                        interval: 0,
                        rotate: 45,
                        textStyle: {
                            fontSize: 12
                        }
                    }
                },
                yAxis: {
                    type: 'value',
                    minInterval: 1,  // 设置最小间隔为1，避免小数
                    splitLine: {     // 网格线样式
                        lineStyle: {
                            type: 'dashed'
                        }
                    }
                },
                series: [
                    {
                        name: '用例数量',
                        type: 'bar',
                        barWidth: '60%',
                        showBackground: true,  // 显示柱状图背景
                        backgroundStyle: {
                            color: 'rgba(180, 180, 180, 0.1)'
                        },
                        data: data.map(item => ({
                            value: item.count,
                            itemStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    { offset: 0, color: '#83bff6' },
                                    { offset: 0.5, color: '#188df0' },
                                    { offset: 1, color: '#188df0' }
                                ])
                            }
                        })),
                        emphasis: {
                            itemStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    { offset: 0, color: '#2378f7' },
                                    { offset: 0.7, color: '#2378f7' },
                                    { offset: 1, color: '#83bff6' }
                                ])
                            }
                        }
                    }
                ]
            };

            chart.setOption(option);
            
            // 添加窗口大小改变时的自适应
            window.addEventListener('resize', () => {
                chart.resize();
            });
        };

        onMounted(() => {
            // 获取count数据
            getHomeData();
            // 获取echarts表格数据
            // getLineData();
            getUserInfo();
            getTrendData();
            getApiDistribution();  // 获取接口分布数据
            getCaseDistribution();  // 获取用例执行数据
        });

        onUnmounted(() => {
            // 清理所有图表的事件监听
            const charts = [
                proxy.$refs.trend_chart, 
                proxy.$refs.api_echart, 
                proxy.$refs.data_echart
            ].filter(Boolean);
            charts.forEach(chart => {
                chart && echarts.dispose(chart);
            });
            window.removeEventListener('resize', () => {
                charts.forEach(chart => chart && chart.resize());
            });
        });

        // 关于echarts 表格的渲染部分
        let lineOptions = reactive({
            // 图例文字颜色
            textStyle: {
                color: "#333",
            },
            grid: {
                left: "20%",
            },
            // 提示框
            tooltip: {
                trigger: "axis",
            },
            xAxis: {
                type: "category", // 类目轴
                data: [],
                axisLine: {
                    lineStyle: {
                        color: "#17b3a3",
                    },
                },
                axisLabel: {
                    interval: 0,
                    color: "#333",
                },
            },
            yAxis: [
                {
                    type: "value",
                    axisLine: {
                        lineStyle: {
                            color: "#17b3a3",
                        },
                    },
                },
            ],
            color: ["#2ec7c9", "#b6a2de", "#5ab1ef", "#ffb980", "#d87a80", "#8d98b3"],
            series: [],
            legend: {
                data: [],
            },
            aria: {
                show: true
            },
            title: {
                text: '近期造数',
                x: 'left',
                textStyle: {
                    fontSize: 14,
                },
            },
        });

        let apiPieOptions = reactive({
            title: {
                text: '造数统计',
                left: 'center',
                top: 0,
                textStyle: {
                    fontSize: 14,
                },
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 10,
                top: 'center',
                data: ['数据库造数', '文件造数', '业务造数']
            },
            series: [
                {
                    name: '造数统计',
                    type: 'pie',
                    radius: ['40%', '70%'],  // 设置成环形图
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: 20,
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: []
                }
            ]
        });

        let mockPieOptions = reactive({
            title: {
                text: '用例执行',
                left: 'center',
                top: 0,
                textStyle: {
                    fontSize: 14,
                },
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 10,
                top: 'center',
                data: ['成功', '失败', '阻塞']
            },
            series: [
                {
                    name: '执行结果',
                    type: 'pie',
                    radius: '50%',
                    data: [],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        });

        return {
            cardSetData,
            userInfo,
            lineData,
            chartData,
            timeUnit,
            navigateTo,
            switchTimeUnit
        };
    },
});
</script>
  


<style lang="less" scoped>
.home {
    .visitSet {
        display: block;
        .el-card {
            margin-left: 15px;
            margin-bottom: 10px;
            padding: 2px;
        }

    }

    .user {
        display: flex;
        align-items: center;
        padding-bottom: 20px;
        border-bottom: 1px solid #ccc;
        margin-bottom: 20px;

        img {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            margin-right: 40px;
        }
    }

    .login-info {
        p {
            line-height: 30px;
            font-size: 14px;
            color: #999;

            span {
                color: #666;
                margin-left: 60px;
            }
        }
    }

    .num {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;

        .el-card {
            width: 32%;
            margin-bottom: 20px;
            // height: 80px !important;
        }

        .icons {
            width: 40px;
            height: 40px;
            padding: 20px;
            font-size: 30px;
            text-align: center;
            line-height: 70px;
            color: #fff;
        }

        .detail {
            margin-left: 30px;
            display: flex;
            flex-direction: column;
            justify-content: center;

            .num {
                font-size: 30px;
                margin-bottom: 10px;
            }

            .txt {
                font-size: 14px;
                text-align: left;
                color: #999;
            }
        }
    }

    .graph {
        margin-top: 20px;
        display: flex;
        justify-content: space-between;

        .el-card {
            width: 49.5%;
        }
    }

    .statistics-card {
        margin-bottom: 20px;

        .stat-item {
            height: 100px;
            cursor: pointer;
            transition: all 0.3s;

            &:hover {
                transform: translateY(-2px);
            }

            .stat-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                color: #666;

                .icon {
                    font-size: 20px;
                    padding: 8px;
                    border-radius: 50%;
                    
                    &.Clock {
                        background-color: #FFE4E6;
                        color: #FF4D4F;
                    }
                    &.CreditCard {
                        background-color: #E6F4FF;
                        color: #1890FF;
                    }
                    &.Download {
                        background-color: #FFF7E6;
                        color: #FFA940;
                    }
                    &.PieChart {
                        background-color: #F6FFED;
                        color: #52C41A;
                    }
                }
            }

            .stat-content {
                .current {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 5px;
                }

                .total {
                    font-size: 12px;
                    color: #999;
                }
            }
        }
    }
}

.quick-nav {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding: 10px;

    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        background-color: #f5f7fa;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.3s;

        &:hover {
            background-color: #ecf5ff;
            transform: translateY(-2px);
        }

        i {
            font-size: 24px;
            margin-bottom: 8px;
            color: #409EFF;
        }

        span {
            font-size: 14px;
            color: #606266;
        }
    }
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    margin-bottom: 20px;

    .chart-title, .time-filter {
        span {
            cursor: pointer;
            padding: 4px 12px;
            margin-right: 8px;
            border-radius: 4px;
            color: #606266;

            &.active {
                background-color: #409EFF;
                color: #fff;
            }

            &:hover:not(.active) {
                background-color: #f5f7fa;
            }
        }
    }
}
</style>
  