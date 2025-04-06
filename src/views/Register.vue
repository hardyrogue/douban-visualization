<template>
  <div class="login-container">
    <!-- 左侧背景图 -->
    <div class="login-left">
      <img src="/src/assets/login-bg.jpg" alt="背景图" />
    </div>

    <!-- 右侧注册表单 -->
    <div class="login-right">
      <div class="login-box">
        <img class="logo" src="/src/assets/logo.png" alt="logo" />
        <h2>注册新用户</h2>

        <!-- 注册表单 -->
        <el-form :model="form" ref="formRef" label-position="top">
          <!-- 用户名输入框 -->
          <el-form-item prop="username">
            <el-input v-model="form.username" placeholder="用户名" />
          </el-form-item>

          <!-- 密码输入框 -->
          <el-form-item prop="password">
            <el-input v-model="form.password" type="password" placeholder="密码" />
          </el-form-item>

          <!-- 确认密码输入框 -->
          <el-form-item prop="confirm">
            <el-input v-model="form.confirm" type="password" placeholder="确认密码" />
          </el-form-item>

          <!-- 简介（可选）输入框 -->
          <el-form-item>
            <el-input v-model="form.bio" placeholder="简介（可选）" />
          </el-form-item>

          <!-- 邮箱（可选）输入框 -->
          <el-form-item>
            <el-input v-model="form.email" placeholder="邮箱（可选）" />
          </el-form-item>

          <!-- 注册按钮 -->
          <el-button type="warning" class="login-btn" @click="handleRegister" round block>
            注册
          </el-button>

          <!-- 登录链接 -->
          <p class="link-tip">已有账号？<router-link to="/login">去登录</router-link></p>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
// 引入 Vue 和相关库
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from '@/services/axios'

// 路由实例
const router = useRouter()

// 表单引用和初始值
const formRef = ref(null)
const form = reactive({
  username: '',
  password: '',
  confirm: '',
  bio: '',
  email: ''
})

// 处理注册逻辑
const handleRegister = async () => {
  // 校验用户名和密码
  if (!form.username || !form.password) {
    return ElMessage.warning('用户名和密码不能为空')
  }
  if (form.password !== form.confirm) {
    return ElMessage.error('两次密码不一致')
  }

  try {
    // 注册请求
    await axios.post('/auth/register/', {
      username: form.username,
      password: form.password,
      bio: form.bio,
      email: form.email
    })

    // 注册成功后自动登录
    const loginRes = await axios.post('/auth/login/', {
      username: form.username,
      password: form.password
    })

    const { token, user } = loginRes.data
    // 存储 token 和用户信息
    localStorage.setItem('token', token)
    localStorage.setItem('username', user.username)
    localStorage.setItem('role', user.role || 'user')

    ElMessage.success('注册并登录成功')
    router.push('/home')  // 跳转到首页
  } catch (err) {
    console.error('注册失败', err)
    const msg = err?.response?.data?.error || err?.message || '注册失败'
    ElMessage.error(msg)
  }
}
</script>

<style scoped>
/* 注册页面容器样式 */
.login-container {
  display: flex;
  height: 100vh;
  background-color: #2f2f2f;
}

/* 左侧背景图样式 */
.login-left {
  flex: 1;
}
.login-left img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 右侧表单样式 */
.login-right {
  width: 400px;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px 0 0 8px;
}

/* 表单框样式 */
.login-box {
  width: 80%;
}

/* logo 样式 */
.logo {
  width: 80px;
  margin: 0 auto 20px;
  display: block;
}

/* 注册按钮样式 */
.login-btn {
  margin-top: 10px;
}

/* 登录链接样式 */
.link-tip {
  margin-top: 1rem;
  text-align: center;
  font-size: 14px;
}
</style>
