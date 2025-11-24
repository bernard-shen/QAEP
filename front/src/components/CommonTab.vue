<template>
    <div class="tags">
        <el-tag 
        :key="tag.index"
        v-for="(tag, index) in tags"
        :closable="tag.name !== 'home'"
        :disable-transitions="false"
        :effect="$route.name === tag.name ? 'dark': 'plain'"
        @click="changeMenu(tag)"
        @close="handleClose(tag,index)"
        >{{ tag.label }}</el-tag>
    </div>
</template>

<script>
import { useRouter, useRoute } from 'vue-router';
import { useStore } from 'vuex';
export default {
    setup() {
        const route = useRoute();
        const router = useRouter();
        const store = useStore();
        const tags = store.state.tabsList;
        
        const changeMenu = (item) => {
            router.push({
                name: item.name
            })
        };

        const handleClose = (tag, index) => {
            let length = tags.length - 1 ;
            store.commit("closeTab", tag); //删掉tag

            if (tag.name !== route.name) {
                return; //如果删除的tag非当前路由，也非选中的tag，则不做处理
            }

            if (index === length) {
                router.push({
                    name: tags[index - 1].name
                }); //如果删除的是最后一个tag，则默认选中tag前移；
            } else {
                router.push({
                    name: tags[index].name, //如果删除选中的tag本身，或之前的tag，则新tag路由后移；
                })
            }
        };

        return {
            tags,
            changeMenu,
            handleClose,
        };
    },
}
</script>

<style lang="less" scoped>
.tags {
    padding: 8px;
    // height: 42px;
    width: 100%;
    .el-tag {
        margin-right: 15px;
        // margin-left: 15px;
        cursor: pointer;
    }
}
</style>