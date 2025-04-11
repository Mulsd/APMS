<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')

const handleLogin = async () => {
  try {
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('password', password.value)

    const response = await axios.post('/token', formData)
    const token = response.data.access_token
    localStorage.setItem('token', token)
    
    // 设置全局请求头
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    
    ElMessage.success('登录成功')
    router.push('/mng/all')
  } catch (error: any) {
    ElMessage.error('登录失败：用户名或密码错误')
  }
}
</script>

<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2>登录系统</h2>
      </template>
      <el-form>
        <el-form-item label="用户名">
          <el-input v-model="username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  width: 400px;
}
</style>