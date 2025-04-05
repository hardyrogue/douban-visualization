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
  <el-menu-item
    v-for="item in menus"
    :key="item.path"
    :index="item.path"
  >
    {{ item.name }}
  </el-menu-item>
</el-menu>

    </el-aside>

    <!-- 主区域 -->
    <el-container>
      <!-- 顶部栏 -->
      <el-header class="header">
        <div class="breadcrumb">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item>豆瓣后台</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <el-dropdown>
          <span class="user">
            <el-avatar :size="30" src="https://i.pravatar.cc/100?img=3" />
            {{ typeof window !== 'undefined' ? localStorage.getItem('username') || '游客' : '游客' }}
          </span>

          
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>

      <!-- 内容 -->
      <el-main class="main-content">
        <slot />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

// 获取用户角色（安全方式）
const safeGetItem = (key, fallback = '') => {
  return typeof window !== 'undefined' ? localStorage.getItem(key) || fallback : fallback
}

const router = useRouter()
const route = useRoute()

const allMenus = [
  { path: '/home', name: '主页' },
  { path: '/dashboard', name: '数据看板' },
  { path: '/users', name: '用户管理', roles: ['admin'] },
  { path: '/settings', name: '系统设置', roles: ['admin'] },
  { path: '/favorites', name: '我的收藏' }
]

const userRole = safeGetItem('role', 'admin')  // ⬅️ 安全获取角色
const menus = allMenus.filter(item => !item.roles || item.roles.includes(userRole))

const currentTitle = computed(() => {
  const current = menus.find(m => m.path === route.path)
  return current ? current.name : ''
})

const logout = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('role')
  }
  router.push('/login')
}
</script>


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
  padding: 0 1.5rem;
  background-color: #f5f5f5;
}

.breadcrumb {
  font-weight: bold;
}

.user {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.main-content {
  background: #fff;
  padding: 2rem;
  min-height: calc(100vh - 64px);
}
</style>
