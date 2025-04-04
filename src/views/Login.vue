<template>
  <div class="login-container">
    <div class="login-left">
      <img src="/src/assets/login-bg.jpg" alt="Login Background" />
    </div>
    <div class="login-right">
      <div class="login-box">
        <img class="logo" src="/src/assets/logo.png" alt="logo" />
        <h2>豆瓣电影可视化后台</h2>

        <el-form :model="form" ref="formRef" label-position="top">
          <el-form-item prop="username">
            <el-input v-model="form.username" placeholder="用户名">
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input v-model="form.password" placeholder="密码" type="password">
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-button type="warning" class="login-btn" @click="handleLogin" round block>
            登录
          </el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const formRef = ref(null)
const form = reactive({ username: '', password: '' })

const handleLogin = () => {
  if (form.username === 'admin' && form.password === '123456') {
    localStorage.setItem('token', 'mock-token')
    localStorage.setItem('role', 'admin')
    ElMessage.success('管理员登录成功')
    router.push('/home')
  } else if (form.username === 'user' && form.password === '123456') {
    localStorage.setItem('token', 'mock-token')
    localStorage.setItem('role', 'user')
    ElMessage.success('用户登录成功')
    router.push('/home')
  } else {
    ElMessage.error('用户名或密码错误')
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  background-color: #2f2f2f;
}
.login-left {
  flex: 1;
}
.login-left img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.login-right {
  width: 400px;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px 0 0 8px;
}
.login-box {
  width: 80%;
}
.logo {
  width: 80px;
  margin: 0 auto 20px;
  display: block;
}
.login-btn {
  margin-top: 10px;
}
</style>
