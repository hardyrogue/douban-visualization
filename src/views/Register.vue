<template>
  <div class="register-container">
    <div class="register-left">
      <img src="/src/assets/login-bg.jpg" alt="Register Background" />
    </div>
    <div class="register-right">
      <div class="register-box">
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

          <el-form-item prop="bio">
            <el-input v-model="form.bio" type="textarea" placeholder="简介（可选）" />
          </el-form-item>
          <el-form-item prop="bio">
            <el-input v-model="form.email" type="textarea" placeholder="邮箱" />
          </el-form-item>

          <el-button type="primary" class="register-btn" @click="handleRegister" round block>
            注册
          </el-button>

          <p class="link-tip">已有账号？<router-link to="/login">立即登录</router-link></p>
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
  avatar: '',
  bio: ''
})

const handleRegister = async () => {
  if (!form.username || !form.password) {
    return ElMessage.warning('用户名和密码不能为空')
  }
  if (form.password !== form.confirm) {
    return ElMessage.error('两次密码不一致')
  }

  try {
    // 1️⃣ 先注册
    const res = await axios.post('/auth/register/', {
      username: form.username,
      password: form.password
    })

    // ✅ 确认状态码是否合理
    if (res.status !== 200 && res.status !== 201) {
      throw new Error('注册失败')
    }

    // 2️⃣ 注册成功后自动登录
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
/* 样式与之前相同 */
.register-container {
  display: flex;
  height: 100vh;
  background-color: #2f2f2f;
}
.register-left {
  flex: 1;
}
.register-left img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.register-right {
  width: 400px;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px 0 0 8px;
}
.register-box {
  width: 80%;
}
.logo {
  width: 80px;
  margin: 0 auto 20px;
  display: block;
}
.register-btn {
  margin-top: 10px;
}
.link-tip {
  margin-top: 1rem;
  text-align: center;
  font-size: 14px;
}
</style>
