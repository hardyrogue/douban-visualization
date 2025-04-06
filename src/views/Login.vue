<template>
  <div class="login-page">
    <!-- 登录卡片 -->
    <div class="login-card">
      <img class="logo" src="/src/assets/logo.png" alt="logo" />
      <h2 class="title">豆瓣电影可视化后台</h2>

      <!-- 登录表单 -->
      <el-form :model="form" ref="formRef" label-position="top">
        <!-- 用户名输入框 -->
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名">
            <template #prefix>
              <el-icon><User /></el-icon> <!-- 用户图标 -->
            </template>
          </el-input>
        </el-form-item>

        <!-- 密码输入框 -->
        <el-form-item prop="password">
          <el-input v-model="form.password" placeholder="密码" type="password">
            <template #prefix>
              <el-icon><Lock /></el-icon> <!-- 锁图标 -->
            </template>
          </el-input>
        </el-form-item>

        <!-- 登录按钮 -->
        <el-button
          type="primary"
          class="login-btn"
          @click="handleLogin" 
          round
        >
          登录
        </el-button>

        <!-- 注册链接 -->
        <p class="link-tip">
          还没有账号？
          <router-link to="/register">立即注册</router-link>
        </p>
      </el-form>
    </div>
  </div>
</template>

<script setup>
// 导入相关模块
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from '@/services/axios'

// 路由实例
const router = useRouter()

// 表单引用和状态
const formRef = ref(null)
const form = reactive({ username: '', password: '' })

// 登录处理函数
const handleLogin = async () => {
  try {
    // 发送登录请求
    await axios.post('/auth/login/', {
      username: form.username,
      password: form.password
    })

    // 获取用户信息
    const res = await axios.get('/auth/user/')
    const user = res.data

    // 将用户信息存储在 localStorage 中
    localStorage.setItem('token', 'session')  // 用 session 模拟 token
    localStorage.setItem('username', user.username)
    localStorage.setItem('role', user.is_staff ? 'admin' : 'user')
    if (user.avatar) localStorage.setItem('avatar', user.avatar)
    if (user.bio) localStorage.setItem('bio', user.bio)

    // 显示成功消息并跳转到主页
    ElMessage.success('登录成功')
    router.push('/home')
  } catch (err) {
    // 捕获错误并显示提示
    ElMessage.error(err?.response?.data?.error || '用户名或密码错误')
  }
}
</script>

<style scoped>
/* 登录页面基础样式 */
.login-page {
  height: 100vh;
  width: 100vw;
  background: url('/src/assets/login-bg.jpg') no-repeat center center;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

/* 背景遮罩和模糊效果 */
.login-page::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.6); /* 半透明遮罩 */
  backdrop-filter: blur(4px); /* 背景模糊 */
}

/* 登录卡片样式 */
.login-card {
  position: relative;
  z-index: 1;
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 12px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 380px;
}

/* logo 图片 */
.logo {
  width: 72px;
  margin: 0 auto 20px;
  display: block;
}

/* 标题样式 */
.title {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 2rem;
}

/* 登录按钮样式 */
.login-btn {
  display: block;
  margin: 10px auto 0;
  padding: 0 2rem;
}

/* 注册链接样式 */
.link-tip {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.link-tip a {
  color: #409eff;
  text-decoration: none;
}

.link-tip a:hover {
  text-decoration: underline;
}
</style>
