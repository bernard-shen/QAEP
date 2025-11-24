<template>
    <el-aside :width="$store.state.isCollapse ? '72px' : '160px'">
        <el-menu 
        class="el-menu-vertical-demo" 
        background-color="#545c64" 
        text-color="#fff"
        :collapse="$store.state.isCollapse" 
        :collapse-transition="false">
        <h3 v-show="$store.state.isCollapse">AT平台</h3>
        <h3 v-show="!$store.state.isCollapse">质效提升平台</h3>
            <el-menu-item
            :index="item.path" 
            v-for="item in noChildren()" 
            :key="item.path" 
            @click="clickMenu(item)">
                <!-- vue3中，通过component标签的 :is属性来动态的获取标签展示 -->
                <component class="icons" :is="item.icon"></component>
                <span>{{ item.label }}</span>
            </el-menu-item>
            <el-sub-menu 
            :index="item.label" 
            v-for="item in hasChildren()" 
            :key="item.path" >
                <template #title>
                    <component class="icons" :is="item.icon"></component>
                    <span>{{ item.label }}</span>
                </template>
                <el-menu-item-group>
                    <el-menu-item 
                    :index="subItem.path" 
                    v-for="(subItem, subIndex) in item.children" 
                    :key="subIndex" 
                    @click="clickMenu(subItem)">
                        <component class="icons" :is="subItem.icon"></component>
                        <span>{{ subItem.label }}</span>
                    </el-menu-item>
                </el-menu-item-group>
            </el-sub-menu>
        </el-menu>
    </el-aside>
</template>

<script>
import { getCurrentInstance, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import { useStore } from 'vuex';
export default {
    setup() {
        const store = useStore();
        const router = useRouter();
        const { proxy } = getCurrentInstance();
        const list = [];
        // 通过ref对象定义响应式数据，访问时需通过 menu_list.value访问；
        // 此处的全部菜单数据 实际不需要响应式定义；
        // 但是获取接口并赋值，这个操作是异步的，所以需要定义异步 -使用async/await或者.then()方法来等待数据的获取完成；
        const menu_list = ref([])

        // 旧逻辑，后去所有菜单
        // const getMenuList = async () => {
        //     let res = await proxy.$api.getAllMenu();
        //     menu_list.value = res.data;
        //     console.log(menu_list,'menu_list')
        // };
        
        // 新逻辑，利用store中的state，来存取用户登录后的权限菜单列表
        const getMenuList = () => {
            menu_list.value = store.state.menu;
            console.log(menu_list,'menu_list')
        };

        const noChildren = () => {
            return menu_list.value.filter((item) => !item.children);
        };
        const hasChildren = () => {
            return menu_list.value.filter((item) => item.children);
        };

        const clickMenu = (item) => {
            // console.log(item.name,'name')
            // console.log(item.path,'path')
            router.push({
                name: item.name
            });
            store.commit("selectMenu", item);
        };

        onMounted(() => {
            getMenuList();
        });

        return {
            noChildren,
            hasChildren,
            clickMenu,
        }
    }
}
</script>

<style lang="less" scoped>
.icons {
    width: 18px;
    height: 18px;
    min-width: 18px; //遇到问题，侧边菜单收起是icons不展示，加了这个属性后才展示；
}
.el-menu {
    border-right: none;
    h3 {
        line-height: 48px;
        color: #fff;
        text-align: center;
    }
    .el-menu-item-group {
        .el-menu-item-group__title {
            margin: 0%;
            padding: 0%;
        }
        // ??????????未生效

    }

}



// .svg {
//     width: 12px;
//     height: 12px;
//     margin-right: 5px;
// }

</style>