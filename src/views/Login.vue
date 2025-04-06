<template>
  <div class="login-page">
    <div class="login-card">
      <img class="logo" src="/src/assets/logo.png" alt="logo" />
      <h2 class="title">豆瓣电影可视化后台</h2>

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

        <el-button
          type="primary"
          class="login-btn"
          @click="handleLogin"
          round
        >
          登录
        </el-button>


        <p class="link-tip">还没有账号？<router-link to="/register">立即注册</router-link></p>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from '@/services/axios'

const router = useRouter()
const formRef = ref(null)
const form = reactive({ username: '', password: '' })

const handleLogin = async () => {
  try {
    await axios.post('/auth/login/', {
      username: form.username,
      password: form.password
    })

    const res = await axios.get('/auth/user/')
    const user = res.data

    localStorage.setItem('token', 'session')
    localStorage.setItem('username', user.username)
    localStorage.setItem('role', user.is_staff ? 'admin' : 'user')
    if (user.avatar) localStorage.setItem('avatar', user.avatar)
    if (user.bio) localStorage.setItem('bio', user.bio)

    ElMessage.success('登录成功')
    router.push('/home')
  } catch (err) {
    ElMessage.error(err?.response?.data?.error || '用户名或密码错误')
  }
}
</script>

<style scoped>
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

.login-page::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.6); /* 背景遮罩 */
  backdrop-filter: blur(4px); /* 背景模糊 */
}

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

.logo {
  width: 72px;
  margin: 0 auto 20px;
  display: block;
}

.title {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 2rem;
}

.login-btn {
  display: block;
  margin: 10px auto 0; /* 顶部 10px，居中 */
  padding: 0 2rem;
}
  

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
