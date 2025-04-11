<script setup lang="ts">
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { useRouter } from 'vue-router'

const router = useRouter()
router.push('/welcome')
</script>

<template>
  <el-config-provider namespace="ep" :locale="zhCn">
    <div class="app-container">
      <BaseHeader class="app-header" />
      <div class="main-container">
        <BaseSide class="app-sidebar" />
        <div class="app-content">
          <RouterView />
        </div>
      </div>
    </div>
  </el-config-provider>
</template>

<style>
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.main-container {
  display: flex;
  height: calc(100vh - var(--ep-menu-item-height));
  margin-top: var(--ep-menu-item-height);
}

.app-sidebar {
  position: fixed;
  left: 0;
  top: var(--ep-menu-item-height);
  bottom: 0;
  overflow-y: auto;
}

.app-content {
  flex: 1;
  margin-left: 200px; /* 与侧边栏宽度相同 */
  margin-left: 200px; /* 侧边栏宽度 */
  padding: 20px;
  overflow-y: auto;
}
</style>
