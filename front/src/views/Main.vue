<template>
  <div class="common-layout">
    <el-container class="lay-container">
      <common-aside />
      <el-container>
        <common-header />
        <common-tab />
        <el-main class="right-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>
  

<script>
import { defineComponent } from 'vue';
import CommonHeader from '../components/CommonHeader.vue';
import CommonAside from '../components/CommonAside.vue';
import CommonTab from '../components/CommonTab.vue';

export default defineComponent({
  components: {
    CommonHeader,
    CommonAside,
    CommonTab,
  },
});
</script>


<style lang="less" scoped>

.el-container {
  flex-wrap: wrap;
  align-items: flex-start; // 基准线从最上层开始
  height: 100%;
}
.common-layout {
  .lay-container {
    flex-wrap: nowrap; //阻止项目在容器中换行
    .right-main {
      padding: 10px;
      height: calc(100% - 80px) !important; //!important css语法，强制应用该样式规则，即使有其他样式规则可能会覆盖它。//原始样式：height: calc(100% - 124px) !important;
    }
  }
  height: 100%;
  & > .el-container {
    height: 100%;
    & > .el-aside {
      height: 100%;
      background: #545c64;
    }
  }
}
</style>