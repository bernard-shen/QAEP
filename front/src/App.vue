<template>
    <router-view />
</template>


<script setup>
import { useStore } from "vuex";
import { useRouter } from "vue-router";
const store = useStore();
const router = useRouter();
store.commit("addMenu", router);

</script>


<style>
/* #用于选择具有特定id的元素， .用于选择具有特定class的元素*/
#app {
    height: 100%;
}
</style>