<script setup>
import { ref, onMounted, computed,onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/services/axios'
import { eventBus } from '@/eventBus'
const defaultAvatar = 'https://i.pravatar.cc/100?img=1'  // 默认头像
const router = useRouter()
const route = useRoute()

const user = ref({
  username: '',
  avatar: '',
  bio: '',
})

const fetchUserInfo = async () => {
  try {
    const res = await axios.get('/auth/user/')
    console.log('获取用户信息成功', res.data)  // 👈 看看有无 avatar、bio
    user.value = res.data
  } catch (err) {
    console.error('获取用户信息失败', err)
    router.push('/login')
  }
}

const logout = async () => {
  try {
    await axios.post('/auth/logout/')
  } catch (e) {
    console.warn('登出异常，可忽略', e)
  }
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  router.push('/login')
}

onMounted(() => {
  fetchUserInfo()
  eventBus.on('user-updated', fetchUserInfo)
})
onUnmounted(() => {
  eventBus.off('user-updated', fetchUserInfo)
})
const allMenus = [
  { path: '/home', name: '主页' },
  { path: '/dashboard', name: '数据看板' },
  { path: '/users', name: '用户管理', roles: ['admin'] },
  { path: '/settings', name: '系统设置', roles: ['admin'] },
  { path: '/favorites', name: '我的收藏' },
  { path: '/profile', name: '个人中心' },  
]

const userRole = localStorage.getItem('role') || 'user'
const menus = allMenus.filter(item => !item.roles || item.roles.includes(userRole))

const currentTitle = computed(() => {
  const current = menus.find(m => m.path === route.path)
  return current ? current.name : ''
})
</script>

<template>
  <el-container style="height: 100vh">
    <!-- 左侧菜单 -->
    <el-aside width="200px" class="sidebar">
      <div class="logo">🍿 豆瓣电影</div>
      <el-menu
        :default-active="route.path"
        class="el-menu-vertical"
        @select="(key) => router.push(key)"
        background-color="#24292f"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          {{ item.name }}
        </el-menu-item>
        
      </el-menu>
    </el-aside>

    <!-- 主区域 -->
    <el-container>
      <!-- 顶部栏 -->
      <el-header class="header">
  <div class="header-left">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item>豆瓣后台</el-breadcrumb-item>
      <el-breadcrumb-item>{{ currentTitle }}</el-breadcrumb-item>
    </el-breadcrumb>
  </div>

  <div class="header-right">
    <el-dropdown>
      <div class="user clickable-user" @click="router.push('/profile')">
        <el-avatar
          :size="30"
          :src="user.avatar || defaultAvatar"
        />
        <span class="username">{{ user.username }}</span>
      </div>

      <template #dropdown>
        <el-dropdown-menu class="user-dropdown">
          <div class="user-info">
            <el-avatar :size="40" :src="user.avatar" />
            <div class="user-meta">
              <div class="username">{{ user.username }}</div>
              <div class="bio">{{ user.bio || '暂无简介' }}</div>
            </div>
          </div>
          <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</el-header>


      <!-- 主内容 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.sidebar {
  background-color: #24292f;
  color: #fff;
  padding: 1rem;
}
.logo {
  font-size: 18px;
  font-weight: bold;
  color: #ffd04b;
  margin-bottom: 1rem;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
  background-color: #f5f5f5;
}

/* ⭐ header-right 是右上角头像区域容器 */
.header-right {
  margin-right: 0.5rem; /* ✅ 向左靠一点 */
}

/* ⭐ 面包屑字体 */
.breadcrumb {
  font-weight: bold;
}

.user {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}
.user:hover {
  background: rgba(0, 0, 0, 0.04);
}

/* ⭐ 头像下拉卡片整体样式 */
.user-dropdown {
  padding: 10px;
  width: 240px;
}

/* ⭐ 用户资料区域 */
.user-info {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  border-bottom: 1px solid #eee;
}

.user-meta {
  margin-left: 12px;
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
  font-size: 15px;
  color: #333;
}

.bio {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}

/* 主体内容 */
.main-content {
  background: #fff;
  padding: 2rem;
  min-height: calc(100vh - 64px);
}
.clickable-avatar {
  cursor: pointer;
}
.clickable-text {
  cursor: pointer;
  font-weight: bold;
  margin-left: 5px;
}
.clickable-user {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}
.clickable-user:hover {
  background: rgba(0, 0, 0, 0.05);
}
</style>