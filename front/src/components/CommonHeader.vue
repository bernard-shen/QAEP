<template>
    <el-header>
        <div class="left-content">
            <el-button size="small" @click="handleCollapse">
                <el-icon :size="20">
                    <Menu />
                </el-icon>
            </el-button>
            <h3>首页</h3>
        </div>
        <div class="right-content">
            <el-dropdown>
                <span class="el-dropdown-link">
                    <img class="user" :src="getImgSrc('user')" alt="">
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item>个人中心</el-dropdown-item>
                        <el-dropdown-item @click="handleLoginOut">退出</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </el-header>
</template>

<script>
import { defineComponent } from 'vue';
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
export default defineComponent({
    setup() {
        const getImgSrc = (user) => {
            return new URL(`../assets/images/${user}.png`, import.meta.url).href
        };

        const router = useRouter();
        let store = useStore();
        let handleCollapse = () => {
            store.commit("updateIsCollapse");
        };
        const handleLoginOut = () => {
            store.commit('cleanMenu');
            store.commit('clearToken');
            router.push({
                name: 'login',
            })
        };

        return {
            getImgSrc,
            handleCollapse,
            handleLoginOut
        }

    }
})
</script>

<style lang="less" scoped>
header {
    display: flex;
    justify-content: space-between;
    align-items: center; // align-items只对具有显示属性（display）为flex或inline-flex的容器起作用; 
    //flex水平时，元素垂直方向居中对齐；flex垂直时，元素水平方向上居中对齐
    width: 100%;
    background: #333;
}
.right-content {
    .user {
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
}
.left-content {
    display: flex;
    align-items: center;
    .el-button {
        margin-right: 20px;
    }
    h3 {
        color: #fff;
    }
}

:deep(.bread span) {
    color:#fff !important;
    cursor: pointer !important;
}
</style>