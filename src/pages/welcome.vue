<script lang="ts" setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const handleNavigation = (path: string) => {
  router.push(path)
}
</script>

<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <h1 class="main-title">欢迎使用管理系统</h1>
      <h2 class="sub-title">选择下方按钮直达页面</h2>
      <div class="button-group">
        <el-button type="primary" class="welcome-button" @click="handleNavigation('/mng/upload')">添加项目</el-button>
        <el-button type="primary" class="welcome-button" @click="handleNavigation('/mng/all')">管理项目</el-button>
        <el-button type="primary" class="welcome-button" @click="handleNavigation('/mng/deliver')">交接管理</el-button>
        <el-button type="primary" class="welcome-button" @click="handleNavigation('/mng/payment')">财务管理</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.welcome-container {
  height: calc(100);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 60px;
}

.welcome-content {
  text-align: center;
}

.main-title {
  font-size: 48px;
  margin-bottom: 20px;
}

.sub-title {
  font-size: 24px;
  margin-bottom: 40px;
  color: #666;
}

.button-group {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.welcome-button {
  min-width: 120px;
}
</style>