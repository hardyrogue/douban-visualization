import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '@/layout/DefaultLayout.vue'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import MyFavorites from '../views/MyFavorites.vue'
import UserProfile from '../views/UserProfile.vue'
import MovieDetail from '../views/MovieDetail.vue'

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      { path: '', redirect: '/home' },
      { path: 'home', component: Home },
      { path: 'favorites', component: MyFavorites, meta: { requiresAuth: true } },
      { path: 'profile', name: 'UserProfile', component: UserProfile, meta: { requiresAuth: true } },
      { path: 'movie/:id', component: MovieDetail },
    ]
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/register',
    component: Register,
  },
  {
    path: '/users',
    name: '用户管理',
    component: () => import('@/views/UserList.vue')
  }
  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ✅ 路由守卫：仅拦截需要登录权限的页面
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
