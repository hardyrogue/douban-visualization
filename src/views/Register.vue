<template>
  <div class="login-container">
    <div class="login-left">
      <img src="/src/assets/login-bg.jpg" alt="背景图" />
    </div>
    <div class="login-right">
      <div class="login-box">
        <img class="logo" src="/src/assets/logo.png" alt="logo" />
        <h2>注册新用户</h2>

        <el-form :model="form" ref="formRef" label-position="top">
          <el-form-item prop="username">
            <el-input v-model="form.username" placeholder="用户名" />
          </el-form-item>

          <el-form-item prop="password">
            <el-input v-model="form.password" type="password" placeholder="密码" />
          </el-form-item>

          <el-form-item prop="confirm">
            <el-input v-model="form.confirm" type="password" placeholder="确认密码" />
          </el-form-item>

          <el-form-item>
            <el-input v-model="form.bio" placeholder="简介（可选）" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.email" placeholder="邮箱（可选）" />
          </el-form-item>

          <el-button type="warning" class="login-btn" @click="handleRegister" round block>
            注册
          </el-button>

          <p class="link-tip">已有账号？<router-link to="/login">去登录</router-link></p>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from '@/services/axios'

const router = useRouter()
const formRef = ref(null)
const form = reactive({
  username: '',
  password: '',
  confirm: '',
  bio: '',
  email: ''
})

const handleRegister = async () => {
  if (!form.username || !form.password) {
    return ElMessage.warning('用户名和密码不能为空')
  }
  if (form.password !== form.confirm) {
    return ElMessage.error('两次密码不一致')
  }

  try {
    // 注册
    await axios.post('/auth/register/', {
      username: form.username,
      password: form.password,
      bio: form.bio,
      email: form.email
    })


    // 自动登录
    const loginRes = await axios.post('/auth/login/', {
      username: form.username,
      password: form.password
    })

    const { token, user } = loginRes.data
    localStorage.setItem('token', token)
    localStorage.setItem('username', user.username)
    localStorage.setItem('role', user.role || 'user')

    ElMessage.success('注册并登录成功')
    router.push('/home')
  } catch (err) {
    console.error('注册失败', err)
    const msg = err?.response?.data?.error || err?.message || '注册失败'
    ElMessage.error(msg)
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
.link-tip {
  margin-top: 1rem;
  text-align: center;
  font-size: 14px;
}
</style>
