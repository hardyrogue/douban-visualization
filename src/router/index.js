import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import MyFavorites from '../views/MyFavorites.vue'
import Register from '../views/Register.vue'
const routes = [
  {
    path: '/',
    redirect: '/home', // ✅ 默认跳到公开的首页
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/home',
    component: Home, // ✅ 搜索页是公开页面
  },
  {
    path: '/movie/:id',
    component: () => import('../views/MovieDetail.vue'), // ✅ 详情页也是公开的
  },
  {
    path: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }, // ✅ 后台页需登录
  },
  {
    path: '/favorites',
    component: MyFavorites,
    meta: { requiresAuth: true }, // ✅ 我的收藏需登录
  },
  {
    path: '/register',
    component: Register 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ✅ 路由守卫：仅拦截需要登录权限的页面
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')  // 或你用的登录状态字段
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
